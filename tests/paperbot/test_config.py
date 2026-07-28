from __future__ import annotations

from pathlib import Path

import pytest

from scripts.paperbot.config import load_config


def _write_config(root: Path, paths: str = "") -> Path:
  config = root / "paperbot.toml"
  path_lines = paths or 'bibliography = "bibliography.bib"'
  config.write_text(
    'repository = "delalamo/SKM"\n'
    "[paths]\n"
    f"{path_lines}\n",
    encoding="utf-8",
  )
  return config


def test_confined_config_resolves_data_inside_repository(tmp_path: Path) -> None:
  config_path = _write_config(
    tmp_path,
    'bibliography = "data/library.bib"\n'
    'artifacts = "generated/model"\n'
    'abstract_exceptions = "generated/exceptions.json"',
  )

  config = load_config(config_path, repository_root=tmp_path)

  assert config.bibliography_path == tmp_path / "data/library.bib"
  assert config.artifact_dir == tmp_path / "generated/model"
  assert config.abstract_exceptions_path == tmp_path / "generated/exceptions.json"


def test_confined_config_must_exist_as_a_regular_file(tmp_path: Path) -> None:
  with pytest.raises(ValueError, match="regular, non-symlink"):
    load_config(tmp_path / "paperbot.toml", repository_root=tmp_path)

  target = _write_config(tmp_path)
  link = tmp_path / "linked.toml"
  link.symlink_to(target)
  with pytest.raises(ValueError, match="regular, non-symlink"):
    load_config(link, repository_root=tmp_path)


@pytest.mark.parametrize(
  "path_value",
  [
    "../outside.bib",
    "/tmp/outside.bib",
  ],
)
def test_confined_config_rejects_data_path_escape(
  tmp_path: Path,
  path_value: str,
) -> None:
  config_path = _write_config(
    tmp_path,
    f'bibliography = "{path_value}"',
  )

  with pytest.raises(ValueError, match="escapes repository root"):
    load_config(config_path, repository_root=tmp_path)


def test_confined_config_itself_must_be_inside_repository(tmp_path: Path) -> None:
  repository = tmp_path / "repository"
  repository.mkdir()
  outside = tmp_path / "outside"
  outside.mkdir()
  config_path = _write_config(outside)

  with pytest.raises(ValueError, match="config must be inside"):
    load_config(config_path, repository_root=repository)


def test_confined_config_rejects_symlinked_data_parent(
  tmp_path: Path,
) -> None:
  repository = tmp_path / "repository"
  repository.mkdir()
  outside = tmp_path / "outside"
  outside.mkdir()
  (repository / "linked").symlink_to(outside, target_is_directory=True)
  config_path = _write_config(
    repository,
    'bibliography = "linked/bibliography.bib"',
  )

  with pytest.raises(ValueError, match="escapes repository root"):
    load_config(config_path, repository_root=repository)
