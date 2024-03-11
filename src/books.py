from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    release_year = Column(Integer)
    unique_ISBN = Column(String, unique=True)
    available = Column(Boolean, default=True)
    reserved_by = Column(Integer, ForeignKey("users.id"))

    def is_available(self):
        return self.available

    def reserve_book(self, user_id):
        if self.available:
            self.available = False
            self.reserved_by = user_id
            return True
        else:
            return False

    def loan_book(self, user_id):
        if self.available:
            self.available = True
            self.reserved_by = user_id
            return True
        else:
            return False

    def return_book(self):
        self.available = True
        self.reserved_by = None
        return True
