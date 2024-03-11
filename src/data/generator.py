"""Data generation script."""

import uuid

import csv
from multiprocessing import Pool
from typing import Any, Generator

from tqdm import tqdm

from src.constants import fake


def create_fake_row_user(_: Any) -> dict[str, Any]:
    """Create a single fake row.

    Args:
        _ (Any): Variable used for imap.

    Returns:
        dict[str, Any]: Fake Row.
    """
    profile: dict[str, Any] = {
        "ID": uuid.uuid4(),
        "Name": fake.name(),
        "Adress": fake.adress(),
        "Borrowed books": [],
    }
    return profile


def create_fake_row_book(_: Any) -> dict[str, Any]:
    """Create a single fake row.

    Args:
        _ (Any): Variable used for imap.

    Returns:
        dict[str, Any]: Fake Row.
    """
    book: dict[str, Any] = {
        "Auther": fake.name(),
        "Puplished": fake.year(),
        "ID": uuid.uuid4(),
    }

    return book


def generate_fake_dataset(
    num_rows: int,
    function: callable[[], dict[str, Any]],
) -> Generator[dict[str, str], None, None]:
    """Create generator for making dataset.

    Args:
        num_rows (int): Number of desired row in dataset.

    Yields:
        Generator[list[str, str], None, None]: Fake row generator.
    """
    with Pool() as pool:
        rows = pool.imap_unordered(function, range(num_rows))
        for row in rows:
            yield row


def create_dataset(
    name: str,
    num_rows: int,
    function: callable[[], dict[str, Any]],
) -> None:
    """Save the dataset iterativly.

    Args:
        name (str): File name.
        num_rows (int): Desired number of rows.
    """
    iterator = generate_fake_dataset(num_rows, function)
    fake_row = create_fake_row_user(None)
    with open(f"Data/{name}.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        csv_writer.writerow(fake_row.keys())

        # Write rows
        for row in tqdm(iterator, total=num_rows, desc=f"Creating {name}.csv"):
            csv_writer.writerow(row.values())
