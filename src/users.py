from books import Book

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(String, unique=True)

    borrowed_books = relationship("Book", secondary='borrowed_books')

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
    __tablename__ = 'borrowed_books'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)

    user = relationship(User, backref='borrowed_books')
    book = relationship("Book", backref='borrowed_by')
