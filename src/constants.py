"""Constant variables used throughout the repocetory."""

from faker import Faker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

fake = Faker()
