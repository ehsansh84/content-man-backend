from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.db_models.consts import ContentType, Language

module_name = 'content'


class Base(BaseModel):
    f"""
    Use this model for base fields of a {module_name}
    """
    parent_id: str = Field(description="parent_id", example="62d7a781d8f8d7627ce212d5")
    language: Language = Field(description="language", example=Language.Farsi)
    name: str = Field(description="name", example="cat1")


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


class Update(Base):
    f"""
    Use this model to update a {module_name}
    """
    pass


ListRead = List[Read]
