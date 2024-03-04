import typer
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from ...api import Plan
from ...api.recipe import Recipe
from ..utils import multiple_choice_menu


async def plan_recipe(query: str):
    plan = Plan.current()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        transient=True,  # will disappear on complete
    ) as progress:
        progress.add_task("loading recipes")
        all_recipes = await Recipe.load_all()

    matches = Recipe.search(query=query, recipes=all_recipes)

    match len(matches):
        case 0:
            typer.secho(f"Couldn't find any recipes for {query}")
            return
        case 1:
            # if there's only one match, don't bother prompting the user
            recipe = matches[0]
        case _:
            # todo: allow Ctrl+C and abort gracefullys
            recipe = multiple_choice_menu(
                prompt="Which recipe did you mean?",
                choices={r.name: r for r in matches},
            )

    plan.add(recipe)
    plan.save()
    typer.secho(f"Added {recipe} to plan. Plan is now: ")
    typer.secho(f"{plan}")
