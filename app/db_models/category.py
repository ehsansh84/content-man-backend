from typing import List
from app.core.base_db import DB
from app.db_models.consts import Language

module_name = 'category'
module_text = 'Category'


class Category(DB):
    f"""
    Use this model to manage a {module_text}
    """

    def __init__(self, _id=None, module_name=module_name, module_text=module_text, db=None,
                 user_id='', category_id='', title='', language=Language.Farsi):
        self._id: str = _id
        self.user_id: str = user_id
        self.language: Language = language
        self.parent_id: str = category_id
        self.name: str = title

        super().__init__(_id=_id, module_name=module_name, module_text=module_text, db=db)

    def list(self, query=None) -> List['Category']:
        return super().list(query=query)
