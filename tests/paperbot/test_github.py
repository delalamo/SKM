from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from scripts.paperbot.github import (
    GitHubClient,
    GitHubError,
    ManagedIssueIndex,
    ProjectClient,
    build_managed_meta,
    identity_for_record,
    load_managed_issues,
    parse_managed_meta,
    render_managed_body,
    replace_managed_block,
    reserve_bibtex_key,
    rescore_managed_issues,
    upsert_paper_issue,
)
from scripts.paperbot.records import PaperRecord


@dataclass
class Paper:
    title: str = "A useful paper"
    abstract: str = "A complete abstract."
    authors: tuple[str, ...] = ("Ada Lovelace",)
    year: int = 2026
    doi: str = "https://doi.org/10.1000/Test"
    pmid: str = "12345"
    arxiv_id: str = "2501.00001v2"
    source: str = "biorxiv"
    source_id: str = "10.1000/test"
    venue: str = "bioRxiv"
    version: str = "v2"
    created: str = "2026-07-20"
    updated: str = "2026-07-22"
    url: str = "https://example.test/paper"
    aliases: tuple[str, ...] = ()
    related_work_aliases: tuple[str, ...] = ()


class MemoryIssueClient:
    def __init__(self, issues: list[dict[str, Any]] | None = None) -> None:
        self.repo = "delalamo/SKM"
        self.issues = deepcopy(issues or [])
        self.calls: list[tuple[Any, ...]] = []
        self.comments: dict[int, list[dict[str, Any]]] = {}

    def list_issues(self, *, label: str | None = "paper") -> list[dict[str, Any]]:
        self.calls.append(("list_issues", label))
        return deepcopy(self.issues)

    def ensure_label(
        self,
        name: str = "paper",
        *,
        color: str = "1d76db",
        description: str = "Paper reading queue",
    ) -> None:
        self.calls.append(("ensure_label", name, color, description))

    def create_issue(self, *, title: str, body: str) -> dict[str, Any]:
        number = len(self.issues) + 1
        issue = {
            "number": number,
            "node_id": f"ISSUE_{number}",
            "title": title,
            "body": body,
            "state": "open",
            "html_url": f"https://github.test/issues/{number}",
            "labels": [{"name": "paper"}, {"name": "AI-generated"}],
            "user": {"login": "github-actions[bot]", "type": "Bot"},
        }
        self.issues.append(issue)
        self.calls.append(("create_issue", title, body))
        return deepcopy(issue)

    def update_issue(
        self,
        number: int,
        *,
        title: str | None = None,
        body: str | None = None,
        state: str | None = None,
    ) -> dict[str, Any]:
        issue = next(issue for issue in self.issues if issue["number"] == number)
        if title is not None:
            issue["title"] = title
        if body is not None:
            issue["body"] = body
        if state is not None:
            issue["state"] = state
        self.calls.append(("update_issue", number, title, body, state))
        return deepcopy(issue)

    def list_comments(self, number: int) -> list[dict[str, Any]]:
        self.calls.append(("list_comments", number))
        return deepcopy(self.comments.get(number, []))

    def create_comment(self, number: int, body: str) -> dict[str, Any]:
        comment = {"body": body}
        self.comments.setdefault(number, []).append(comment)
        self.calls.append(("create_comment", number, body))
        return deepcopy(comment)

    def add_labels(self, number: int, labels: list[str]) -> None:
        issue = next(issue for issue in self.issues if issue["number"] == number)
        existing = {
            label.get("name", "") if isinstance(label, dict) else str(label)
            for label in issue.get("labels", [])
        }
        issue["labels"] = [{"name": name} for name in sorted(existing | set(labels))]
        self.calls.append(("add_labels", number, labels))


class GraphQLTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, str]]:
        assert method == "POST"
        assert json_body is not None
        self.calls.append(json_body)
        query = json_body["query"]
        if "query PaperbotProject(" in query:
            data = {
                "user": {
                    "projectV2": {
                        "id": "PROJECT",
                        "fields": {
                            "nodes": [
                                {
                                    "id": "FIELD",
                                    "name": "Relevance",
                                    "dataType": "NUMBER",
                                }
                            ]
                        },
                    }
                }
            }
        elif "query PaperbotProjectItem" in query:
            data = {"node": {"projectItems": {"nodes": []}}}
        elif "mutation PaperbotAddItem" in query:
            data = {"addProjectV2ItemById": {"item": {"id": "ITEM"}}}
        elif "mutation PaperbotSetRelevance" in query:
            data = {"updateProjectV2ItemFieldValue": {"projectV2Item": {"id": "ITEM"}}}
        else:  # pragma: no cover - makes unexpected GraphQL fail loudly
            raise AssertionError(query)
        return {"data": data}, {}


class RestTransport:
    def __init__(self, pages: dict[int, list[dict[str, Any]]]) -> None:
        self.pages = pages
        self.calls: list[str] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json_body: Any | None = None,
    ) -> tuple[Any, dict[str, str]]:
        self.calls.append(url)
        page = int(url.rsplit("page=", 1)[1])
        return deepcopy(self.pages[page]), {}


def paper_issue(
    paper: Paper,
    *,
    score: float = 0.7,
    model_hash: str = "model-v1",
    state: str = "open",
    prefix: str = "",
    suffix: str = "",
) -> dict[str, Any]:
    bibtex = "@article{Lovelace2026,\n  title = {A useful paper}\n}"
    meta = build_managed_meta(
        paper, score, bibtex, "Lovelace2026", model_hash=model_hash
    )
    body = render_managed_body(
        paper, score, bibtex, "Lovelace2026", meta=meta
    )
    return {
        "number": 4,
        "node_id": "ISSUE_4",
        "title": paper.title,
        "body": f"{prefix}{body}{suffix}",
        "state": state,
        "html_url": "https://github.test/issues/4",
        "labels": [{"name": "paper"}, {"name": "AI-generated"}],
        "user": {"login": "github-actions[bot]", "type": "Bot"},
    }


def test_reserve_bibtex_key_uses_b_then_c_case_insensitively() -> None:
    reserved = {"Lovelace2026", "Lovelace2026_B"}

    assert reserve_bibtex_key("Lovelace2026", reserved) == "Lovelace2026_C"
    assert reserve_bibtex_key("lovelace2026", reserved) == "lovelace2026_D"
    assert (
        reserve_bibtex_key(
            "Lovelace2026", reserved, aliases_for_same_work={"Lovelace2026"}
        )
        == "Lovelace2026"
    )


def test_identity_normalizes_doi_and_arxiv_revision() -> None:
    work_id, aliases = identity_for_record(Paper())

    assert work_id == "doi:10.1000/test"
    assert "arxiv:2501.00001" in aliases
    assert "pmid:12345" in aliases
    assert any(alias.startswith("title:") for alias in aliases)


def test_explicit_canonical_identity_is_always_a_hashed_alias() -> None:
    work_id, aliases = identity_for_record(
        {
            "canonical_id": "provider:Canonical-123",
            "source": "other-provider",
            "source_id": "source-456",
            "title": "A paper",
        }
    )

    assert work_id == "provider:canonical-123"
    assert work_id in aliases


def test_managed_metadata_rejects_boolean_schema_alias() -> None:
    with pytest.raises(GitHubError, match="unsupported metadata schema"):
        parse_managed_meta('<!-- paperbot:meta {"schema":true} -->')


def test_identity_and_metadata_are_compatible_with_canonical_paper_record() -> None:
    record = PaperRecord(
        source="bioRxiv",
        source_id="10.1101/2026.01.02.123456v2",
        title="Canonical record",
        abstract="Abstract",
        authors=("Lovelace, Ada",),
        created_at=datetime(2026, 1, 2, tzinfo=UTC),
        updated_at=datetime(2026, 1, 3, tzinfo=UTC),
        doi="10.1101/2026.01.02.123456",
        version="2",
        related_ids=("pmid:98765", "arxiv:2501.00001v3"),
    )

    work_id, aliases = identity_for_record(record)
    meta = build_managed_meta(
        record, 0.5, "@article{Lovelace2026}", "Lovelace2026"
    )

    assert work_id == record.canonical_id
    assert set(aliases) == set(record.identity_aliases())
    assert "biorxiv:10.1101/2026.01.02.123456v2" in aliases
    assert "source:biorxiv:10.1101/2026.01.02.123456v2" not in aliases
    assert meta["updated"] == "2026-01-03T00:00:00+00:00"


def test_managed_block_preserves_user_text_and_bibtex_backslashes() -> None:
    paper = Paper()
    old = paper_issue(paper, prefix="My notes\n\n", suffix="\n\nMore notes")["body"]
    bibtex = "@article{Lovelace2026, title={X}, note={\\url{https://x.test}}}"
    new = render_managed_body(paper, 0.8, bibtex, "Lovelace2026")

    replaced = replace_managed_block(old, new)

    assert replaced.startswith("My notes\n\n")
    assert replaced.endswith("\n\nMore notes")
    assert "\\url{https://x.test}" in replaced
    assert parse_managed_meta(replaced)["score"] == 0.8


@pytest.mark.parametrize("score", [0.0, 0.8])
def test_new_issue_requires_strictly_greater_than_cutoff(score: float) -> None:
    client = MemoryIssueClient()

    result = upsert_paper_issue(
        client,
        Paper(),
        score,
        "@article{Lovelace2026}",
        "Lovelace2026",
        model_hash="model",
    )

    assert result.action == "skipped"
    assert not any(call[0] == "create_issue" for call in client.calls)


def test_new_issue_is_labeled_and_contains_copyable_bibtex() -> None:
    client = MemoryIssueClient()

    result = upsert_paper_issue(
        client,
        Paper(),
        0.801,
        "@article{Lovelace2026}",
        "Lovelace2026",
        model_hash="model",
    )

    assert result.action == "created"
    assert any(call[:2] == ("ensure_label", "paper") for call in client.calls)
    assert any(call[:2] == ("ensure_label", "AI-generated") for call in client.calls)
    assert "```bibtex\n@article{Lovelace2026}\n```" in result.issue.body
    assert result.issue.title == "A useful paper"
    assert result.issue.labels == frozenset({"paper", "AI-generated"})
    assert "**Authors:** Ada Lovelace" in result.issue.body
    assert "**Venue:** bioRxiv" in result.issue.body
    assert "**Date:** 2026-07-20" in result.issue.body
    assert result.issue.body.index("**Authors:**") < result.issue.body.index("## Abstract")
    assert result.issue.body.index("**Venue:**") < result.issue.body.index("## Abstract")
    assert result.issue.body.index("**Date:**") < result.issue.body.index("## Abstract")


def test_revision_updates_managed_block_comments_once_and_reopens() -> None:
    original = Paper(version="v1", updated="2026-07-21", abstract="Old abstract")
    client = MemoryIssueClient(
        [
            paper_issue(
                original,
                state="closed",
                prefix="Personal finding\n\n",
                suffix="\n\nDo not overwrite",
            )
        ]
    )
    revised = Paper(version="v2", abstract="Revised abstract")

    result = upsert_paper_issue(
        client,
        revised,
        0.2,
        "@article{Lovelace2026,\n  title = {A useful paper}\n}",
        "Lovelace2026",
        model_hash="model-v1",
    )

    assert result.action == "updated"
    assert result.substantive_change
    assert client.issues[0]["state"] == "open"
    assert client.issues[0]["body"].startswith("Personal finding\n\n")
    assert client.issues[0]["body"].endswith("\n\nDo not overwrite")
    assert len(client.comments[4]) == 1
    assert "abstract, version" in client.comments[4][0]["body"]

    repeated = upsert_paper_issue(
        client,
        revised,
        0.2,
        "@article{Lovelace2026,\n  title = {A useful paper}\n}",
        "Lovelace2026",
        model_hash="model-v1",
    )
    assert repeated.action == "unchanged"
    assert len(client.comments[4]) == 1


def test_score_only_change_is_silent_and_does_not_reopen() -> None:
    client = MemoryIssueClient([paper_issue(Paper(), state="closed")])

    result = upsert_paper_issue(
        client,
        Paper(),
        0.8,
        "@article{Lovelace2026,\n  title = {A useful paper}\n}",
        "Lovelace2026",
        model_hash="model-v2",
    )

    assert result.action == "rescored"
    assert client.issues[0]["state"] == "closed"
    assert client.comments == {}


def test_unchanged_managed_issue_gets_missing_paper_label_back() -> None:
    issue = paper_issue(Paper())
    issue["labels"] = [{"name": "research"}]
    client = MemoryIssueClient([issue])

    result = upsert_paper_issue(
        client,
        Paper(),
        0.7,
        "@article{Lovelace2026,\n  title = {A useful paper}\n}",
        "Lovelace2026",
        model_hash="model-v1",
    )

    assert result.action == "relabeled"
    assert ("add_labels", 4, ["paper", "AI-generated"]) in client.calls
    assert not any(call[0] == "update_issue" for call in client.calls)


def test_load_managed_issues_paginates_and_ignores_unmanaged_and_prs() -> None:
    managed = paper_issue(Paper())
    filler = [{"number": index, "body": "ordinary"} for index in range(1, 100)]
    transport = RestTransport(
        {
            1: [managed, *filler],
            2: [
                {"number": 101, "body": "ordinary"},
                {"number": 102, "body": "ordinary", "pull_request": {}},
            ],
        }
    )
    client = GitHubClient("delalamo/SKM", "token", transport=transport)

    index = load_managed_issues(client)

    assert [issue.number for issue in index.issues] == [4]
    assert len(transport.calls) == 2
    assert all("sort=created" in url for url in transport.calls)
    assert all("direction=asc" in url for url in transport.calls)


def test_read_only_client_can_use_public_github_without_a_token() -> None:
    transport = RestTransport({1: []})
    client = GitHubClient("delalamo/SKM", "", transport=transport)

    assert client.list_issues(label=None) == []
    assert "Authorization" not in client._headers

    with pytest.raises(GitHubError, match="token is required"):
        client.create_issue(title="Cannot publish", body="without credentials")


def test_public_issue_reads_need_no_token_but_mutations_do() -> None:
    transport = RestTransport({1: []})
    client = GitHubClient("delalamo/SKM", "", transport=transport)

    assert client.list_issues() == []
    with pytest.raises(GitHubError, match="token is required"):
        client.create_issue(title="No", body="No")


def test_alias_collision_between_distinct_works_fails_closed() -> None:
    first = paper_issue(Paper())
    second = paper_issue(
        Paper(
            doi="10.1000/other",
            pmid="67890",
            arxiv_id="2501.99999",
            source_id="10.1000/other",
            aliases=("doi:10.1000/test",),
        )
    )
    second["number"] = 5
    second["node_id"] = "ISSUE_5"
    client = MemoryIssueClient([first, second])

    with pytest.raises(GitHubError, match="belongs to both"):
        load_managed_issues(client)


@pytest.mark.parametrize(
    "corrupt",
    [
        lambda body: body + "\n<!-- paperbot:meta {not-json} -->",
        lambda body: body + "\n" + body,
        lambda body: body.replace("<!-- paperbot:managed:end -->", ""),
    ],
)
def test_bot_authored_malformed_managed_body_fails_before_deduplication(
    corrupt: Any,
) -> None:
    issue = paper_issue(Paper())
    issue["body"] = corrupt(issue["body"])

    with pytest.raises(GitHubError, match="metadata marker|complete paperbot block"):
        load_managed_issues(MemoryIssueClient([issue]))


def test_repository_owner_managed_issue_prevents_duplicate_creation() -> None:
    legacy = paper_issue(Paper())
    legacy["user"] = {"login": "delalamo", "type": "User"}
    client = MemoryIssueClient([legacy])

    index = load_managed_issues(client)
    result = upsert_paper_issue(
        client,
        Paper(),
        0.7,
        "@article{Lovelace2026,\n  title = {A useful paper}\n}",
        "Lovelace2026",
        index=index,
        model_hash="model-v1",
    )

    assert index.find(Paper()).number == 4
    assert result.action == "unchanged"
    assert not any(call[0] == "create_issue" for call in client.calls)


def test_exact_duplicate_work_keeps_oldest_issue_canonical() -> None:
    legacy = paper_issue(Paper())
    legacy["user"] = {"login": "delalamo", "type": "User"}
    duplicate = deepcopy(legacy)
    duplicate["number"] = 5
    duplicate["node_id"] = "ISSUE_5"
    duplicate["user"] = {"login": "github-actions[bot]", "type": "Bot"}
    client = MemoryIssueClient([duplicate, legacy])

    index = load_managed_issues(client)

    assert [issue.number for issue in index.issues] == [4]
    assert [issue.number for issue in index.duplicates] == [5]
    assert index.find(Paper()).number == 4


def test_user_authored_marker_cannot_claim_aliases_or_be_mutated() -> None:
    spoofed = paper_issue(Paper(), state="closed")
    spoofed["user"] = {"login": "untrusted-reader", "type": "User"}
    malformed = {
        "number": 5,
        "node_id": "ISSUE_5",
        "title": "Malformed spoof",
        "body": "<!-- paperbot:meta {not-json} -->",
        "state": "open",
        "html_url": "https://github.test/issues/5",
        "labels": [{"name": "paper"}],
        "user": {"login": "another-reader", "type": "User"},
    }
    client = MemoryIssueClient([spoofed, malformed])

    index = load_managed_issues(client)
    assert index.issues == []
    assert index.find(Paper()) is None
    result = upsert_paper_issue(
        client,
        Paper(),
        0.9,
        "@article{Lovelace2026}",
        "Lovelace2026",
        index=index,
        model_hash="model",
    )

    assert result.action == "created"
    assert result.issue.number == 3
    assert client.issues[0] == spoofed
    assert not any(
        call[0] in {"update_issue", "create_comment", "add_labels"}
        and len(call) > 1
        and call[1] in {4, 5}
        for call in client.calls
    )


def test_project_sync_adds_item_then_sets_numeric_relevance() -> None:
    transport = GraphQLTransport()
    project = ProjectClient(
        "projects-token",
        "delalamo",
        7,
        relevance_field="Relevance",
        transport=transport,
    )

    item_id = project.sync("ISSUE_NODE", 0.875)

    assert item_id == "ITEM"
    assert len(transport.calls) == 4
    assert "includeArchived: true" in transport.calls[1]["query"]
    assert transport.calls[-1]["variables"] == {
        "project": "PROJECT",
        "item": "ITEM",
        "field": "FIELD",
        "score": 0.875,
    }


def test_rescore_updates_open_issue_without_comment_and_repairs_project() -> None:
    client = MemoryIssueClient([paper_issue(Paper(), model_hash="old")])

    class Project:
        def __init__(self) -> None:
            self.calls: list[tuple[str, float]] = []

        def sync(self, node_id: str, score: float) -> str:
            self.calls.append((node_id, score))
            return "ITEM"

    project = Project()
    results = rescore_managed_issues(
        client,
        lambda issue: 0.9123456,
        "new",
        project=project,
        index=load_managed_issues(client),
    )

    assert results[0].action == "rescored"
    assert "**Relevance:** 0.912346" in client.issues[0]["body"]
    assert client.comments == {}
    assert project.calls == [("ISSUE_4", 0.9123456)]


def test_reconcile_relables_and_syncs_closed_issue_without_rescoring() -> None:
    issue = paper_issue(Paper(), model_hash="old", state="closed")
    issue["labels"] = []
    client = MemoryIssueClient([issue])

    class Project:
        def __init__(self) -> None:
            self.calls: list[tuple[str, float]] = []

        def sync(self, node_id: str, score: float) -> str:
            self.calls.append((node_id, score))
            return "ITEM"

    project = Project()

    def should_not_score(issue: Any) -> float:  # pragma: no cover - failure path
        raise AssertionError("closed issues must not be rescored")

    results = rescore_managed_issues(
        client,
        should_not_score,
        "new",
        project=project,
        index=load_managed_issues(client),
    )

    assert results[0].action == "relabeled"
    assert ("add_labels", 4, ["paper", "AI-generated"]) in client.calls
    assert not any(call[0] == "update_issue" for call in client.calls)
    assert project.calls == [("ISSUE_4", 0.7)]


def test_discovery_workflow_keeps_project_token_in_the_queue_step_only() -> None:
    workflow = Path(".github/workflows/paper-discovery.yml").read_text(encoding="utf-8")

    assert 'cron: "0 0 * * *"' in workflow
    assert '"$GITHUB_EVENT_NAME" == "schedule"' in workflow
    assert 'date -u +%Y-%m-%dT00:00:00Z' in workflow
    assert "persist-credentials: false" in workflow
    assert workflow.count("secrets.PROJECTS_TOKEN") == 1
    assert "steps.project_queue.outputs.ready == 'true'" in workflow
    assert workflow.index("secrets.NCBI_API_KEY") < workflow.index(
        "secrets.PROJECTS_TOKEN"
    )
