"""Main script."""

from src.GUI.LibraryApp import LibraryApp


def main() -> None:
    """Run the main loop."""
    app = LibraryApp()  # type:ignore
    app.mainloop()


if __name__ == "__main__":
    main()
