"""Functions to handle sql database."""

from typing import Any, Generator, Union

import mysql
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.books import Book
from src.constants import Base
from src.users import User


def create_database(username: str, password: str) -> Session:
    """Create the sql database if not present and connect.

    Args:
        username (str): Username for sql server.
        password (str): Password for sql server.

    Returns:
        Session: Connection to sql server.
    """
    # Create an engine to connect to your MySQL server
    engine = create_engine(
        f"mysql+mysqlconnector://{username}:{password}@localhost/", echo=True
    )

    # Connect to the MySQL server and obtain a connection object
    connection = engine.connect()

    connection = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library")

    # Close the connection
    connection.close()

    # Now connect to the 'library' database
    engine = create_engine(
        f"mysql+mysqlconnector://{username}:{password}@localhost/library", echo=True
    )

    Base.metadata.create_all(engine)

    # Create a sessionmaker bound to the engine
    Session = sessionmaker(bind=engine)

    # Create a session
    session = Session()

    return session


def upload_data_in_chunks(
    session: Session,
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
            session.bulk_save_objects(chunk)
            session.commit()
            chunk = []
    if chunk:
        session.bulk_save_objects(chunk)
        session.commit()


def is_table_empty(session: Session, table: type[Book]) -> bool:
    """Check if a table is empty.

    Args:
        session (Session): Connection to the sql database.
        table (Book): Table to be checked.

    Returns:
        bool: Is table empty.
    """
    # Count the number of rows in the table
    count = session.query(table).count()

    # If the count is zero, the table is empty
    return bool(count == 0)


if __name__ == "__main__":
    pass
