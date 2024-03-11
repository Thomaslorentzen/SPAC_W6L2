from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.books import Book
from src.constants import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    books = relationship("Book", back_populates="user")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
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
