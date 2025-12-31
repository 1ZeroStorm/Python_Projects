
from db_setup import get_connection

def reading_books():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    for row in results:
        print(row)
    db.close()

def read_books_limit(n):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id <= %s", (n,))
    results = cursor.fetchall()
    db.close()
    return results


import tkinter as tk
from tkinter import messagebox, ttk


def show_all_books(tree):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    db.close()
    for i in tree.get_children():
        tree.delete(i)
    for row in results:
        tree.insert("", "end", values=row)

def run_books_query_ui():
    def query_books():
        id_val = entry_id.get()
        try:
            max_id = int(id_val)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return
        results = read_books_limit(max_id)
        for i in tree.get_children():
            tree.delete(i)
        for row in results:
            tree.insert("", "end", values=row)

    root = tk.Tk()
    root.title("Query Books by ID")
    tk.Label(root, text="Show books with ID <= ").grid(row=0, column=0, padx=10, pady=5)
    entry_id = tk.Entry(root, width=10)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
    tk.Button(root, text="Search", command=query_books).grid(row=0, column=2, padx=10, pady=5)
    tk.Button(root, text="Show All Data", command=lambda: show_all_books(tree)).grid(row=0, column=3, padx=10, pady=5)
    root.mainloop()

if __name__ == "__main__":
    run_books_query_ui()