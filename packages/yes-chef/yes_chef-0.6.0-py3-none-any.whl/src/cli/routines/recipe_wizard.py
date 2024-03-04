from pathlib import Path
from typing import Any

from src.api import Recipe, RecipeSerializer, Settings
from src.api.ingredient import ParseIngredientError, Ingredient
from src.api.recipe.serializer import Format
from src.api.utils import clean_filename


def recipe_wizard() -> Recipe:
    """
    Interactively guide the user through creating a new recipe
    """
    name = prompt("name")
    author = prompt("author")

    print("Ingredients:")
    print("format: [amount, [unit,]] name [; prep]")
    ingredients = []
    while ing_str := prompt("enter an ingredient [leave blank to finish]"):
        try:
            ingredient = Ingredient.from_str(ing_str)
        except ParseIngredientError as e:
            print(e)
            continue
        else:
            ingredients.append(ingredient)

    print("Method:")
    method = []
    while method_str := prompt("enter a method step [leave blank to finish]"):
        method.append(method_str)

    print("Equipment:")
    equipment = []
    while equipment_str := prompt(
        "what equipment do you need? [leave blank to finish]"
    ):
        equipment.append(equipment_str)

    recipe = Recipe(
        name=name,
        author=author,
        ingredients=ingredients,
        method=method,
        equipment=equipment,
        prep_minutes=prompt("prep_minutes", default=0, expected_type=int),
        cook_minutes=prompt("cook_minutes", default=0, expected_type=int),
        servings=prompt("servings", default=0, expected_type=int),
        source=prompt("source (url or book name)"),
        image=prompt("image (url or local image)"),
        notes=prompt("notes"),
    )
    return recipe


NOT_SET = object()


def prompt(name: str, default: Any = NOT_SET, expected_type: type = str) -> Any:
    s = f"{name}"
    if expected_type != str:
        s += f" ({expected_type.__name__})"
    if default is not NOT_SET:
        s += f" [{default}]"
    s += ": "

    while True:
        raw = input(s)
        if not raw:
            if default is NOT_SET:
                return expected_type()
            else:
                return default

        try:
            parsed = expected_type(raw)
        except Exception as e:
            print(e)
        else:
            return parsed
