from update_book import run_update_book_ui
from delete_book import run_delete_book_ui
from read_books import run_books_query_ui
from search_book import run_search_book_ui
from reset_books import run_reset_books_ui
from create_book import run_create_book_ui
import tkinter as tk

def main_menu():
    root = tk.Tk()
    root.title("Book Management System")

    tk.Button(root, text="View All Books", command=run_books_query_ui, width=30).pack(pady=5)
    tk.Button(root, text="Search Books by Author", command=run_search_book_ui, width=30).pack(pady=5)
    tk.Button(root, text="Update Book Author", command=run_update_book_ui, width=30).pack(pady=5)
    tk.Button(root, text="Delete Book by ID", command=run_delete_book_ui, width=30).pack(pady=5)
    tk.Button(root, text="Reset Books Table", command=run_reset_books_ui, width=30, fg="red").pack(pady=5)
    tk.Button(root, text="Add New Book", command=run_create_book_ui, width=30).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit, width=30).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main_menu()