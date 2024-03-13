"""Data generation script."""

import random
import time
import uuid
from datetime import datetime
from typing import Any, Callable, Generator

from src.constants import fake


def generate_fake_data_user(num_users: int) -> Generator[dict[str, Any], None, None]:
    """Generate fake users.

    Args:
        Num_users (int): Number of fake users.

    Returns:
        Generator[dict[str, Any], None, None]: Fake users.
    """
    for _ in range(num_users):
        yield {
            "user_id": time.perf_counter_ns(),
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
            "unique_ISBN": time.perf_counter_ns(),
        }


if __name__ == "__main__":
    pass
