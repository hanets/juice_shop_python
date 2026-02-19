"""Base model with automatic snake_case to camelCase conversion."""

from pydantic import BaseModel, ConfigDict


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelModel(BaseModel):
    """Base model that converts snake_case fields to camelCase aliases.
    
    All fields use snake_case in Python code, but serialize/deserialize
    using camelCase for API compatibility.
    """

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )
