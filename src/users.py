from src.books import Book
from src.constants import Base

from sqlalchemy import Column, BIGINT, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(BIGINT, primary_key=True, unique=True, autoincrement=False)
    name = Column(String(255))
    address = Column(String(255))

    borrowed_books = relationship(
        "Book", secondary="borrowed_books", back_populates="borrowers"
    )

    def __init__(self, name, user_id, address):
        self.name = name
        self.user_id = user_id
        self.address = address
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available():
            if book.loan_book(self.user_id):
                self.borrowed_books.append(book)
                return True
            else:
                return False  # Book is not available for loan
        else:
            return False  # Book is already borrowed or reserved

    def return_book(self, book):
        if book in self.borrowed_books:
            if book.return_book():
                self.borrowed_books.remove(book)
                return True
            else:
                return False  # Error in returning book
        else:
            return False  # User hasn't borrowed this book


class BorrowedBooks(Base):
    __tablename__ = "borrowed_books"

    user_id = Column(BIGINT, ForeignKey("users.user_id"), primary_key=True)
    book_id = Column(BIGINT, ForeignKey("books.unique_ISBN"), primary_key=True)

    user_borrowed = relationship("User", backref="books_borrowed")
    book_borrowed = relationship("Book", backref="borrowed_by")
