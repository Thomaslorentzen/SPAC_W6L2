from books import Book
from functools import wraps

class LibrarySystem:
    def __init__(self):
        self.books = []  # Liste over bøger i biblioteket
        self.users = {}  # Dictionary af brugerkonti (bruger_id: User)
    
    def log_activity(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Log aktivitet
            activity = f"Function '{func.__name__}' called with args: {args}, kwargs: {kwargs}"
            print(activity)
            
            # Kald den oprindelige funktion
            result = func(*args, **kwargs)
            
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
        # Implementer søgning i bogsamlingen ved hjælp af list comprehensions eller generators
        for books in self.books:
            if query.lower() in books.title.lower() or  query.lower() in books.author.lower():
                yield books


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
                if book.is_available():
                    book.return_book(user_id)
                    return f"Bogen '{book.title}' er blevet returnert til bruger med ID {user_id}."
                else:
                    return f"Bogen '{book.title}' er allerede returnert."
        
        # Returnér en fejlbesked, hvis bogen ikke blev fundet
        return "Bogen med det angivne ID blev ikke fundet."

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
    
