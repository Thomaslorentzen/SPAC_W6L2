"""User logic."""

from sqlalchemy import BIGINT, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.entities.books import Book
from src.constants import Base


class User(Base):  # type: ignore
    """User entity in the library database."""

    __tablename__ = "users"

    user_id = Column(BIGINT, primary_key=True, unique=True, autoincrement=False)
    name = Column(String(255))
    address = Column(String(255))

    borrowed_books = relationship(
        "Book", secondary="borrowed_books", back_populates="borrowers"
    )

    def __init__(self, name: str, user_id: int, address: str):
        """Initialize class.

        Args:
            name (str): Name of user
            user_id (str): Id of user.
            address (str): Address of user.
        """
        self.name = name
        self.user_id = user_id
        self.address = address
        self.borrowed_books = []

    def borrow_book(self, book: Book) -> bool:
        """Apply logic to borrow a book.

        Args:
            book (Book): The book to be borrowed.

        Returns:
            bool: Is the book available.
        """
        if book.is_available():
            if book.loan_book(self.user_id):
                self.borrowed_books.append(book)
                return True
            else:
                return False  # Book is not available for loan
        else:
            return False  # Book is already borrowed or reserved

    def return_book(self, book: Book) -> bool:
        """Impliment logic to return a book.

        Args:
            book (Book): Book to be returned.

        Returns:
            bool: Was the return a succes.
        """
        if book in self.borrowed_books:
            if book.return_book():
                self.borrowed_books.remove(book)
                return True
            else:
                return False  # Error in returning book
        else:
            return False  # User hasn't borrowed this book


class BorrowedBooks(Base):  # type: ignore
    """Association table between users and books in the library database."""

    __tablename__ = "borrowed_books"

    user_id = Column(BIGINT, ForeignKey("users.user_id"), primary_key=True)
    book_id = Column(BIGINT, ForeignKey("books.unique_ISBN"), primary_key=True)

    user_borrowed = relationship("User", backref="books_borrowed")
    book_borrowed = relationship("Book", backref="borrowed_by")
