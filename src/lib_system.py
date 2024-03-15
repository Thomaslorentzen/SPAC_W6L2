"""Functionality related to library system logic."""

from functools import wraps
from typing import Any, Callable, Generator, Optional

from src.entities.books import Book
from src.entities.users import User


class SearchStrategy:
    """Base class for search strategies."""

    def search(
        self,
        books: list[type[Book]],
        query: str,
    ) -> Generator[type[Book], None, None]:
        """Catch not implimented strategies.

        Args:
            books (list[type[Book]]): Books.
            query (str): Query to find books.

        Raises:
            NotImplementedError: strategies not implimented.

        Yields:
            Generator[type[Book], None, None]: Found books.
        """
        raise NotImplementedError()


class TitleSearchStrategy(SearchStrategy):
    """Search by title."""

    def search(
        self,
        books: list[type[Book]],
        query: str,
    ) -> Generator[type[Book], None, None]:
        """Search by title.

        Args:
            books (list[type[Book]]): Books.
            query (str): Query to find books.

        Yields:
            Generator[type[Book], None, None]: Found books.
        """
        for book in books:
            if query.lower() in book.title.lower():
                yield book


class AuthorSearchStrategy(SearchStrategy):
    """Search by author."""

    def search(
        self,
        books: list[type[Book]],
        query: str,
    ) -> Generator[type[Book], None, None]:
        """Search by author.

        Args:
            books (list[type[Book]]): Books.
            query (str): Query to find books.

        Yields:
            Generator[type[Book], None, None]: Found books.
        """
        for book in books:
            if query.lower() in book.author.lower():
                yield book


class ISBNSearchStrategy(SearchStrategy):
    """Search by ISBN."""

    def search(
        self,
        books: list[type[Book]],
        query: str,
    ) -> Generator[type[Book], None, None]:
        """Search by ISBN.

        Args:
            books (list[type[Book]]): Books.
            query (str): Query to find books.

        Yields:
            Generator[type[Book], None, None]: Found books.
        """
        for book in books:
            if str(book.unique_ISBN) == str(query):
                yield book


class yearSearchStrategy(SearchStrategy):
    """Search by year."""

    def search(
        self,
        books: list[type[Book]],
        query: str,
    ) -> Generator[type[Book], None, None]:
        """Search by year.

        Args:
            books (list[type[Book]]): Books.
            query (str): Query to find books.

        Yields:
            Generator[type[Book], None, None]: Found books.
        """
        query_year = int(query)

        for book in books:
            if book.release_year == query_year:
                yield book


class LibrarySystem:
    """System to handle books and users."""

    def __init__(self, books: Optional[list[type[Book]]] = None) -> None:
        """Initialize class.

        Args:
            books (list[type[Book]], optional): All books. Defaults to None.
        """
        self.books = books
        self.search_strategy: Optional[Any] = None
        self.transcript: list[str] = []

    def log_activity(  # type: ignore
        func: Callable[[Any, int, int], str],
    ) -> Callable[..., str]:
        """Wraping function to log activities.

        Args:
            func (Callable[
                [list[type[Book]], str],
                Generator[ type[Book],
                None, None, ],
                ]): Function to be wrapped.

        Returns:
            Callable[..., str]: Loggings.
        """

        @wraps(func)
        def wrapper(  # type: ignore
            self,
            *args: Any,
            **kwargs: Any,
        ) -> str:
            """Log activity.

            Returns:
                str: Result of activity.
            """
            activity = (
                f"Function '{func.__name__}' called with args: {args}, kwargs: {kwargs}"
            )
            print(activity)

            result = func(self, *args, **kwargs)

            # Log transaction details to transcript
            if "user_id" in kwargs and "book_id" in kwargs:
                user_id = kwargs["user_id"]
                book_id = kwargs["book_id"]
                book = next((b for b in self.books if b.unique_ISBN == book_id), None)
                if book:
                    action = func.__name__.replace("_", " ").capitalize()
                    transcript_entry = f"""User ID: {user_id},
                    Action: {action},
                    Book Title: {book.title},
                    Book ID: {book_id}"""
                    self.transcript.append(transcript_entry)

            return result

        return wrapper

    def search_books(self, query: str) -> list[type[Book]]:
        """Search for book.

        Args:
            query (str): Search query.

        Raises:
            ValueError: Search strategy not implimented.

        Returns:
            list[type[Book]]: Found books
        """
        # Check if a search strategy is set
        if self.search_strategy is None:
            raise ValueError("No search strategy set")

        # Perform search using the selected strategy
        books: list[type[Book]] = self.search_strategy.search(self.books, query)
        return books

    @log_activity
    def loan_book(self, user_id: int, book_id: int) -> str:
        """Try to loan book.

        Args:
            user_id (int): Id of user.
            book_id (int): Id of book.

        Returns:
            str: Result as text.
        """
        for book in self.books:  # type: ignore
            if book.unique_ISBN == book_id:
                if book.is_available():  # type: ignore
                    book.loan_book(user_id)  # type: ignore
                    return (
                        f"Bogen '{book.title}' er blevet udlånt"
                        f"til bruger med ID {user_id}."
                    )
                else:
                    return f"Bogen '{book.title}' er allerede udlånt."

        # Returnér en fejlbesked, hvis bogen ikke blev fundet
        return "Bogen med det angivne ID blev ikke fundet."

    @log_activity
    def return_book(self, user_id: int, book_id: int) -> str:
        """Try to return a book.

        Args:
            user_id (int): Id of user.
            book_id (int): Id of book.

        Returns:
            str: Result as text.
        """
        for book in self.books:  # type: ignore
            if book.unique_ISBN == book_id:
                if not book.is_available():  # type:ignore
                    book.return_book(user_id)  # type: ignore
                    return (
                        f"Bogen '{book.title}' blevt afleveret af bruger med ID"
                        f"{user_id}."
                    )
                else:
                    return (
                        f"Bogen '{book.title}' er allerede tilgængelig på biblioteket."
                    )

        return "Bogen med det specifikke ID blev ikke fundet."

    @log_activity
    def reserve_book(self, user_id: int, book_id: int) -> str:
        """Try to reserve book.

        Args:
            user_id (int): Id of user.
            book_id (int): Id of book.

        Returns:
            str: Result as text.
        """
        for book in self.books:  # type: ignore
            if book.unique_ISBN == book_id:
                if book.is_available():  # type: ignore
                    book.reserve_book(user_id)  # type: ignore
                    return (
                        f"Bogen '{book.title}' er blevet reserveret"
                        f"til bruger med ID {user_id}."
                    )
                else:
                    return f"Bogen '{book.title}' er allerede reserveret."

        # Returnér en fejlbesked, hvis bogen ikke blev fundet
        return "Bogen med det angivne ID blev ikke fundet."


class ReservedBookNotification:
    """Notification system."""

    def update(self, book: type[Book]) -> None:
        """Update.

        Args:
            book (type[Book]): Book of interest.
        """
        if book.available:
            print(
                f"Bogen '{book.title}' er nu tilgængelig."
                f"Notifikation sendt til bruger {book.reserved_by}."
            )
