import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR.parent / "generated"
SCHEMA_PATH = BASE_DIR.parent / "interface" / "interface.json"

TYPE_MAP = {
    "uint8": "B",
    "uint16": "H",
    "int32": "i",
    "float": "f",
    "double": "d",
}


def load_schema(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as token:
        return json.load(token)


def validate_schema(schema: dict) -> None:
    if "types" not in schema or not isinstance(schema["types"], list):
        raise ValueError("Schema must contain a 'types' list.")

    for type_index, type_def in enumerate(schema["types"]):
        if "name" not in type_def or not type_def["name"]:
            raise ValueError(f"types[{type_index}] is missing a valid 'name'.")

        fields = type_def.get("fields", [])
        if not isinstance(fields, list):
            raise ValueError(f"types[{type_index}].fields must be a list.")

        for field_index, field in enumerate(fields):
            if "name" not in field or not field["name"]:
                raise ValueError(f"types[{type_index}].fields[{field_index}] is missing a valid 'name'.")
            if "type" not in field or not field["type"]:
                raise ValueError(f"types[{type_index}].fields[{field_index}] is missing a valid 'type'.")


def render_schema(schema: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape([]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("serializer.py.j2")
    return template.render(types=schema["types"], type_map=TYPE_MAP)


def write_output(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as token:
        token.write(text)


if __name__ == "__main__":
    schema = load_schema(SCHEMA_PATH)
    validate_schema(schema)
    output = render_schema(schema)
    output_path = OUTPUT_DIR / "serializers.py"
    write_output(output, output_path)
    print(f"Generated {output_path}")
