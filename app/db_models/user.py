from typing import List

from passlib.context import CryptContext

from app.core.base_db import DB
from app.db_models.consts import UserStatus
from datetime import datetime

module_name = 'user'
module_text = 'User'


class User(DB):
    f"""
    Use this model to manage a {module_text}
    """

    def __init__(self, _id=None, module_name=module_name, module_text=module_text, db=None,
                 role_id='', family='', email='', username='', password='', pic='', country_code='',
                 last_login=datetime.now(), status=UserStatus.Enabled, name='', mobile='', email_verified=False,
                 mobile_verified=False):
        self._id: str = _id

        self.role_id: str = role_id
        self.name: str = name
        self.family: str = family
        self.email: str = email
        self.country_code: str = country_code
        self.mobile: str = mobile
        self.username: str = username
        self.password: str = password
        self.pic: str = pic
        self.last_login: datetime = last_login
        self.status: UserStatus = status
        self.password: str = password
        self.email_verified: bool = email_verified
        self.mobile_verified: bool = mobile_verified
        self.__password_is_hashed = False

        super().__init__(_id=_id, module_name=module_name, module_text=module_text, db=db)

    def list(self, query=None) -> List['User']:
        return super().list(query=query)

    def hash_password(self):
        if not self.__password_is_hashed:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            self.password = pwd_context.hash(self.password)
            self.__password_is_hashed = True

    def before_insert(self):
        self.hash_password()

    def before_update(self):
        self.hash_password()

    def login(self):
        self.hash_password()
        result = self.col.find({
            "$or": [
                {"username": self.username, "password": self.password},
                {"email": self.email, "password": self.password},
                {"mobile": self.mobile, "password": self.password},
            ]
        })
        return result
