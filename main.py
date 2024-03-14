"""Main script."""

from src.data.database import SQLConnection
from src.data.generator import generate_fake_data_book, generate_fake_data_user
from src.entities.books import Book
from src.entities.users import User
from src.utils import ConfigManager


def main(num_books: int, num_users: int) -> None:
    """Run the main loop.

    Args:
        num_books (int): Number of books.
        num_users (int): Number of users.
    """
    # Load config file
    config_manager = ConfigManager("config.json")

    # Create SQL server if not present
    connection = SQLConnection(config_manager.username(), config_manager.password())

    # Generate fake data if database empty
    if connection.is_table_empty(Book):
        book_data = generate_fake_data_book(num_books)
        user_data = generate_fake_data_user(num_users)

        # Upload data in chunks
        chunk_size = 100
        connection.upload_data_in_chunks(book_data, chunk_size, Book)
        connection.upload_data_in_chunks(user_data, chunk_size, User)

    connection.session.close()


if __name__ == "__main__":
    main(1000, 200)
