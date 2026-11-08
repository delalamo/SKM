"""Validator rule registry.

Each rule is a function ``(vault) -> Iterable[Problem]`` registered with a
stable ID. Every registered rule must have at least one mutation test in
``_tools/tests/test_rule_mutations.py`` that breaks the fixture vault and
sees the rule fire (spec section 11.3).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class Problem:
  rule: str
  path: str
  line: int
  message: str

  def __str__(self) -> str:
    return f"{self.path}:{self.line} {self.rule} {self.message}"


@dataclass(frozen=True)
class Rule:
  id: str
  scope: str
  description: str
  fn: Callable
  needs_katex: bool = False


RULES: dict[str, Rule] = {}


def rule(rule_id: str, scope: str, description: str, needs_katex: bool = False):
  def register(fn):
    if rule_id in RULES:
      raise ValueError(f"duplicate rule {rule_id}")
    RULES[rule_id] = Rule(rule_id, scope, description, fn, needs_katex)
    return fn

  return register


def load_all() -> dict[str, Rule]:
  from . import common, papers, claims, others  # noqa: F401  (registration side effects)

  return RULES


def run(vault, katex: str | None = None, only: Iterable[str] | None = None) -> list[Problem]:
  problems: list[Problem] = []
  wanted = set(only) if only else None
  for rule_obj in load_all().values():
    if wanted is not None and rule_obj.id not in wanted:
      continue
    if rule_obj.needs_katex:
      if not katex:
        continue
      found = rule_obj.fn(vault, katex)
    else:
      found = rule_obj.fn(vault)
    for problem in found:
      problems.append(Problem(rule_obj.id, problem[0], problem[1], problem[2]))
  problems.sort(key=lambda p: (p.path, p.line, p.rule, p.message))
  return problems
