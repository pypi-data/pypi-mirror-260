import yaml

from .recipe import Recipe


def serialize_yaml(recipe: Recipe) -> str:
    recipe_dict = recipe.model_dump()
    recipe_dict = {key: value for key, value in recipe_dict.items() if value}
    # make sure the ingredients are displayed in their yaml format
    recipe_dict["ingredients"] = [
        ing.to_yaml_str() for ing in recipe.ingredients
    ]
    return yaml.safe_dump(recipe_dict)


def serialize_json(recipe: Recipe) -> str:
    return recipe.model_dump_json()


def serialize_markdown(recipe: Recipe) -> str:
    strings = []

    title_block = f"# {recipe.name}"
    if recipe.image:
        title_block += f"\n![](../images/{recipe.image})"
    title_block += f"\n\nAuthor: {recipe.author.title()}"
    strings.append(title_block)

    if recipe.source:
        strings.append(f"From: {recipe.source}")
    if recipe.servings:
        strings.append(f"Servings: {recipe.servings}")
    if recipe.prep_minutes:
        strings.append(f"Preparation: {recipe.prep_minutes} minutes")
    if recipe.cook_minutes:
        strings.append(f"Cooking: {recipe.cook_minutes} minutes")
    if recipe.notes:
        strings.append(f"Notes: {recipe.notes}")

    if recipe.equipment:
        equipment_str = "## Equipment: "
        for item in recipe.equipment:
            equipment_str += f"\n- {item}"
        strings.append(equipment_str)

    ingredients_str = "## Ingredients:"
    for ing in recipe.ingredients:
        ingredients_str += f"\n- [ ] {ing}"
    strings.append(ingredients_str)

    if recipe.method:
        method_str = "## Method:"
        for ii, step in enumerate(recipe.method, start=1):
            method_str += f"\n{ii}. {step}"
        strings.append(method_str)

    return "\n\n".join(strings)
