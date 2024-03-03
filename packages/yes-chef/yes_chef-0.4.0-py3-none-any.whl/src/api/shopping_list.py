from pydantic import BaseModel, Field

from .recipe import Recipe

Amount = int | float
Unit = str
IngredientName = str
RecipeName = str


class Amounts(BaseModel):
    # from "apples" -> display as "enough for x"
    enough_for: list[RecipeName] = []

    # from "4 apples"
    unitless: Amount = 0

    # from "4 kg apples"
    units: dict[Unit, Amount] = Field(default_factory=dict)


ShoppingList = dict[IngredientName, Amounts]


example = ShoppingList(
    apples=Amounts(
        enough_for=["apple pie"],
        unitless=4,
        units=dict(kg=4),
    ),
    potatoes=Amounts(units=dict(kg=5)),
)


def merge_recipes(recipes: list[Recipe]) -> ShoppingList:
    """
    This is the magic.
    :param recipes:
    :return:
    """
    shopping_list = {}
    for recipe in recipes:
        for ing in recipe.ingredients:
            amounts = shopping_list.get(ing.name, Amounts())
            match [ing.amount, ing.unit]:
                case [0, ""]:
                    amounts.enough_for.append(recipe.name)
                case [amount, ""]:
                    amounts.unitless += amount
                case [amount, unit]:
                    amounts.units[unit] = amounts.units.get(unit, 0) + amount
            shopping_list[ing.name] = amounts

    return shopping_list
