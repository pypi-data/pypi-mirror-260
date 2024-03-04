import enum
import typing as t

from . import formats
from .recipe import Recipe


class Format(enum.Enum):
    YAML = enum.auto()
    MARKDOWN = enum.auto()


# function which takes a recipe and serializes it to some string format
SerializerFunc = t.Callable[[Recipe], str]


class RecipeSerializer:
    """
    RecipeSerializer.serialize(recipe, fmt=Format.MARKDOWN)
    """

    _handlers: dict[Format, SerializerFunc] = {}

    def serialize(self, recipe: Recipe, fmt: Format) -> str:
        handler = self._get_handler(fmt)
        result = handler(recipe)
        return result

    def _get_handler(self, fmt: Format) -> t.Callable:
        return self._handlers[fmt]

    @classmethod
    def register(cls, fmt: Format, handler: SerializerFunc):
        cls._handlers[fmt] = handler


RecipeSerializer.register(Format.YAML, formats.serialize_yaml)
RecipeSerializer.register(Format.MARKDOWN, formats.serialize_markdown)
