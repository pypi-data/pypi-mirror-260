import string
from pathlib import Path


def touch(file: Path):
    file.parent.mkdir(exist_ok=True, parents=True)
    file.touch(exist_ok=True)


def clean_filename(original: Path) -> Path:
    """
    Strip spaces and punctuation out of the filename and replace them with
    hyphens.

    :param original: E.g. "some/folder/my bad file.txt"
    :return: the cleaned filename e.g. "some/folder/my-bad-file.txt"
    """
    mapping = {
        " ": "-",
        "_": "-",
        ".": "-",
    }
    stem = original.stem.lower()
    allowed = string.ascii_letters + string.digits + "-"
    cleaned = "".join(
        char if char in allowed else mapping.get(char, "") for char in stem
    )
    out = original.parent / f"{cleaned}{original.suffix}"
    return out
