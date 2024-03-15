"""Unittest for the User class."""

import unittest
from unittest.mock import MagicMock

from src.entities.users import User


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = User(name="John Doe", user_id=123, address="123 Main St")

    def test_borrow_book_success(self) -> None:
        """Test borrow book function."""
        mock_book = MagicMock()
        mock_book.is_available.return_value = True
        mock_book.loan_book.return_value = True

        # Borrow the book
        result = self.user.borrow_book(mock_book)

        # Assert that the book was borrowed successfully
        self.assertTrue(result)
        self.assertIn(mock_book, self.user.borrowed_books)

    def test_return_book_success(self) -> None:
        """Test return book function."""
        # Mocking a book object
        mock_book = MagicMock()
        self.user.borrowed_books.append(mock_book)

        # Return the book
        result = self.user.return_book(mock_book)

        # Assert that the book was returned successfully
        self.assertTrue(result)
        self.assertNotIn(mock_book, self.user.borrowed_books)


if __name__ == "__main__":
    pass
