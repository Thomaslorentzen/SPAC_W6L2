"""Book logic."""

from sqlalchemy import BIGINT, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.constants import Base


class Book(Base):  # type: ignore
    """Book entity in the library database."""

    __tablename__ = "books"

    unique_ISBN = Column(BIGINT, primary_key=True, autoincrement=False)
    title = Column(String(255))
    author = Column(String(255))
    release_year = Column(Integer)
    available = Column(Boolean, default=True)
    reserved_by = Column(BIGINT, ForeignKey("users.user_id"))

    borrowers = relationship("User", back_populates="borrowed_books")

    def __init__(self, title: str, author: str, release_year: int, unique_ISBN: int):
        """Initialize class.

        Args:
            title (str): Title of book.
            author (str): Auther of book.
            release_year (int): Release year of book.
            unique_ISBN (int): Unique id of book.
        """
        self.title = title
        self.author = author
        self.release_year = release_year
        self.unique_ISBN = unique_ISBN
        self.available = True
        self.reserved: bool = False

    def is_available(self) -> bool:
        """Is book available.

        Returns:
            bool: Is book available.
        """
        return self.available  # type: ignore

    def reserve_book(self, user_id: int) -> bool:
        """Aplly logic to reserve book.

        Args:
            user_id (int): Id of user.

        Returns:
            bool: Is book reserved.
        """
        if self.available:
            self.available = False
            self.reserved_by = user_id
            return True
        else:
            return False

    def loan_book(self, user_id: int) -> bool:
        """Apply logic to loan book.

        Args:
            user_id (int): Id of user.

        Returns:
            bool: Is book loaned.
        """
        if self.available:
            self.available = True
            self.reserved_by = user_id
            return True
        else:
            return False

    def return_book(self) -> bool:
        """Impliment logic to return book.

        Returns:
            bool: is book returned.
        """
        self.available = True
        self.reserved_by = None
        return True
