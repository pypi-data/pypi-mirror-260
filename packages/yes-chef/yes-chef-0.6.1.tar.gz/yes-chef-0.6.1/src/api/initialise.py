from pathlib import Path


def init_library(path: Path):
    for p in [
        path,
        path / "yaml",
        path / "md",
        path / ".chef",
    ]:
        p.mkdir(parents=True, exist_ok=True)  # ensure the dir exists
