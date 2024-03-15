from src.entities.books import Book
from functools import wraps


class SearchStrategy:
    def search(self, books, query):
        raise NotImplementedError()


class TitleSearchStrategy(SearchStrategy):
    def search(self, books, query):
        for book in books:
            if query.lower() in book.title.lower():
                yield book

class AuthorSearchStrategy(SearchStrategy):
    def search(self, books, query):
        for book in books:
            if query.lower() in book.author.lower():
                yield book



class ISBNSearchStrategy(SearchStrategy):
    def search(self, books, query):
        for book in books:
            if str(book.unique_ISBN) == str(query):
                yield book



class yearSearchStrategy(SearchStrategy):
    def search(self, books, query):
        # Convert the query to an integer
        query_year = int(query)
        
        for book in books:
            #print("Book release year:", book.release_year)
            # Compare the release_year with the query_year
            if book.release_year == query_year:
                yield book




class LibrarySystem:
    def __init__(self, books=None):
        self.books = books if books is not None else []
        self.users = {}
        self.search_strategy = None
        self.transcript = []

    def set_books(self, books):
        self.books = books

    def log_activity(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Log aktivitet
            activity = (
                f"Function '{func.__name__}' called with args: {args}, kwargs: {kwargs}"
            )
            print(activity)

            # Kald den oprindelige funktion
            result = func(self, *args, **kwargs)

             # Log transaction details to transcript
            if "user_id" in kwargs and "book_id" in kwargs:
                user_id = kwargs["user_id"]
                book_id = kwargs["book_id"]
                book = next((b for b in self.books if b.unique_ISBN == book_id), None)
                if book:
                    action = func.__name__.replace("_", " ").capitalize()
                    transcript_entry = f"User ID: {user_id}, Action: {action}, Book Title: {book.title}, Book ID: {book_id}"
                    self.transcript.append(transcript_entry)

            # Returnér resultatet af funktionen
            return result

        return wrapper

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def add_user(self, user):
        self.users[user.user_id] = user

    def remove_user(self, user):
        del self.users[user.user_id]

    def search_books(self, query):
        # Check if a search strategy is set
        if self.search_strategy is None:
            raise ValueError("No search strategy set")

        # Perform search using the selected strategy
        return self.search_strategy.search(self.books, query)


    @log_activity
    def loan_book(self, user_id, book_id):
        for book in self.books:
            if book.unique_ISBN == book_id:
                if book.is_available():
                    book.loan_book(user_id)
                    return f"Bogen '{book.title}' er blevet udlånt til bruger med ID {user_id}."
                else:
                    return f"Bogen '{book.title}' er allerede udlånt."

        # Returnér en fejlbesked, hvis bogen ikke blev fundet
        return "Bogen med det angivne ID blev ikke fundet."

    @log_activity
    def return_book(self, user_id, book_id):
        for book in self.books:
            if book.unique_ISBN == book_id:
                if not book.is_available():
                    book.return_book(user_id)
                    return f"Bogen '{book.title}' er blevet afleveret af bruger med ID {user_id}."
                else:
                    return f"Bogen '{book.title}' er allerede tilgængelig på biblioteket."

        return "Bogen med det specifikke ID blev ikke fundet."


    @log_activity
    def reserve_book(self, user_id, book_id):
        for book in self.books:
            if book.unique_ISBN == book_id:
                if book.is_available():
                    book.reserve_book(user_id)
                    return f"Bogen '{book.title}' er blevet reserveret til bruger med ID {user_id}."
                else:
                    return f"Bogen '{book.title}' er allerede reserveret."

        # Returnér en fejlbesked, hvis bogen ikke blev fundet
        return "Bogen med det angivne ID blev ikke fundet."


class ReservedBookNotification:
    def update(self, book):
        if book.available:
            print(
                f"Bogen '{book.title}' er nu tilgængelig. Notifikation sendt til bruger {book.reserved_by}."
            )
