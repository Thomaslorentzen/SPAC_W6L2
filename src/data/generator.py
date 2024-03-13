"""Data generation script."""

import uuid
from datetime import datetime
from typing import Any, Generator, Callable
import time
import random

from src.constants import fake


def generate_fake_data_user(num_users):
    """Create a single fake row.

    Args:
        Num_users (int): Variable used for imap.

    Returns:
        dict[str, Any]: Fake data.
    """
    for _ in range(num_users):
        yield {
            "user_id": time.perf_counter_ns(),
            "name": fake.name(),
            "address": fake.address(),
        }


def generate_fake_data_book(num_records):
    current_year = datetime.now().year
    for _ in range(num_records):
        yield {
            "title": fake.text(max_nb_chars=50),
            "author": fake.name(),
            "release_year": fake.random_int(min=1950, max=current_year),
            "unique_ISBN": time.perf_counter_ns(),
        }
