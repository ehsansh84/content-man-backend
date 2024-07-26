import pytest
from datetime import datetime
from bson import ObjectId
from app.db_models.user import User
from app.db_models.consts import UserStatus
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def user(mock_db):
    return User(
        _id="123456789012345678901234",
        db=mock_db,
        role_id="role1",
        name="John",
        family="Doe",
        email="john@example.com",
        username="johndoe",
        password="password123",
        mobile="1234567890"
    )


def test_user_initialization(user):
    assert user._id == "123456789012345678901234"
    assert user.role_id == "role1"
    assert user.name == "John"
    assert user.family == "Doe"
    assert user.email == "john@example.com"
    assert user.username == "johndoe"
    assert user.password == "password123"
    assert user.mobile == "1234567890"
    assert user.status == UserStatus.Enabled
    assert user.email_verified == False
    assert user.mobile_verified == False


def test_to_json(user):
    json_data = user.to_json()
    assert json_data['id'] == "123456789012345678901234"
    assert json_data['name'] == "John"
    assert json_data['email'] == "john@example.com"
    assert 'password' in json_data  # Make sure password is included in JSON


def test_hash_password(user):
    original_password = user.password
    user.hash_password()
    assert user.password != original_password
    assert len(user.password) > len(original_password)


@patch('app.db_models.user.CryptContext')
def test_before_insert(mock_crypt_context, user):
    mock_hash = MagicMock(return_value="hashed_password")
    mock_crypt_context.return_value.hash = mock_hash

    user.before_insert()

    mock_hash.assert_called_once_with("password123")
    assert user.password == "hashed_password"


@patch('app.db_models.user.CryptContext')
def test_before_update(mock_crypt_context, user):
    mock_hash = MagicMock(return_value="hashed_password")
    mock_crypt_context.return_value.hash = mock_hash

    user.before_update()

    mock_hash.assert_called_once_with("password123")
    assert user.password == "hashed_password"


def test_login(user):
    user.col.find = MagicMock(return_value=[{"username": "johndoe"}])

    result = user.login()

    user.col.find.assert_called_once()
    assert result == [{"username": "johndoe"}]


def test_prepare_insert(user):
    with pytest.raises(ValueError):
        user.prepare_insert()


def test_prepare_update(user):
    user._DB__loaded = True
    update_doc = user.prepare_update()
    assert 'updated_at' in update_doc
    assert 'id' not in update_doc
    assert '_id' not in update_doc


def test_insert(user):
    user._id = None
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = ObjectId("123456789012345678901234")
    user.col.insert_one = MagicMock(return_value=mock_insert_result)

    result = user.insert()

    assert result == "123456789012345678901234"
    assert user._id == "123456789012345678901234"
    assert user._DB__loaded == True


def test_update(user):
    user.col.update_one = MagicMock()
    user.update()
    user.col.update_one.assert_called_once()


def test_delete(user):
    user.col.delete_one = MagicMock()
    user.delete()
    user.col.delete_one.assert_called_once()


def test_load(user):
    mock_result = {
        "_id": ObjectId("123456789012345678901234"),
        "name": "John",
        "email": "john@example.com"
    }
    user.col.find_one = MagicMock(return_value=mock_result)

    result = user.load()

    assert result == True
    assert user.name == "John"
    assert user.email == "john@example.com"


def test_exists(user):
    user.col.find_one = MagicMock(return_value={"username": "johndoe"})

    result = user.exists("username", "johndoe")

    assert result == True
    user.col.find_one.assert_called_once_with({"username": "johndoe"})


def test_list(user):
    mock_results = [
        {"_id": ObjectId("123456789012345678901234"), "name": "John"},
        {"_id": ObjectId("123456789012345678901235"), "name": "Jane"}
    ]
    user.col.find = MagicMock(return_value=mock_results)

    results = user.list()

    assert len(results) == 2
    assert isinstance(results[0], User)
    assert results[0].name == "John"
    assert results[1].name == "Jane"


def test_count(user):
    user.col.count_documents = MagicMock(return_value=5)

    result = user.count({"status": UserStatus.Enabled})

    assert result == 5
    user.col.count_documents.assert_called_once_with({"status": UserStatus.Enabled})


def test_set_payload(user):
    payload = {
        "name": "Jane",
        "email": "jane@example.com"
    }
    user.set_payload(payload)

    assert user.name == "Jane"
    assert user.email == "jane@example.com"
    assert user._DB__loaded == True


def test_set_payload_with_invalid_attribute(user):
    payload = {
        "invalid_attribute": "value"
    }
    with pytest.raises(ValueError):
        user.set_payload(payload)


def test_set_payload_with_none(user):
    with pytest.raises(ValueError):
        user.set_payload(None)
