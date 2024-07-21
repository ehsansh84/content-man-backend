from typing import List
from app.core.base_db import DB
from app.db_models.consts import ContentType, Language

module_name = 'content'
module_text = 'Content'


class Content(DB):
    f"""
    Use this model to manage a {module_text}
    """

    def __init__(self, _id=None, module_name=module_name, module_text=module_text, db=None,
                 user_id='', category_id='', title='', text='', type=ContentType.Text, image='',
                 choices=None, answer=-1, visit_count=0, like_count=0, tags=None, language=Language.Farsi):
        self._id: str = _id
        self.user_id: str = user_id
        self.language: Language = language
        self.category_id: str = category_id
        self.title: str = title
        self.text: str = text
        self.image: str = image
        self.type: ContentType = type
        self.choices: list = choices
        self.answer: int = answer
        self.visit_count: int = visit_count
        self.like_count: int = like_count
        self.tags: list = tags

        super().__init__(_id=_id, module_name=module_name, module_text=module_text, db=db)

    def list(self, query=None) -> List['Content']:
        return super().list(query=query)
