from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    amount: int | float = 0
    unit: str = ""
    prep: str = ""

    @classmethod
    def from_str(cls, s: str) -> "Ingredient":
        """
        :raises: ParseIngredientError
        """
        return Ingredient(**parse_ingredient_str(s))

    def __str__(self):
        match [self.name, self.amount, self.unit]:
            case [name, 0, ""]:
                result = f"{name}"
            case [name, amount, ""]:
                result = f"{amount} {name}"
            case [name, amount, unit]:
                result = f"{amount} {unit} {name}"
            case _:
                raise RuntimeError("unreachable")

        if self.prep:
            result += f", {self.prep}"

        return result

    def to_yaml_str(self):
        match [self.name, self.amount, self.unit]:
            case [name, 0, ""]:
                result = f"{name}"
            case [name, amount, ""]:
                result = f"{amount}, {name}"
            case [name, amount, unit]:
                result = f"{amount}, {unit}, {name}"
            case _:
                raise RuntimeError("unreachable")

        if self.prep:
            result += f"; {self.prep}"

        return result


def parse_ingredient_str(s: str) -> dict:
    """
    :param s: examples:
                name only:                    "apple"
                amount and name:              "1, apple"
                amount, unit and name:        "1, kg, apples"
                amount, unit, name, and prep: "1, kg, apples; chopped"
    :return:
    :raises: IngredientParseError
    """
    output = {}

    match list(map(str.strip, s.split(";"))):
        case [""]:
            raise ParseIngredientError("empty input")
        case [s]:
            pass
        case [s, ""]:  # trailing ";" and empty prep
            pass
        case [s, prep]:  # non-empty prep
            output["prep"] = prep
        case _:
            raise ParseIngredientError(f"Too many semicolons: {s}")

    match list(map(str.strip, s.split(","))):
        case [""]:
            raise ParseIngredientError("Got prep but no ingredients")
        case [amount, name]:  # e.g. 1, apple
            if not name:
                raise ParseIngredientError("empty value: name")
            if not amount:
                raise ParseIngredientError("empty value: amount")
            output["name"] = name
            output["amount"] = _parse_number(amount)
        case [amount, unit, name]:  # e,g. 1, kg, apples
            output["name"] = name
            output["amount"] = _parse_number(amount)
            output["unit"] = unit
        case [name]:
            output["name"] = name
        case _:
            raise ParseIngredientError(f"Too many commas: {s}")

    return output


class ParseIngredientError(Exception):
    pass


def _parse_number(number: str) -> int | float:
    """
    :raises: IngredientParseError if invalid number
    """
    if not number.strip():
        return 0

    try:
        result = float(number)
    except ValueError:
        raise ParseIngredientError(f"invalid number: {number!r}")
    else:
        if result % 1 == 0:
            return int(result)
        else:
            return result
