class LibrarySystem:
    def __init__(self):
        self.books = []  # Liste over bøger i biblioteket
        self.users = {}  # Dictionary af brugerkonti (bruger_id: User)

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
        pass

    def loan_book(self, user_id, book_id):
        # Implementer udlånsoperationen
        pass

    def return_book(self, user_id, book_id):
        # Implementer returneringsoperationen
        pass

    def reserve_book(self, user_id, book_id):
        # Implementer reservationsoperationen
        pass

    # Implementer decorators til logging af vigtige operationer

    # Anvend designmønstre som Observer, Strategy, og Decorator

