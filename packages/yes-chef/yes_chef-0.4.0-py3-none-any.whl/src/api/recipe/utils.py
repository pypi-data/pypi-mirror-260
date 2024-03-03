from ..ingredient import parse_ingredient_str


def preprocess_yaml(yaml_dict: dict) -> dict:
    """
    Convert all the ingredient strings into ingredient dicts, so that we can
    pass the result to pydantic models.

    :param yaml_dict: YAML recipe loaded into dict form
    :raises: ParseIngredientError
    """
    if "ingredients" in yaml_dict:
        yaml_dict["ingredients"] = list(
            map(parse_ingredient_str, yaml_dict["ingredients"])
        )
    return yaml_dict
