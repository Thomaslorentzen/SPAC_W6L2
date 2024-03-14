"""Unittest for the Book class."""

import unittest

from src.entities.books import Book


class TestBook(unittest.TestCase):
    """Test cases for the Book class."""

    def setUp(self) -> None:
        """Set up the test."""
        self.book = Book(
            title="Sample Book",
            author="John Doe",
            release_year=2022,
            unique_ISBN=123456789,
        )

    def test_reserve_book(self) -> None:
        """Test the reserve_book method."""
        # Assert that the book is initially available
        self.assertTrue(self.book.is_available())

        # Reserve the book
        user_id = 123
        result = self.book.reserve_book(user_id)

        # Assert that the book was reserved successfully
        self.assertTrue(result)
        self.assertFalse(self.book.is_available())

    def test_loan_book(self) -> None:
        """Test the loan_book method."""
        # Reserve the book
        user_id = 123
        self.book.reserve_book(user_id)

        # Assert that the book is not available
        self.assertFalse(self.book.is_available())

        # Loan the book
        result = self.book.loan_book(user_id)

        # Assert that the book was loaned successfully
        self.assertTrue(result)
        self.assertTrue(self.book.is_available())

    def test_return_book(self) -> None:
        """Test the return_book method."""
        # Reserve and loan the book
        user_id = 123
        self.book.reserve_book(user_id)
        self.book.loan_book(user_id)

        # Return the book
        result = self.book.return_book()

        # Assert that the book was returned successfully
        self.assertTrue(result)
        self.assertTrue(self.book.is_available())


if __name__ == "__main__":
    pass
