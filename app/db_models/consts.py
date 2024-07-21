from enum import Enum
from datetime import datetime, timedelta


class UserStatus(str, Enum):
    Enabled = "enabled"
    Disabled = "disabled"


class ContentType(str, Enum):
    Text = "text"
    Image = "image"
    Question = "question"
