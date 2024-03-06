from pathlib import Path


def ensure_folder(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
