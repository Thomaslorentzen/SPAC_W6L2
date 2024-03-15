"""GUI for library system."""

# TODO: Fix messagebox
import tkinter as tkinter
from tkinter import ttk
from typing import Any, Optional

from src.data.database import SQLConnection
from src.entities.books import Book
from src.lib_system import (
    AuthorSearchStrategy,
    ISBNSearchStrategy,
    LibrarySystem,
    TitleSearchStrategy,
    yearSearchStrategy,
)
from src.utils import ConfigManager


class LibraryApp(tkinter.Tk):
    """User interface to interact with library system."""

    def __init__(self, *args, **kwargs):  # type: ignore
        """Initialize class."""
        super().__init__(*args, **kwargs)
        self.title("Bibliotekssøgning")
        self.config_manager = ConfigManager("config.json")
        self.user_name = self.config_manager.username()
        self.password = self.config_manager.password()
        self.geometry("800x600")

        self.connection = SQLConnection(self.user_name, self.password)
        self.connection.create_fake_dataset()

        # Load books from the database or any other source
        books = self.connection.load_books_from_database()

        self.library = LibrarySystem(books)

        self.search_frame = tkinter.Frame(self)
        self.search_frame.pack(padx=10, pady=10)

        self.query_label = tkinter.Label(self.search_frame, text="Search Query:")
        self.query_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.query_entry = tkinter.Entry(self.search_frame)
        self.query_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.strategy_label = tkinter.Label(self.search_frame, text="Search Strategy:")
        self.strategy_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.strategy_combobox = ttk.Combobox(
            self.search_frame, values=["Title", "Author", "ISBN", "Release Year"]
        )
        self.strategy_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.strategy_combobox.current(0)

        self.user_id_entry_label = tkinter.Label(self.search_frame, text="User ID:")
        self.user_id_entry_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.user_id_entry = tkinter.Entry(self.search_frame)
        self.user_id_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.search_button = tkinter.Button(
            self.search_frame, text="Search", command=self.search_books
        )
        self.search_button.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.reserve_button = tkinter.Button(
            self.search_frame, text="Reserve", command=lambda: self.reserve_book()
        )
        self.reserve_button.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.loan_button = tkinter.Button(
            self.search_frame, text="Loan", command=self.loan_book
        )
        self.loan_button.grid(
            row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.return_button = tkinter.Button(
            self.search_frame,
            text="Return",
            command=lambda: self.return_book(
                self.get_user_id_from_input(), self.get_selected_book_id()
            ),
        )
        self.return_button.grid(
            row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.results_frame = tkinter.Frame(self)
        self.results_frame.pack(padx=10, pady=10)

        self.results_label = tkinter.Label(self.results_frame, text="Search Results:")
        self.results_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Expanded the Listbox and wrapped it in a Scrollbar
        self.results_listbox = tkinter.Listbox(self.results_frame)
        self.results_listbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.results_scrollbar = tkinter.Scrollbar(
            self.results_frame, orient="vertical", command=self.results_listbox.yview
        )
        self.results_scrollbar.grid(row=1, column=1, sticky="ns")

        self.results_listbox.config(yscrollcommand=self.results_scrollbar.set)

    def get_selected_book_id(self) -> Optional[int]:
        """Get id of the selected book.

        Returns:
            int: Id of the selected book.
        """
        selected_book_index = self.results_listbox.curselection()  # type: ignore
        if selected_book_index:
            selected_book = self.library.books[selected_book_index[0]]  # type: ignore
            return int(selected_book.unique_ISBN)
        return None

    def return_book(self, user_id: int, book_id: Optional[int]) -> None:
        """Return a book.

        Args:
            user_id (int): Id of the user.
            book_id (int): Id of the book.
        """
        selected_book_index = self.results_listbox.curselection()  # type: ignore
        if selected_book_index:
            message = self.library.return_book(user_id, book_id)
            tkinter.messagebox.showinfo("Return Book", message)  # type: ignore
            self.search_books()  # Refresh the search results after returning a book

    def reserve_book(self) -> None:
        """Get the selected book from the listbox."""
        selected_book_index = self.results_listbox.curselection()  # type: ignore
        if selected_book_index:
            selected_book = self.library.books[selected_book_index[0]]  # type: ignore
            user_id = self.get_user_id_from_input()
            book_id = selected_book.unique_ISBN
            message = self.library.reserve_book(user_id, book_id)
            tkinter.messagebox.showinfo("Reserve Book", message)  # type:ignore
            self.search_books()  # Refresh the search results after reserving a book

    def loan_book(self) -> None:
        """Get the selected book from the listbox."""
        selected_book_index = self.results_listbox.curselection()  # type: ignore
        if selected_book_index:
            selected_book = self.library.books[selected_book_index[0]]  # type: ignore
            user_id = self.get_user_id_from_input()
            message = self.library.loan_book(user_id, selected_book.unique_ISBN)
            tkinter.messagebox.showinfo("Loan Book", message)  # type: ignore
            self.search_books()  # Refresh the search results after loaning a book

    def get_user_id_from_input(self) -> int:
        """Get user ID input from the entry field.

        Returns:
            int: Id of user.
        """
        user_id = self.user_id_entry.get()
        return int(user_id)

    def search_books(self) -> None:
        """Search for book."""
        query = self.query_entry.get()
        selected_strategy = self.strategy_combobox.get()

        if selected_strategy == "Title":
            self.library.search_strategy = TitleSearchStrategy()
        elif selected_strategy == "Author":
            self.library.search_strategy = AuthorSearchStrategy()
        elif selected_strategy == "ISBN":
            self.library.search_strategy = ISBNSearchStrategy()
        elif selected_strategy == "Release Year":
            self.library.search_strategy = yearSearchStrategy()

        # Set the search strategy in the LibrarySystem instance
        self.library.search_strategy = self.library.search_strategy

        print("Search query:", query)
        # print("Books in library:", self.library.books)

        # Perform search using selected strategy
        search_results = list(
            self.library.search_books(query)
        )  # Only pass query argument
        self.display_search_results(search_results)

    def display_search_results(self, search_results: list[type[Book]]) -> None:
        """Display results of search.

        Args:
            search_results (list[Book]): Found books.
        """
        self.results_listbox.delete(0, tkinter.END)

        print("Received", len(search_results), "search results.")

        for book in search_results:
            print(
                "Displaying book:",
                book.title,
                "by",
                book.author,
                "(Release Year:",
                book.release_year,
                ")",
            )
            book_info = f"{book.title} by {book.author} ({book.release_year})"
            self.results_listbox.insert(tkinter.END, book_info)


if __name__ == "__main__":
    pass
