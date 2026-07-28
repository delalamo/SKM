"""GitHub Issues and Projects integration for the paper reading queue.

The functions in this module deliberately use only the Python standard library.
Network access is hidden behind an injectable JSON transport so the publishing
logic can be tested without contacting GitHub.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, MutableSet
from dataclasses import dataclass, field
from hashlib import sha256
import json
import re
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


MANAGED_BLOCK_BEGIN = "<!-- paperbot:managed:start -->"
MANAGED_BLOCK_END = "<!-- paperbot:managed:end -->"
META_PREFIX = "<!-- paperbot:meta "
REVISION_PREFIX = "<!-- paperbot:revision:"
DEFAULT_CUTOFF = 0.80
GITHUB_ACTIONS_BOT_LOGIN = "github-actions[bot]"
MANAGED_ISSUE_LABELS = ("paper", "AI-generated")
MANAGED_LABEL_SPECS = (
    ("paper", "1d76db", "Paper reading queue"),
    ("AI-generated", "6f42c1", "Created and maintained by automated tooling"),
)

_MANAGED_RE = re.compile(
    re.escape(MANAGED_BLOCK_BEGIN) + r".*?" + re.escape(MANAGED_BLOCK_END),
    re.DOTALL,
)
_META_RE = re.compile(r"<!-- paperbot:meta (\{.*?\}) -->")
_BACKTICK_RUN_RE = re.compile(r"`+")
_ARXIV_VERSION_RE = re.compile(r"v\d+$", re.IGNORECASE)
_NON_KEY_RE = re.compile(r"[^A-Za-z0-9_:.+\-/]")


class GitHubError(RuntimeError):
    """Raised when GitHub returns an error or an unexpected response."""

    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class JsonTransport(Protocol):
    """Small HTTP seam used by :class:`GitHubClient` and ProjectClient."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        json_body: Any | None = None,
    ) -> tuple[Any, Mapping[str, str]]: ...


class UrllibJsonTransport:
    """JSON transport backed by :mod:`urllib.request`."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        json_body: Any | None = None,
    ) -> tuple[Any, Mapping[str, str]]:
        data = None
        if json_body is not None:
            data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        request = Request(url, data=data, headers=dict(headers), method=method)
        try:
            with urlopen(request, timeout=60) as response:  # noqa: S310 - fixed GitHub URL
                raw = response.read()
                payload = json.loads(raw) if raw else None
                return payload, dict(response.headers.items())
        except HTTPError as error:
            raw = error.read().decode("utf-8", errors="replace")
            try:
                detail = json.loads(raw).get("message", raw)
            except json.JSONDecodeError:
                detail = raw
            raise GitHubError(
                f"GitHub request failed ({error.code}): {detail}", status=error.code
            ) from error
        except URLError as error:
            raise GitHubError(f"GitHub request failed: {error.reason}") from error


@dataclass(frozen=True)
class ManagedIssue:
    number: int
    node_id: str
    title: str
    body: str
    state: str
    html_url: str
    meta: dict[str, Any]
    labels: frozenset[str] = frozenset()


@dataclass
class ManagedIssueIndex:
    """Canonical lookups for trusted open and closed paperbot issues.

    Exact duplicate work IDs are retained in ``duplicates`` but excluded from
    canonical lookups and reconciliation.
    """

    issues: list[ManagedIssue] = field(default_factory=list)
    duplicates: list[ManagedIssue] = field(default_factory=list)
    by_alias: dict[str, ManagedIssue] = field(default_factory=dict)
    by_work_id: dict[str, ManagedIssue] = field(default_factory=dict)
    reserved_bibkeys: set[str] = field(default_factory=set)

    def add(self, issue: ManagedIssue) -> None:
        work_id = str(issue.meta.get("work_id", ""))
        bibkey = str(issue.meta.get("bibkey", ""))
        if bibkey:
            self.reserved_bibkeys.add(bibkey.casefold())
        incumbent = self.by_work_id.get(work_id) if work_id else None
        if incumbent is not None and incumbent.number != issue.number:
            # Legacy local runs authenticated as the repository owner, while
            # scheduled runs authenticate as github-actions. If both created
            # the same work before owner-authored issues were indexed, retain
            # the oldest issue as canonical and prevent any further copies.
            for alias in issue.meta.get("aliases", []):
                self._claim(
                    self.by_alias, normalize_alias(str(alias)), incumbent
                )
            self.duplicates.append(issue)
            return

        self.issues.append(issue)
        if work_id:
            self._claim(self.by_work_id, work_id, issue)
        for alias in issue.meta.get("aliases", []):
            self._claim(self.by_alias, normalize_alias(str(alias)), issue)

    @staticmethod
    def _claim(
        lookup: dict[str, ManagedIssue], key: str, issue: ManagedIssue
    ) -> None:
        if not key:
            return
        incumbent = lookup.get(key)
        if incumbent is not None and incumbent.number != issue.number:
            raise GitHubError(
                f"Managed paper identity {key!r} belongs to both "
                f"#{incumbent.number} and #{issue.number}"
            )
        lookup[key] = issue

    def find(self, record: Any) -> ManagedIssue | None:
        candidates: dict[int, ManagedIssue] = {}
        work_id, aliases = identity_for_record(record)
        if work_id in self.by_work_id:
            issue = self.by_work_id[work_id]
            candidates[issue.number] = issue
        for alias in aliases:
            issue = self.by_alias.get(alias)
            if issue is not None:
                candidates[issue.number] = issue
        if len(candidates) > 1:
            numbers = ", ".join(f"#{number}" for number in sorted(candidates))
            raise GitHubError(f"Paper aliases match multiple managed issues: {numbers}")
        return next(iter(candidates.values()), None)


@dataclass(frozen=True)
class UpsertResult:
    action: str
    issue: ManagedIssue | None
    substantive_change: bool = False
    project_score: float | None = None


class GitHubClient:
    """Minimal REST client for same-repository issue operations."""

    def __init__(
        self,
        repo: str,
        token: str,
        *,
        transport: JsonTransport | None = None,
        api_url: str = "https://api.github.com",
    ) -> None:
        if repo.count("/") != 1:
            raise ValueError("repo must be in 'owner/name' form")
        self.repo = repo
        self.token = token
        self.api_url = api_url.rstrip("/")
        self.transport = transport or UrllibJsonTransport()

    @property
    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "skm-paperbot/1",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(
        self, method: str, path: str, *, json_body: Any | None = None
    ) -> tuple[Any, Mapping[str, str]]:
        if method != "GET" and not self.token:
            raise GitHubError("a GitHub token is required for issue mutations")
        return self.transport.request(
            method,
            f"{self.api_url}{path}",
            headers=self._headers,
            json_body=json_body,
        )

    def _paginate(self, path: str, *, params: Mapping[str, str]) -> Iterable[Any]:
        page = 1
        while True:
            query = urlencode({**params, "per_page": "100", "page": str(page)})
            payload, _ = self._request("GET", f"{path}?{query}")
            if not isinstance(payload, list):
                raise GitHubError(f"Expected a list from {path}")
            yield from payload
            if len(payload) < 100:
                return
            page += 1

    def list_issues(self, *, label: str | None = "paper") -> list[dict[str, Any]]:
        path = f"/repos/{self.repo}/issues"
        # Created-ascending order makes page-number pagination stable when new
        # issues are opened while a long collection pass is in progress: new
        # rows are appended after the pages already read instead of shifting
        # their offsets. Label and state changes can still race a run, so
        # callers that need a snapshot validate duplicate identities.
        params = {"state": "all", "sort": "created", "direction": "asc"}
        if label:
            params["labels"] = label
        return [
            issue
            for issue in self._paginate(path, params=params)
            if "pull_request" not in issue
        ]

    def ensure_label(
        self, name: str = "paper", *, color: str = "1d76db", description: str = "Paper reading queue"
    ) -> None:
        path = f"/repos/{self.repo}/labels/{name}"
        try:
            self._request("GET", path)
        except GitHubError as error:
            if error.status != 404:
                raise
            self._request(
                "POST",
                f"/repos/{self.repo}/labels",
                json_body={"name": name, "color": color, "description": description},
            )

    def create_issue(self, *, title: str, body: str) -> dict[str, Any]:
        payload, _ = self._request(
            "POST",
            f"/repos/{self.repo}/issues",
            json_body={"title": title, "body": body, "labels": list(MANAGED_ISSUE_LABELS)},
        )
        return _expect_mapping(payload, "created issue")

    def update_issue(
        self,
        number: int,
        *,
        title: str | None = None,
        body: str | None = None,
        state: str | None = None,
    ) -> dict[str, Any]:
        changes = {
            key: value
            for key, value in {"title": title, "body": body, "state": state}.items()
            if value is not None
        }
        payload, _ = self._request(
            "PATCH", f"/repos/{self.repo}/issues/{number}", json_body=changes
        )
        return _expect_mapping(payload, "updated issue")

    def list_comments(self, number: int) -> list[dict[str, Any]]:
        path = f"/repos/{self.repo}/issues/{number}/comments"
        return list(self._paginate(path, params={}))

    def create_comment(self, number: int, body: str) -> dict[str, Any]:
        payload, _ = self._request(
            "POST",
            f"/repos/{self.repo}/issues/{number}/comments",
            json_body={"body": body},
        )
        return _expect_mapping(payload, "created comment")

    def add_labels(self, number: int, labels: Iterable[str]) -> None:
        self._request(
            "POST",
            f"/repos/{self.repo}/issues/{number}/labels",
            json_body={"labels": list(labels)},
        )


class ProjectClient:
    """GraphQL client for one user-owned GitHub Project v2."""

    def __init__(
        self,
        token: str,
        owner: str,
        project_number: int,
        *,
        relevance_field: str = "Relevance",
        transport: JsonTransport | None = None,
        graphql_url: str = "https://api.github.com/graphql",
    ) -> None:
        if not token:
            raise ValueError("PROJECTS_TOKEN is required for Project updates")
        self.token = token
        self.owner = owner
        self.project_number = int(project_number)
        self.relevance_field = relevance_field
        self.transport = transport or UrllibJsonTransport()
        self.graphql_url = graphql_url
        self._project_id: str | None = None
        self._field_id: str | None = None

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "skm-paperbot/1",
        }

    def _graphql(self, query: str, variables: Mapping[str, Any]) -> dict[str, Any]:
        payload, _ = self.transport.request(
            "POST",
            self.graphql_url,
            headers=self._headers,
            json_body={"query": query, "variables": dict(variables)},
        )
        result = _expect_mapping(payload, "GraphQL response")
        if result.get("errors"):
            messages = "; ".join(
                str(error.get("message", error)) for error in result["errors"]
            )
            raise GitHubError(f"GitHub Project GraphQL error: {messages}")
        data = result.get("data")
        if not isinstance(data, dict):
            raise GitHubError("GitHub Project GraphQL response has no data")
        return data

    def _resolve_project(self) -> tuple[str, str]:
        if self._project_id and self._field_id:
            return self._project_id, self._field_id
        data = self._graphql(
            """
            query PaperbotProject($owner: String!, $number: Int!) {
              user(login: $owner) {
                projectV2(number: $number) {
                  id
                  fields(first: 100) {
                    nodes {
                      ... on ProjectV2Field { id name dataType }
                    }
                  }
                }
              }
            }
            """,
            {"owner": self.owner, "number": self.project_number},
        )
        user = data.get("user")
        project = user.get("projectV2") if isinstance(user, dict) else None
        if not isinstance(project, dict):
            raise GitHubError(
                f"User project {self.owner}/{self.project_number} was not found"
            )
        fields = project.get("fields", {}).get("nodes", [])
        match = next(
            (
                item
                for item in fields
                if isinstance(item, dict)
                and item.get("name") == self.relevance_field
                and item.get("dataType") == "NUMBER"
            ),
            None,
        )
        if match is None:
            raise GitHubError(
                f"Project field {self.relevance_field!r} is missing or is not numeric"
            )
        self._project_id = str(project["id"])
        self._field_id = str(match["id"])
        return self._project_id, self._field_id

    def _find_item(self, issue_node_id: str, project_id: str) -> str | None:
        data = self._graphql(
            """
            query PaperbotProjectItem($issue: ID!) {
              node(id: $issue) {
                ... on Issue {
                  projectItems(first: 100, includeArchived: true) {
                    nodes { id project { id } }
                  }
                }
              }
            }
            """,
            {"issue": issue_node_id},
        )
        node = data.get("node")
        if not isinstance(node, dict):
            raise GitHubError(f"Issue node {issue_node_id!r} was not found")
        for item in node.get("projectItems", {}).get("nodes", []):
            if isinstance(item, dict) and item.get("project", {}).get("id") == project_id:
                return str(item["id"])
        return None

    def sync(self, issue_node_id: str, score: float) -> str:
        project_id, field_id = self._resolve_project()
        item_id = self._find_item(issue_node_id, project_id)
        if item_id is None:
            data = self._graphql(
                """
                mutation PaperbotAddItem($project: ID!, $content: ID!) {
                  addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
                    item { id }
                  }
                }
                """,
                {"project": project_id, "content": issue_node_id},
            )
            item = data.get("addProjectV2ItemById", {}).get("item")
            if not isinstance(item, dict) or not item.get("id"):
                raise GitHubError("GitHub did not return the newly added Project item")
            item_id = str(item["id"])
        self._graphql(
            """
            mutation PaperbotSetRelevance(
              $project: ID!, $item: ID!, $field: ID!, $score: Float!
            ) {
              updateProjectV2ItemFieldValue(input: {
                projectId: $project,
                itemId: $item,
                fieldId: $field,
                value: {number: $score}
              }) { projectV2Item { id } }
            }
            """,
            {
                "project": project_id,
                "item": item_id,
                "field": field_id,
                "score": float(score),
            },
        )
        return item_id


def ensure_paper_label(client: GitHubClient) -> None:
    """Ensure both labels required on every paperbot-managed issue exist."""

    for name, color, description in MANAGED_LABEL_SPECS:
        client.ensure_label(name, color=color, description=description)


def load_managed_issues(client: GitHubClient) -> ManagedIssueIndex:
    index = ManagedIssueIndex()
    # Search all issues so removing a label cannot make the next run duplicate a
    # managed paper thread. Pull requests are filtered by GitHubClient. Trust
    # both Actions and the repository owner because the supported local runner
    # creates issues as the owner. Check authorship before parsing the marker so
    # other public users cannot claim aliases or make malformed marker text
    # abort discovery.
    trusted_logins = {GITHUB_ACTIONS_BOT_LOGIN}
    repository = str(getattr(client, "repo", "") or "")
    owner, separator, _name = repository.partition("/")
    if separator and owner:
        trusted_logins.add(owner.casefold())
    managed: list[ManagedIssue] = []
    for raw in client.list_issues(label=None):
        author = raw.get("user")
        login = str(author.get("login", "") if isinstance(author, Mapping) else "")
        if login.casefold() not in trusted_logins:
            continue
        body = str(raw.get("body") or "")
        meta = parse_managed_meta(body)
        if meta is None:
            continue
        blocks = list(_MANAGED_RE.finditer(body))
        if (
            len(blocks) != 1
            or body.count(MANAGED_BLOCK_BEGIN) != 1
            or body.count(MANAGED_BLOCK_END) != 1
            or META_PREFIX not in blocks[0].group(0)
        ):
            number = raw.get("number", "?")
            raise GitHubError(
                f"Managed paper issue #{number} must contain exactly one "
                "complete paperbot block"
            )
        managed.append(_managed_issue_from_api(raw, meta))
    for issue in sorted(managed, key=lambda item: item.number):
        index.add(issue)
    return index


def upsert_paper_issue(
    client: GitHubClient,
    record: Any,
    score: float,
    bibtex: str,
    bibkey: str,
    known_bib_key: str | None = None,
    *,
    index: ManagedIssueIndex | None = None,
    model_hash: str = "",
    cutoff: float = DEFAULT_CUTOFF,
) -> UpsertResult:
    """Create or reconcile the one managed issue for *record*.

    New papers at or below the strict cutoff are skipped. Existing papers are
    updated regardless of score so revisions can be surfaced and closed issues
    can be reopened.
    """

    if not 0.0 <= float(score) <= 1.0:
        raise ValueError("score must be between zero and one")
    index = index or load_managed_issues(client)
    existing = index.find(record)
    if existing is None and float(score) <= cutoff:
        return UpsertResult("skipped", None, project_score=float(score))

    meta = build_managed_meta(
        record,
        score,
        bibtex,
        bibkey,
        model_hash=model_hash,
        known_bib_key=known_bib_key,
    )
    managed_body = render_managed_body(
        record,
        score,
        bibtex,
        bibkey,
        known_bib_key=known_bib_key,
        meta=meta,
    )
    title = str(_value(record, "title", "")).strip()
    if not title:
        raise ValueError("paper title is required")

    if existing is None:
        ensure_paper_label(client)
        raw = client.create_issue(title=title, body=managed_body)
        issue = _managed_issue_from_api(raw, meta)
        index.add(issue)
        return UpsertResult("created", issue, True, float(score))

    old_meta = existing.meta
    substantive = old_meta.get("metadata_hash") != meta["metadata_hash"]
    score_changed = _score_changed(old_meta.get("score"), score)
    model_changed = old_meta.get("model_hash", "") != model_hash
    identity_changed = (
        old_meta.get("work_id") != meta["work_id"]
        or old_meta.get("aliases", []) != meta["aliases"]
        or old_meta.get("bibkey") != bibkey
        or old_meta.get("known_bib_key") != known_bib_key
    )
    title_changed = existing.title != title
    missing_labels = _missing_managed_labels(existing.labels)
    label_missing = bool(missing_labels)
    content_changed = (
        substantive or score_changed or model_changed or identity_changed or title_changed
    )
    if not (content_changed or label_missing):
        return UpsertResult("unchanged", existing, False, float(score))

    if label_missing:
        ensure_paper_label(client)
        client.add_labels(existing.number, missing_labels)
        if not content_changed:
            return UpsertResult("relabeled", existing, False, float(score))
    if substantive:
        revision_marker = f"{REVISION_PREFIX}{meta['metadata_hash']} -->"
        if not any(
            revision_marker in str(comment.get("body") or "")
            for comment in client.list_comments(existing.number)
        ):
            changed = _changed_fields(old_meta, meta)
            version = str(meta.get("version") or "unspecified version")
            updated = str(meta.get("updated") or "unknown date")
            client.create_comment(
                existing.number,
                "Paper metadata was updated "
                f"({version}, {updated}). Changed: {', '.join(changed)}.\n\n"
                f"{revision_marker}",
            )
    body = replace_managed_block(existing.body, managed_body)
    state = "open" if substantive and existing.state == "closed" else None
    raw = client.update_issue(
        existing.number,
        title=title if title_changed else None,
        body=body,
        state=state,
    )
    issue = _managed_issue_from_api(raw, meta)
    action = "updated" if substantive or identity_changed or title_changed else "rescored"
    return UpsertResult(action, issue, substantive, float(score))


def sync_project(project: ProjectClient, issue_node_id: str, score: float) -> str:
    return project.sync(issue_node_id, score)


def rescore_managed_issues(
    client: GitHubClient,
    scorer: Callable[[ManagedIssue], float],
    model_hash: str,
    *,
    project: ProjectClient | None = None,
    index: ManagedIssueIndex | None = None,
) -> list[UpsertResult]:
    """Relabel all managed issues, silently rescore open ones, and sync the Project."""

    index = index or load_managed_issues(client)
    results: list[UpsertResult] = []
    label_ensured = False
    for existing in index.issues:
        missing_labels = _missing_managed_labels(existing.labels)
        relabeled = bool(missing_labels)
        if relabeled:
            if not label_ensured:
                ensure_paper_label(client)
                label_ensured = True
            client.add_labels(existing.number, missing_labels)
        if existing.state != "open":
            results.append(
                UpsertResult("relabeled" if relabeled else "unchanged", existing)
            )
            if project is not None:
                project.sync(existing.node_id, float(existing.meta.get("score", 0.0)))
            continue
        issue = existing
        score = float(existing.meta.get("score", 0.0))
        if existing.meta.get("model_hash") != model_hash:
            score = float(scorer(existing))
            if not 0.0 <= score <= 1.0:
                raise ValueError(f"scorer returned invalid score for issue #{existing.number}")
            meta = dict(existing.meta)
            meta["score"] = score
            meta["model_hash"] = model_hash
            block = update_managed_score(existing.body, meta)
            body = replace_managed_block(existing.body, block)
            raw = client.update_issue(existing.number, body=body)
            issue = _managed_issue_from_api(raw, meta)
            results.append(UpsertResult("rescored", issue, False, score))
        else:
            results.append(
                UpsertResult("relabeled" if relabeled else "unchanged", issue, False, score)
            )
        if project is not None:
            project.sync(issue.node_id, score)
    return results


def parse_managed_meta(body: str) -> dict[str, Any] | None:
    matches = list(_META_RE.finditer(body))
    if not matches:
        if META_PREFIX in body:
            raise GitHubError("Managed paper issue contains an incomplete metadata marker")
        return None
    if len(matches) != 1 or body.count(META_PREFIX) != 1:
        raise GitHubError("Managed paper issue must contain exactly one metadata marker")
    match = matches[0]
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise GitHubError("Managed paper issue contains invalid metadata JSON") from error
    schema = payload.get("schema") if isinstance(payload, dict) else None
    if (
        not isinstance(payload, dict)
        or not isinstance(schema, int)
        or isinstance(schema, bool)
        or schema != 1
    ):
        raise GitHubError("Managed paper issue has an unsupported metadata schema")
    return payload


def replace_managed_block(body: str, managed_body: str) -> str:
    """Replace only the bot-owned block, preserving user text around it."""

    if _MANAGED_RE.search(body):
        return _MANAGED_RE.sub(lambda _match: managed_body, body, count=1)
    if parse_managed_meta(body) is not None:
        raise GitHubError("Managed metadata exists outside a complete managed block")
    return f"{body.rstrip()}\n\n{managed_body}".lstrip()


def render_managed_body(
    record: Any,
    score: float,
    bibtex: str,
    bibkey: str,
    *,
    known_bib_key: str | None = None,
    meta: Mapping[str, Any] | None = None,
) -> str:
    meta = dict(
        meta
        or build_managed_meta(
            record, score, bibtex, bibkey, known_bib_key=known_bib_key
        )
    )
    metadata = json.dumps(meta, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    identifiers = _identifier_lines(record)
    abstract = str(_value(record, "abstract", "")).strip()
    authors = _display_authors(record)
    venue = _display_venue(record)
    date = _display_date(record)
    if known_bib_key:
        bibliography_note = (
            f"This work is already in `bibliography.bib` as `{known_bib_key}`. "
            "Use the entry below as a replacement/update, not as an additional entry."
        )
    else:
        bibliography_note = (
            f"The collision-checked citation key is `{bibkey}`; the entry below is ready to copy."
        )
    return "\n".join(
        [
            MANAGED_BLOCK_BEGIN,
            f"{META_PREFIX}{metadata} -->",
            f"**Authors:** {authors}",
            "",
            f"**Venue:** {venue}",
            f"**Date:** {date}",
            "",
            f"**Relevance:** {float(score):.6f}",
            "",
            "## Identifiers",
            "",
            *(identifiers or ["No stable external identifier was supplied."]),
            "",
            "## Abstract",
            "",
            abstract,
            "",
            "## BibTeX",
            "",
            bibliography_note,
            "",
            _code_fence(bibtex.strip(), "bibtex"),
            MANAGED_BLOCK_END,
        ]
    )


def update_managed_score(body: str, meta: Mapping[str, Any]) -> str:
    match = _MANAGED_RE.search(body)
    if not match:
        raise GitHubError("Cannot rescore an issue without a complete managed block")
    block = match.group(0)
    metadata = json.dumps(dict(meta), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    block = _META_RE.sub(lambda _match: f"{META_PREFIX}{metadata} -->", block, count=1)
    block, count = re.subn(
        r"\*\*Relevance:\*\* [0-9]+(?:\.[0-9]+)?",
        f"**Relevance:** {float(meta['score']):.6f}",
        block,
        count=1,
    )
    if count != 1:
        raise GitHubError("Managed issue is missing its relevance line")
    return block


def build_managed_meta(
    record: Any,
    score: float,
    bibtex: str,
    bibkey: str,
    *,
    model_hash: str = "",
    known_bib_key: str | None = None,
) -> dict[str, Any]:
    work_id, aliases = identity_for_record(record)
    authors = _value(record, "authors", []) or []
    if isinstance(authors, str):
        authors = [authors]
    fields = {
        "title": str(_value(record, "title", "")).strip(),
        "abstract": str(_value(record, "abstract", "")).strip(),
        "bibtex": bibtex.strip(),
        "identifiers": json.dumps(aliases, separators=(",", ":")),
        "version": str(_value(record, "version", "") or ""),
        "authors": json.dumps(list(authors), ensure_ascii=False, separators=(",", ":")),
        "venue": str(_value(record, "venue", "") or ""),
        "url": str(_value(record, "url", "") or ""),
        "created": _timestamp_text(
            _value(record, "created_at", "") or _value(record, "created", "")
        ),
        "updated": _timestamp_text(
            _value(record, "updated_at", "")
            or _value(record, "updated", "")
            or _value(record, "updated_date", "")
        ),
        "license": str(_value(record, "license", "") or ""),
    }
    field_hashes = {
        name: sha256(value.encode("utf-8")).hexdigest() for name, value in fields.items()
    }
    metadata_hash = sha256(
        json.dumps(fields, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()
    return {
        "schema": 1,
        "work_id": work_id,
        "aliases": aliases,
        "version": str(_value(record, "version", "") or ""),
        "updated": _timestamp_text(
            _value(record, "updated_at", "")
            or _value(record, "updated", "")
            or _value(record, "updated_date", "")
        ),
        "metadata_hash": metadata_hash,
        "field_hashes": field_hashes,
        "model_hash": model_hash,
        "bibkey": bibkey,
        "known_bib_key": known_bib_key,
        "score": float(score),
    }


def identity_for_record(record: Any) -> tuple[str, list[str]]:
    aliases: set[str] = set()
    doi = normalize_doi(str(_value(record, "doi", "") or ""))
    pmid = str(_value(record, "pmid", "") or "").strip()
    arxiv_id = normalize_arxiv_id(
        str(_value(record, "arxiv_id", "") or _value(record, "arxiv", "") or "")
    )
    source = str(_value(record, "source", "") or "").strip().casefold()
    source_id = str(_value(record, "source_id", "") or "").strip()
    if doi:
        aliases.add(f"doi:{doi}")
    if pmid:
        aliases.add(f"pmid:{pmid}")
    if arxiv_id:
        aliases.add(f"arxiv:{arxiv_id}")
    if source and source_id:
        aliases.add(f"{source}:{source_id.casefold()}")
    identity_aliases = getattr(record, "identity_aliases", None)
    if callable(identity_aliases):
        aliases.update(
            normalized
            for alias in identity_aliases()
            if (normalized := normalize_alias(str(alias)))
        )
    related = _value(record, "aliases", []) or []
    related_work = _value(record, "related_work_aliases", []) or []
    related_ids = _value(record, "related_ids", []) or []
    for alias in [*related, *related_work, *related_ids]:
        normalized = normalize_alias(str(alias))
        if normalized:
            aliases.add(normalized)
    title_alias = title_identity_alias(record)
    if title_alias:
        aliases.add(title_alias)
    canonical_id = normalize_alias(str(_value(record, "canonical_id", "") or ""))
    if canonical_id:
        # The collector requires the canonical work identity to be one of the
        # hashed aliases. Keeping that invariant here prevents paperbot from
        # creating an issue that its own training refresh later rejects.
        aliases.add(canonical_id)
    ordered = sorted(aliases)
    preferred = canonical_id or next(
        (
            prefix
            for kind in ("doi:", "pmid:", "arxiv:", f"{source}:", "title:")
            for prefix in ordered
            if prefix.startswith(kind)
        ),
        "",
    )
    if not preferred:
        raise ValueError("paper requires a stable identifier or title identity")
    return preferred, ordered


def title_identity_alias(record: Any) -> str:
    native_alias = str(_value(record, "title_alias", "") or "")
    if native_alias:
        return normalize_alias(native_alias)
    title = _normalize_identity_text(str(_value(record, "title", "") or ""))
    if not title:
        return ""
    authors = _value(record, "authors", []) or []
    if isinstance(authors, str):
        first_author = authors.split(" and ", 1)[0]
    else:
        first_author = str(next(iter(authors), ""))
    first_author = _normalize_identity_text(first_author)
    year = str(
        _value(record, "year", "")
        or _timestamp_text(
            _value(record, "created_at", "")
            or _value(record, "created", "")
            or _value(record, "published", "")
        )[:4]
    )
    if not first_author or not re.fullmatch(r"\d{4}", year):
        return ""
    digest = sha256(f"{title}\0{first_author}\0{year}".encode()).hexdigest()
    return f"title:{digest}"


def normalize_alias(alias: str) -> str:
    alias = alias.strip()
    if not alias:
        return ""
    kind, separator, value = alias.partition(":")
    if not separator:
        return alias.casefold()
    kind = kind.casefold()
    if kind == "doi":
        value = normalize_doi(value)
    elif kind == "arxiv":
        value = normalize_arxiv_id(value)
    else:
        value = value.strip().casefold()
    return f"{kind}:{value}" if value else ""


def normalize_doi(value: str) -> str:
    value = value.strip().casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    return value.strip().rstrip(".")


def normalize_arxiv_id(value: str) -> str:
    value = value.strip().casefold()
    for prefix in ("https://arxiv.org/abs/", "http://arxiv.org/abs/", "arxiv:"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    return _ARXIV_VERSION_RE.sub("", value)


def reserve_bibtex_key(
    preferred: str,
    reserved: MutableSet[str],
    *,
    aliases_for_same_work: Iterable[str] = (),
) -> str:
    """Reserve a key, adding ``_B``, ``_C`` … on real collisions.

    ``reserved`` is compared case-insensitively. Passing aliases for the same
    work lets an existing canonical key be reused.
    """

    preferred = _NON_KEY_RE.sub("", preferred.strip())
    if not preferred:
        raise ValueError("preferred BibTeX key is empty or invalid")
    folded = {str(key).casefold() for key in reserved}
    same = {str(key).casefold() for key in aliases_for_same_work}
    if preferred.casefold() not in folded or preferred.casefold() in same:
        reserved.add(preferred)
        return preferred
    suffix = 1
    while True:
        candidate = f"{preferred}_{_alpha_suffix(suffix)}"
        if candidate.casefold() not in folded:
            reserved.add(candidate)
            return candidate
        suffix += 1


def _alpha_suffix(number: int) -> str:
    # Deliberately begin at B; the unsuffixed key is the implicit A variant.
    number += 1
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def _managed_issue_from_api(raw: Mapping[str, Any], meta: dict[str, Any]) -> ManagedIssue:
    labels = frozenset(
        str(label.get("name", "") if isinstance(label, Mapping) else label)
        for label in (raw.get("labels") or [])
    )
    return ManagedIssue(
        number=int(raw["number"]),
        node_id=str(raw.get("node_id") or raw.get("id") or ""),
        title=str(raw.get("title") or ""),
        body=str(raw.get("body") or ""),
        state=str(raw.get("state") or "open"),
        html_url=str(raw.get("html_url") or ""),
        meta=meta,
        labels=labels,
    )


def _identifier_lines(record: Any) -> list[str]:
    result: list[str] = []
    url = str(_value(record, "url", "") or "").strip()
    doi = normalize_doi(str(_value(record, "doi", "") or ""))
    pmid = str(_value(record, "pmid", "") or "").strip()
    arxiv_id = normalize_arxiv_id(
        str(_value(record, "arxiv_id", "") or _value(record, "arxiv", "") or "")
    )
    source = str(_value(record, "source", "") or "").strip()
    source_id = str(_value(record, "source_id", "") or "").strip()
    if doi:
        result.append(f"- DOI: [{doi}](https://doi.org/{doi})")
    if pmid:
        result.append(f"- PMID: [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")
    if arxiv_id:
        result.append(f"- arXiv: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})")
    if source and source_id:
        result.append(f"- Source: {source} `{source_id}`")
    if url and not any(url in line for line in result):
        result.append(f"- Paper: {url}")
    return result


def _display_authors(record: Any) -> str:
    authors = _value(record, "authors", []) or []
    if isinstance(authors, str):
        authors = re.split(r"\s+and\s+", authors, flags=re.IGNORECASE)
    names = [str(author).strip() for author in authors if str(author).strip()]
    return "; ".join(names) if names else "Not supplied"


def _display_venue(record: Any) -> str:
    venue = str(_value(record, "venue", "") or "").strip()
    source = str(_value(record, "source", "") or "").strip()
    value = venue or source
    brands = {
        "arxiv": "arXiv",
        "biorxiv": "bioRxiv",
        "chemrxiv": "ChemRxiv",
        "medrxiv": "medRxiv",
        "pubmed": "PubMed",
    }
    return brands.get(value.casefold(), value or "Not supplied")


def _display_date(record: Any) -> str:
    metadata = _value(record, "metadata", {}) or {}
    if isinstance(metadata, Mapping):
        for key in ("publication_date", "preprint_date", "published_date"):
            text = _timestamp_text(metadata.get(key))
            match = re.match(r"((?:19|20)\d{2}(?:-\d{2}-\d{2})?)", text)
            if match:
                return match.group(1)
    for name in ("created_at", "created", "published", "updated_at", "updated", "updated_date"):
        text = _timestamp_text(_value(record, name, ""))
        match = re.match(r"((?:19|20)\d{2}(?:-\d{2}-\d{2})?)", text)
        if match:
            return match.group(1)
    year = str(_value(record, "year", "") or "")
    match = re.search(r"(?:19|20)\d{2}", year)
    return match.group(0) if match else "Not supplied"


def _missing_managed_labels(labels: Iterable[str]) -> list[str]:
    present = {str(label).casefold() for label in labels}
    return [label for label in MANAGED_ISSUE_LABELS if label.casefold() not in present]


def _changed_fields(old: Mapping[str, Any], new: Mapping[str, Any]) -> list[str]:
    old_hashes = old.get("field_hashes")
    new_hashes = new.get("field_hashes")
    if not isinstance(old_hashes, dict) or not isinstance(new_hashes, dict):
        return ["metadata"]
    changed = [
        name.replace("_", " ")
        for name in (
            "title",
            "abstract",
            "bibtex",
            "identifiers",
            "version",
            "authors",
            "venue",
            "url",
            "created",
            "updated",
            "license",
        )
        if old_hashes.get(name) != new_hashes.get(name)
    ]
    return changed or ["metadata"]


def _score_changed(old: Any, new: float) -> bool:
    try:
        return abs(float(old) - float(new)) > 5e-7
    except (TypeError, ValueError):
        return True


def _normalize_identity_text(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def _timestamp_text(value: Any) -> str:
    if value is None or value == "":
        return ""
    isoformat = getattr(value, "isoformat", None)
    return str(isoformat() if callable(isoformat) else value)


def _code_fence(value: str, language: str) -> str:
    longest = max((len(match.group(0)) for match in _BACKTICK_RUN_RE.finditer(value)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}\n{value}\n{fence}"


def _value(record: Any, name: str, default: Any = None) -> Any:
    if isinstance(record, Mapping):
        return record.get(name, default)
    return getattr(record, name, default)


def _expect_mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GitHubError(f"Expected an object for {context}")
    return value


__all__ = [
    "DEFAULT_CUTOFF",
    "GITHUB_ACTIONS_BOT_LOGIN",
    "GitHubClient",
    "GitHubError",
    "ManagedIssue",
    "ManagedIssueIndex",
    "MANAGED_ISSUE_LABELS",
    "ProjectClient",
    "UpsertResult",
    "build_managed_meta",
    "ensure_paper_label",
    "identity_for_record",
    "load_managed_issues",
    "normalize_alias",
    "parse_managed_meta",
    "render_managed_body",
    "replace_managed_block",
    "reserve_bibtex_key",
    "rescore_managed_issues",
    "sync_project",
    "upsert_paper_issue",
]
