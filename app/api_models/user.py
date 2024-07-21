from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.db_models.consts import UserStatus

module_name = 'user'


class Base(BaseModel):
    f"""
    Use this model for base fields of a {module_name}
    """


class Register(Base):
    f"""
    Use this model to create a {module_name}
    """
    name: str = Field(description="Name of user", example="Ehsan")
    family: str = Field(description="Family of user", example="Rezaee")
    email: str = Field(description="Email of user", example="admin@gmail.com")
    mobile: str = Field(description="Mobile of user", example="+989151112233")
    username: str = Field(description="Username of user", example="admin")
    password: str = Field(description="Password of user (will be hashed)", example="123456")


class MarketRegister(Base):
    f"""
    Use this model to create a {module_name}
    """
    name: str = Field(description="Name of user", example="Ehsan")
    email: str = Field(description="Email of user", example="admin@gmail.com")
    mobile: str = Field(description="Mobile of user", example="+989151112233")
    username: str = Field(description="Username of user", example="admin")
    pic: str = Field(description="Profile pic of user", example="pic.jpg")


class Login(Base):
    f"""
    Use this model to create a {module_name}
    """
    username: str = Field(description="Username of user", example="admin")
    password: str = Field(description="Password of user (will be hashed)", example="123456")


class ForgotPassword(Base):
    f"""
    Use this model to create a {module_name}
    """
    username: str = Field(description="Username or Email or Mobile of user", example="admin@gmail.com")


class ResetPassword(Base):
    f"""
    Use this model to create a {module_name}
    """
    email: str = Field(description="Email of user", example="admin@gmail.com")
    code: str = Field(description="Temporary code received by email", example="1000")
    new_password: str = Field(description="New password for user", example="123123")


class Write(Base):
    f"""
    Use this model to create a {module_name}
    """
    name: str = Field(description="Name of user", example="Ehsan")
    family: str = Field(description="Family of user", example="Rezaee")
    email: str = Field(description="Email of user", example="admin@gmail.com")
    mobile: str = Field(description="Mobile of user", example="+989151112233")
    role_id: str = Field(description="Role id of user", example="1")
    pic: str = Field(description="Profile pic of user", example="pic.jpg")
    status: UserStatus = Field(description="Status of user", default=UserStatus.Enabled)
    username: str = Field(description="Username of user", example="admin")
    password: str = Field(description="Password of user (will be hashed)", example="123456")


class Read(Base):
    f"""
    Use this model to read a {module_name}
    """
    id: str = Field(description="id", readOnly=True)
    created_at: datetime = Field(readOnly=True)
    updated_at: datetime = Field(readOnly=True)

    name: str = Field(description="Name of user", example="Ehsan")
    family: str = Field(description="Family of user", example="Rezaee")
    email: str = Field(description="Email of user", example="admin@gmail.com")
    mobile: str = Field(description="Mobile of user", example="+989151112233")
    last_login: datetime = Field(description="last_login of user", readOnly=True)
    email_verified: bool = Field(description="Is email verified?", readOnly=True)
    mobile_verified: bool = Field(description="Is mobile verified?", readOnly=True)
    role_id: str = Field(description="Role id of user", example="1")
    pic: str = Field(description="Profile pic of user", example="pic.jpg")
    status: UserStatus = Field(description="Status of user", default=UserStatus.Enabled)
    username: str = Field(description="Username of user", example="admin")


class Update(Base):
    f"""
    Use this model to update a {module_name}
    """
    name: str = Field(description="Name of user", example="Ehsan")
    family: str = Field(description="Family of user", example="Rezaee")
    email: str = Field(description="Email of user", example="admin@gmail.com")
    mobile: str = Field(description="Mobile of user", example="+989151112233")
    email_verified: bool = Field(description="Is email verified?")
    mobile_verified: bool = Field(description="Is mobile verified?")
    role_id: str = Field(description="Role id of user", example="1")
    pic: str = Field(description="Profile pic of user", example="pic.jpg")
    status: UserStatus = Field(description="Status of user", default=UserStatus.Enabled)
    username: str = Field(description="Username of user", example="admin")
    password: str = Field(description="Password of user (will be hashed)", example="123456")


ListRead = List[Read]
