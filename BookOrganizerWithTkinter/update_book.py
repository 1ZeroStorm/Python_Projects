from db_setup import get_connection
from read_books import reading_books
from search_book import run_search_book_ui

def update_author(book_id, new_author):
    db = get_connection()
    cursor = db.cursor()
    sql = "UPDATE books SET author = %s WHERE id = %s"
    val = (new_author, book_id)
    cursor.execute(sql, val)
    db.commit()
    print('Book with id', book_id, 'successfully updated.')
    db.close()


import tkinter as tk
from tkinter import messagebox

def run_update_book_ui():
    def update():
        book_id = entry_id.get()
        new_author = entry_author.get()
        if not book_id or not new_author:
            messagebox.showerror("Error", "Both fields are required!")
            return
        try:
            book_id_int = int(book_id)
        except ValueError:
            messagebox.showerror("Error", "Book ID must be a number!")
            return
        update_author(book_id_int, new_author)
        messagebox.showinfo("Success", f"Book ID {book_id_int} author updated!")
        entry_id.delete(0, tk.END)
        entry_author.delete(0, tk.END)

    root = tk.Tk()
    root.title("Update Book Author")
    tk.Label(root, text="Book ID:").grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(root, width=10)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(root, text="New Author:").grid(row=1, column=0, padx=10, pady=5)
    entry_author = tk.Entry(root, width=30)
    entry_author.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Update Author", command=update).grid(row=2, column=0, columnspan=2, pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_update_book_ui()