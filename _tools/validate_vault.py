#!/usr/bin/env python3
"""Check every structural rule of the knowledge base (spec Appendix B).

Prints one line per problem as ``path:line RULE message`` and exits 1 when
there is any. The legacy zone (content/notes, content/tags, content/review)
is not checked, but knowledge-base notes may not link into it.

  python3 _tools/validate_vault.py
  python3 _tools/validate_vault.py --katex node_modules/katex
  python3 _tools/validate_vault.py --list-rules
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rules  # noqa: E402
from vaultlib import paths  # noqa: E402
from vaultlib.vault import Vault  # noqa: E402


def main(argv: list[str] | None = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("--vault", type=Path, default=paths.DEFAULT_VAULT)
  parser.add_argument("--bib", type=Path, default=paths.DEFAULT_BIB)
  parser.add_argument("--data", type=Path, default=paths.DEFAULT_DATA)
  parser.add_argument("--katex", help="path to the katex package (e.g. node_modules/katex) to check equations")
  parser.add_argument("--rule", action="append", help="run only this rule (repeatable)")
  parser.add_argument("--json", action="store_true", help="print problems as JSON")
  parser.add_argument("--list-rules", action="store_true")
  args = parser.parse_args(argv)

  if args.list_rules:
    for rule_obj in rules.load_all().values():
      print(f"{rule_obj.id:24} {rule_obj.scope:9} {rule_obj.description}")
    return 0

  vault = Vault(args.vault, args.bib, args.data)
  problems = rules.run(vault, katex=args.katex, only=args.rule)
  if args.json:
    print(json.dumps([problem.__dict__ for problem in problems], indent=1))
  else:
    for problem in problems:
      print(problem)
    checked = len(vault.kb_notes())
    print(f"{len(problems)} errors in {checked} knowledge-base notes")
  return 1 if problems else 0


if __name__ == "__main__":
  sys.exit(main())
