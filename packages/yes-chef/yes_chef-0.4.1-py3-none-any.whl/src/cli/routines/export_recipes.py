import asyncio
from pathlib import Path

import aiofiles

from ...api import Recipe, RecipeSerializer
from ...api import Settings
from ...api.recipe.serializer import Format
from ...api.utils import clean_filename


async def export_recipes():
    settings = Settings.from_file()
    markdown_folder = settings.recipe_library / "md"  # todo: dedupe this
    recipes = await Recipe.load_all()
    print(f"loaded {len(recipes)} recipes")
    await asyncio.gather(
        *(_serialize(recipe, markdown_folder) for recipe in recipes)
    )


async def _serialize(recipe: Recipe, dest_dir: Path):
    stringified = recipe.name.replace(" ", "-")  # TODO: handle other punct
    filename = clean_filename(dest_dir / f"{stringified}.md")
    serialized = RecipeSerializer().serialize(recipe, Format.MARKDOWN)
    async with aiofiles.open(filename, "w") as file:
        await file.write(serialized)
