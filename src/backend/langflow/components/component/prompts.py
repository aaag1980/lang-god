from typing import Optional

from langchain.agents.mrkl import prompt

from langflow.components.component.constants import (
    DEFAULT_PROMPT,
    HUMAN_PROMPT,
    SYSTEM_PROMPT,
)
from langflow.components.field.base import TemplateField
from langflow.components.component.base import Component
from langflow.components.template.base import Template


class PromptComponent(Component):
    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        # if field.field_type  == "StringPromptTemplate"
        # change it to str
        PROMPT_FIELDS = [
            "template",
            "suffix",
            "prefix",
            "examples",
            "format_instructions",
        ]
        if field.field_type == "StringPromptTemplate" and "Message" in str(name):
            field.field_type = "prompt"
            field.multiline = True
            field.value = HUMAN_PROMPT if "Human" in field.name else SYSTEM_PROMPT
        if field.name == "template" and field.value == "":
            field.value = DEFAULT_PROMPT

        if field.name in PROMPT_FIELDS:
            field.field_type = "prompt"
            field.advanced = False

        if (
            "Union" in field.field_type
            and "BaseMessagePromptTemplate" in field.field_type
        ):
            field.field_type = "BaseMessagePromptTemplate"

        # All prompt fields should be password=False
        field.password = False


class PromptTemplateNode(Component):
    name: str = "PromptTemplate"
    template: Template
    description: str
    base_classes: list[str] = ["BasePromptTemplate"]

    def to_dict(self):
        return super().to_dict()

    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        Component.format_field(field, name)
        if field.name == "examples":
            field.advanced = False


class BasePromptComponent(Component):
    name: str
    template: Template
    description: str
    base_classes: list[str]

    def to_dict(self):
        return super().to_dict()


class ZeroShotPromptNode(BasePromptComponent):
    name: str = "ZeroShotPrompt"
    template: Template = Template(
        type_name="ZeroShotPrompt",
        fields=[
            TemplateField(
                field_type="str",
                required=False,
                placeholder="",
                is_list=False,
                show=True,
                multiline=True,
                value=prompt.PREFIX,
                name="prefix",
            ),
            TemplateField(
                field_type="str",
                required=True,
                placeholder="",
                is_list=False,
                show=True,
                multiline=True,
                value=prompt.FORMAT_INSTRUCTIONS,
                name="format_instructions",
            ),
            TemplateField(
                field_type="str",
                required=True,
                placeholder="",
                is_list=False,
                show=True,
                multiline=True,
                value=prompt.SUFFIX,
                name="suffix",
            ),
        ],
    )
    description: str = "Prompt template for Zero Shot Agent."
    base_classes: list[str] = ["BasePromptTemplate"]

    def to_dict(self):
        return super().to_dict()

    @staticmethod
    def format_field(field: TemplateField, name: Optional[str] = None) -> None:
        PromptComponent.format_field(field, name)