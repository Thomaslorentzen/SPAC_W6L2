import mysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.constants import Base


def create_database(username: str, password: str):
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
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS library")

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


def upload_data_in_chunks(session, data, chunk_size, dataclass):
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
