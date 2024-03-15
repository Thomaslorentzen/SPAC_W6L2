"""Functions to handle sql database."""

from typing import Any, Generator, Union

from mysql import connector
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from src.constants import Base
from src.entities.books import Book
from src.entities.users import User
from src.utils import generate_id


class SQLConnection:
    """Class to handle sql connection and queries."""

    _instance = None

    def __new__(cls: Any, *args: tuple[Any], **kwargs: tuple[Any]) -> Any:
        """Make sure there is only one instance of this class.

        Args:
            cls (DatabaseConnection): The class of the instance being created.

        Returns:
            DatabaseConnection: The instance of the DatabaseConnection class.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, username: str, password: str) -> None:
        """Initialize class.

        Args:
            username (str): Username for sql server.
            password (str): Password for sql server.
        """
        self.username = username
        self.password = password
        self.session = self.create_database()

    def create_database(self) -> Session:
        """Create the sql database if not present and connect.

        Returns:
            Session: Connection to sql server.
        """
        connection_mysql = connector.connect(
            host="localhost",
            user=self.username,
            password=self.password,
        )
        cursor = connection_mysql.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS library")

        # Close the connection
        connection_mysql.close()

        # Now connect to the 'library' database
        engine = create_engine(
            f"mysql+mysqlconnector://{self.username}:{self.password}@localhost/library",
            echo=True,
        )

        Base.metadata.create_all(engine)

        # Create a sessionmaker bound to the engine
        Session = sessionmaker(bind=engine)

        # Create a session
        session = Session()

        return session

    def upload_data_in_chunks(
        self,
        data: Generator[dict[str, Any], None, None],
        chunk_size: int,
        dataclass: Union[type[User], type[Book]],
    ) -> None:
        """Upload data to sql server in chuncks.

        Args:
            session (Session): Connection to sql server.
            data (Generator[Dict[str, Any], None, None]): Data.
            chunk_size (int): Size of chunks to be uploaded.
            dataclass Union[User, Book]: Class of the data.
        """
        chunk = []
        for record in data:
            chunk.append(dataclass(**record))
            if len(chunk) >= chunk_size:
                self.session.bulk_save_objects(chunk)
                self.session.commit()
                chunk = []
        if chunk:
            self.session.bulk_save_objects(chunk)
            self.session.commit()

    def is_table_empty(self, table: type[Book]) -> bool:
        """Check if a table is empty.

        Args:
            table (Book): Table to be checked.

        Returns:
            bool: Is table empty.
        """
        # Count the number of rows in the table
        count = self.session.query(table).count()

        # If the count is zero, the table is empty
        return bool(count == 0)

    def add_user(self, name: str, address: str) -> None:
        """Add a user to the database.

        Args:
            name (str): Name of user
            address (str): Address of user.
        """
        try:
            user_id = generate_id()
            new_user = User(name=name, user_id=user_id, address=address)
            self.session.add(new_user)
            self.session.commit()
            print("User added successfully!")
        except IntegrityError as e:
            self.session.rollback()
            print(f"Failed to add user: {e}")

    def add_book(
        self,
        title: str,
        author: str,
        release_year: int,
    ) -> None:
        """Add a book to the database.

        Args:
            title (str): Title of book.
            author (str): Author of book.
            release_year (int): Release year of book.
        """
        try:
            unique_ISBN = generate_id()
            new_book = Book(
                title=title,
                author=author,
                release_year=release_year,
                unique_ISBN=unique_ISBN,
            )
            self.session.add(new_book)
            self.session.commit()
            print("Book added successfully!")
        except IntegrityError as e:
            self.session.rollback()
            print(f"Failed to add book: {e}")

    def remove_user_by_id(self, user_id: int) -> bool:
        """Remove a user from the database by their ID.

        Args:
            user_id (int): The ID of the user to remove.

        Returns:
            bool: True if the user was successfully removed, False otherwise.
        """
        try:
            user = self.session.query(User).filter(User.user_id == user_id).one()
            self.session.delete(user)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False

    def remove_book_by_id(self, unique_ISBN: int) -> bool:
        """Remove a book from the database by its unique ISBN.

        Args:
            unique_ISBN (int): The unique ISBN of the book to remove.

        Returns:
            bool: True if the book was successfully removed, False otherwise.
        """
        try:
            book = (
                self.session.query(Book).filter(Book.unique_ISBN == unique_ISBN).one()
            )
            self.session.delete(book)
            self.session.commit()
            return True
        except IntegrityError:
            self.session.rollback()
            return False


if __name__ == "__main__":
    pass
