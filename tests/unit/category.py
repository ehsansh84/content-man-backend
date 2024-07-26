import unittest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from datetime import datetime
from app.db_models.category import Category
from app.db_models.consts import Language


class TestCategory(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_col = self.mock_db['category']
        self.category = Category(db=self.mock_db)

    def test_insert(self):
        # Arrange
        self.category.name = "Test Category"
        self.category.language = Language.Farsi
        self.mock_col.insert_one.return_value.inserted_id = ObjectId("5f50c31e8a7d7a1c9c8b4567")
        # Act
        result = self.category.insert()

        # Assert
        self.assertEqual(result, "5f50c31e8a7d7a1c9c8b4567")
        self.mock_col.insert_one.assert_called_once()
        self.assertTrue(self.category.is_loaded())

    def test_load(self):
        # Arrange
        mock_data = {
            "_id": ObjectId("5f50c31e8a7d7a1c9c8b4567"),
            "name": "Test Category",
            "language": Language.Farsi,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        self.mock_col.find_one.return_value = mock_data
        self.category._id = "5f50c31e8a7d7a1c9c8b4567"

        # Act
        result = self.category.load()

        # Assert
        self.assertTrue(result)
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.language, Language.Farsi)
        self.mock_col.find_one.assert_called_once_with({"_id": ObjectId("5f50c31e8a7d7a1c9c8b4567")})

    def test_update(self):
        # Arrange
        self.category._id = "5f50c31e8a7d7a1c9c8b4567"
        self.category.name = "Updated Category"
        self.category._DB__loaded = True  # Simulate a loaded object

        # Act
        self.category.update()

        # Assert
        self.mock_col.update_one.assert_called_once()
        call_args = self.mock_col.update_one.call_args
        self.assertEqual(call_args[0][0], {'_id': ObjectId("5f50c31e8a7d7a1c9c8b4567")})
        self.assertIn('name', call_args[0][1]['$set'])
        self.assertEqual(call_args[0][1]['$set']['name'], "Updated Category")

    def test_delete(self):
        # Arrange
        self.category._id = "5f50c31e8a7d7a1c9c8b4567"
        self.mock_col.delete_one.return_value.raw_result = {"n": 1, "ok": 1.0}

        # Act
        result = self.category.delete()

        # Assert
        self.assertEqual(result, {"n": 1, "ok": 1.0})
        self.mock_col.delete_one.assert_called_once_with({'_id': ObjectId("5f50c31e8a7d7a1c9c8b4567")})

    def test_list(self):
        # Arrange
        mock_data = [
            {
                "_id": ObjectId("5f50c31e8a7d7a1c9c8b4567"),
                "name": "Category 1",
                "language": Language.Farsi
            },
            {
                "_id": ObjectId("5f50c31e8a7d7a1c9c8b4568"),
                "name": "Category 2",
                "language": Language.English
            }
        ]
        self.mock_col.find.return_value = mock_data

        # Act
        result = self.category.list()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Category)
        self.assertEqual(result[0].name, "Category 1")
        self.assertEqual(result[1].name, "Category 2")
        self.mock_col.find.assert_called_once_with({})


if __name__ == '__main__':
    unittest.main()
