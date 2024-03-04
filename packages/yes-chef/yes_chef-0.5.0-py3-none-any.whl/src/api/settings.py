from pathlib import Path

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

from . import utils

BASE = Path.home() / ".sous-chef"
GLOBAL_SETTINGS_FILE = BASE / "settings.json"


class Settings(BaseSettings):
    recipe_library: Path = Field(BASE / "recipes")
    plans_dir: Path = Field(BASE / "plans")

    def save(self) -> None:
        utils.touch(GLOBAL_SETTINGS_FILE)
        with open(GLOBAL_SETTINGS_FILE, "w") as file:
            file.write(self.model_dump_json())

    @classmethod
    def from_file(cls) -> "Settings":
        try:
            with open(GLOBAL_SETTINGS_FILE) as file:
                json_str = file.read()
                return cls.model_validate_json(json_str)

        except (FileNotFoundError, ValidationError):
            return cls()  # defaults
