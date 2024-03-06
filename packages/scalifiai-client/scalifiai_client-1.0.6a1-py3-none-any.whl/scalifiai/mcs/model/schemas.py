from pydantic import BaseModel, Field
from typing import Optional


class CreateModel(BaseModel):

    verbose_name: str = Field(validation_alias="name")
    description: Optional[str]
