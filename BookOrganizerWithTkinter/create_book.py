
from db_setup import get_connection
from read_books import reading_books
from utils_logging import logger
from mysql.connector import Error as MySQLError

def create_book(title, author, year):
    """Add a book to the database with error handling and logging."""
    try:
        db = get_connection()
        print('Database connection established.')

        cursor = db.cursor()

        # log input
        print(f"Input received - Title: {title}, Author: {author}, Year: {year}")

        sql = "INSERT INTO books (title, author, year_published) VALUES (%s, %s, %s)"
        val = (title, author, year)
        cursor.execute(sql, val)
        db.commit()
        logger.info(f'Book added: {title}, {author}, {year}')

        print('Book successfully added:', title)
    except MySQLError as e:
        logger.error(f'Error adding book: {e}')
        print('Failed to add book — check input or database connection:', e)
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        print('An unexpected error occurred:', e)
    finally:
        try:
            cursor.close()
            db.close()
            print('Database connection closed.')
        except Exception:
            pass

# UI for adding a book
import tkinter as tk
from tkinter import messagebox

class BookEntryApp:
    def __init__(self, master):
        self.master = master
        master.title("Add New Book")

        tk.Label(master, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_title = tk.Entry(master, width=30)
        self.entry_title.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Author:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_author = tk.Entry(master, width=30)
        self.entry_author.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Year:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_year = tk.Entry(master, width=30)
        self.entry_year.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(master, text="Add Book", command=self.submit_book).grid(row=3, column=0, columnspan=2, pady=10)

    def submit_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        year = self.entry_year.get()
        if not title or not author or not year:
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            year_int = int(year)
        except ValueError:
            messagebox.showerror("Error", "Year must be a number!")
            return
        create_book(title, author, year_int)
        messagebox.showinfo("Success", f"Book '{title}' added!")
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)


def run_create_book_ui():
    root = tk.Tk()
    app = BookEntryApp(root)
    root.mainloop()

if __name__ == '__main__':
    run_create_book_ui()
