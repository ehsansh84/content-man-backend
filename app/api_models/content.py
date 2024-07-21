from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.db_models.consts import ContentType

module_name = 'content'


class Base(BaseModel):
    f"""
    Use this model for base fields of a {module_name}
    """
    category_id: str = Field(description="category_id", example="62d7a781d8f8d7627ce212d5")
    title: str = Field(description="title", example="62d7a781d8f8d7627ce212d5")
    text: str = Field(description="text", example="62d7a781d8f8d7627ce212d5")
    image: str = Field(description="image", example="62d7a781d8f8d7627ce212d5")
    type: ContentType = Field(description="type", example=ContentType.Text)
    choices: str = Field(description="choices", example=["Option1", "Option2", "Option3", "Option4"])
    answer: int = Field(description="answer", example=0)
    tags: list = Field(description="tags", example=0)


class Write(Base):
    f"""
    Use this model to create a {module_name}
    """
    user_id: str = Field(description="user_id", example="62d7a781d8f8d7627ce212d5")


class Read(Base):
    f"""
    Use this model to read a {module_name}
    """
    id: str = Field(description="id", readOnly=True)
    created_at: datetime = Field(readOnly=True)
    updated_at: datetime = Field(readOnly=True)

    user_id: str = Field(description="user_id", example="62d7a781d8f8d7627ce212d5")
    visit_count: int = Field(description="visit_count", example=0)
    like_count: int = Field(description="like_count", example=0)


class Update(Base):
    f"""
    Use this model to update a {module_name}
    """
    pass


ListRead = List[Read]
