"""Data generation script."""

from datetime import datetime
from typing import Any, Generator

from src.constants import fake
from src.utils import generate_id


def generate_fake_data_user(num_users: int) -> Generator[dict[str, Any], None, None]:
    """Generate fake data.

    Args:
        Num_users (int): Number of fake users.

    Returns:
        Generator[dict[str, Any], None, None]: Fake users.
    """
    for _ in range(num_users):
        yield {
            "user_id": generate_id,
            "name": fake.name(),
            "address": fake.address(),
        }


def generate_fake_data_book(num_records: int) -> Generator[dict[str, Any], None, None]:
    """Generate fake books.

    Args:
        num_records (int): Number of fake books.

    Yields:
        Generator[dict[str, Any], None, None]: Fake books.
    """
    current_year = datetime.now().year
    for _ in range(num_records):
        yield {
            "title": fake.text(max_nb_chars=50),
            "author": fake.name(),
            "release_year": fake.random_int(min=1950, max=current_year),
            "unique_ISBN": generate_id(),
        }


if __name__ == "__main__":
    pass
