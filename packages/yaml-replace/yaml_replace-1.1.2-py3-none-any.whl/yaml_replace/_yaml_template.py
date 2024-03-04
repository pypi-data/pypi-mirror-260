import yaml
from typing import Any
from jinja2 import Template
from ._utils import quote, dquote

NONE = "__NONE__"


class YAMLTemplate:
    def __init__(self, yaml_string: str):
        self.yaml_string = yaml_string
        self.template = Template(
            yaml_string,
            variable_start_string="${{",
            variable_end_string="}}",
        )

    def _format_substitutions(self, value: Any) -> Any:
        # Recursively format the substitutions
        if isinstance(value, dict):
            return {k: self._format_substitutions(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._format_substitutions(v) for v in value]

        # If the value is None, return "NONE".
        # We'll substitute this with "null" later
        if value is None:
            return NONE

        # Else, return the value as is
        return value

    def render(self, substitutions: dict) -> dict:
        # Format the substitutions
        substitutions = self._format_substitutions(substitutions)

        # Render the template and replace "NONE" with "null"
        rendered_string = (
            self.template.render(substitutions)
            .replace(quote(NONE), "null")
            .replace(dquote(NONE), "null")
            .replace(NONE, "null")
        )

        # Parse the rendered string
        return yaml.safe_load(rendered_string)

    @staticmethod
    def from_file(file_path: str):
        with open(file_path, "r") as file:
            return YAMLTemplate(file.read())
