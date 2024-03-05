from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base schema class to be inherited by all application schemas."""

    model_config = {
        "from_attributes": True,
    }
