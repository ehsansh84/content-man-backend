from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str = Field(description="uid of created object", example="f969d7c6-c9a0-470b-84bf-b286f71ca38b")


class OutputCreate(BaseModel):
    """
    Use this model to create method response_model
    """
    data: Item
    detail: str = Field(description="Item successfully created.")


class OutputOnlyNote(BaseModel):
    """
    Use this model to all methods with only a text an output for response_model
    """
    detail: str = Field(description="Note string")
