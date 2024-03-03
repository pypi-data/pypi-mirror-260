import asyncio
from pathlib import Path

import aiofiles
import yaml
from pydantic import BaseModel, Field

from .utils import preprocess_yaml
from ..ingredient import Ingredient
from ..settings import Settings


class Recipe(BaseModel):
    # metadata
    name: str
    author: str = ""
    prep_minutes: int = 0
    cook_minutes: int = 0
    servings: int = 0
    source: str = ""
    image: str = ""
    notes: str = ""

    # child objects
    ingredients: list[Ingredient] = Field()

    # for something like a salsa or a spice mix, the "method" is just:
    # combine all the ingredients. So method should not be mandatory.
    method: list[str] = []
    equipment: list[str] = []

    def __str__(self):
        return f"{self.name} by {self.author}"

    @staticmethod
    def search(query: str, recipes: list["Recipe"]) -> list["Recipe"]:
        """
        :param query: Could be anything -- ingredient, title fragment, author
        :param recipes: the recipes to search
        :return: list of recipes that match the given query term
        """
        # todo: improve this function. Should be able to search specifically for
        #  author, or ingredient. Should be able to pass via flags e.g.
        #       -a --author Robin Neville
        #       -i --ingredient lentils
        #       -e --equipment air fryer
        #       -x --exclude (flips the above logic as if applying `not` to the
        #                     whole query)

        if not query or not recipes:
            return []

        return [
            recipe
            for recipe in recipes
            if any(
                needle.lower() in haystack.lower()
                for needle in query.split()
                for haystack in [recipe.name, recipe.author]
            )
        ]

    @classmethod
    async def load_all(cls) -> list["Recipe"]:
        """
        Load all the recipes from yaml
        """
        settings = Settings.from_file()
        # todo: de-dupe these paths
        filenames = settings.recipe_library.joinpath("yaml").glob("*.yaml")
        return list(await asyncio.gather(*(cls.load(f) for f in filenames)))

    @classmethod
    async def load(cls, filename: Path) -> "Recipe":
        """
        Load from yaml
        """
        async with aiofiles.open(filename) as file:
            recipe_str = await file.read()
            recipe_dict = yaml.safe_load(recipe_str)
            recipe_dict = preprocess_yaml(recipe_dict)
            return Recipe(**recipe_dict)
