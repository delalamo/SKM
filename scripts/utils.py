from pathlib import Path


def find_repo_root(marker: str = "quartz.config.ts") -> Path:
    """
    Walk up from this file's location until a directory containing `marker`
    is found. Raises RuntimeError if the repo root cannot be located.
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / marker).exists():
            return parent
    raise RuntimeError(
        f"Could not find repo root (looked for '{marker}' in parents of {__file__})"
    )


REPO_ROOT = find_repo_root()
