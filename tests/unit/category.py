import pytest
from bson import ObjectId
from app.db_models.category import Category
from app.db_models.consts import Language
from unittest.mock import MagicMock


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def category(mock_db):
    return Category(
        _id="123456789012345678901234",
        db=mock_db,
        user_id="user123",
        category_id="parent123",
        title="Test Category",
        language=Language.Farsi
    )


def test_category_initialization(category):
    assert category._id == "123456789012345678901234"
    assert category.user_id == "user123"
    assert category.parent_id == "parent123"
    assert category.name == "Test Category"
    assert category.language == Language.Farsi


def test_category_to_json(category):
    json_data = category.to_json()
    assert json_data['id'] == "123456789012345678901234"
    assert json_data['name'] == "Test Category"
    assert json_data['language'] == Language.Farsi
    assert json_data['user_id'] == "user123"
    assert json_data['parent_id'] == "parent123"


def test_category_insert(category):
    category._id = None
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = ObjectId("123456789012345678901234")
    category.col.insert_one = MagicMock(return_value=mock_insert_result)

    result = category.insert()

    assert result == "123456789012345678901234"
    assert category._id == "123456789012345678901234"
    assert category._DB__loaded == True
    category.col.insert_one.assert_called_once()


def test_category_update(category):
    category._DB__loaded = True
    category.col.update_one = MagicMock()
    category.update()
    category.col.update_one.assert_called_once()


def test_category_delete(category):
    category.col.delete_one = MagicMock()
    category.delete()
    category.col.delete_one.assert_called_once()


def test_category_load(category):
    mock_result = {
        "_id": ObjectId("123456789012345678901234"),
        "name": "Loaded Category",
        "language": Language.English,
        "user_id": "user456",
        "parent_id": "parent456"
    }
    category.col.find_one = MagicMock(return_value=mock_result)

    result = category.load()

    assert result == True
    assert category.name == "Loaded Category"
    assert category.language == Language.English
    assert category.user_id == "user456"
    assert category.parent_id == "parent456"


def test_category_exists(category):
    category.col.find_one = MagicMock(return_value={"name": "Existing Category"})

    result = category.exists("name", "Existing Category")

    assert result == True
    category.col.find_one.assert_called_once_with({"name": "Existing Category"})


def test_category_list(category):
    mock_results = [
        {"_id": ObjectId("123456789012345678901234"), "name": "Category 1"},
        {"_id": ObjectId("123456789012345678901235"), "name": "Category 2"}
    ]
    category.col.find = MagicMock(return_value=mock_results)

    results = category.list()

    assert len(results) == 2
    assert isinstance(results[0], Category)
    assert results[0].name == "Category 1"
    assert results[1].name == "Category 2"


def test_category_count(category):
    category.col.count_documents = MagicMock(return_value=5)

    result = category.count({"language": Language.Farsi})

    assert result == 5
    category.col.count_documents.assert_called_once_with({"language": Language.Farsi})


def test_category_set_payload(category):
    payload = {
        "name": "Updated Category",
        "language": Language.English
    }
    category.set_payload(payload)

    assert category.name == "Updated Category"
    assert category.language == Language.English
    assert category._DB__loaded == True


def test_category_set_payload_with_invalid_attribute(category):
    payload = {
        "invalid_attribute": "value"
    }
    with pytest.raises(ValueError):
        category.set_payload(payload)


def test_category_set_payload_with_none(category):
    with pytest.raises(ValueError):
        category.set_payload(None)
