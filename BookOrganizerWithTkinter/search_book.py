from db_setup import get_connection

import tkinter as tk
from tkinter import messagebox, ttk

def search_books_by_author(author):
	db = get_connection()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM books WHERE author = %s", (author,))
	results = cursor.fetchall()
	db.close()
	return results

def run_search_book_ui():
	def query_books():
		author_val = entry_author.get()
		if not author_val:
			messagebox.showerror("Error", "Please enter an author name!")
			return
		results = search_books_by_author(author_val)
		for i in tree.get_children():
			tree.delete(i)
		for row in results:
			tree.insert("", "end", values=row)

	root = tk.Tk()
	root.title("Search Books by Author")
	tk.Label(root, text="Author:").grid(row=0, column=0, padx=10, pady=5)
	entry_author = tk.Entry(root, width=30)
	entry_author.grid(row=0, column=1, padx=10, pady=5)
	tk.Button(root, text="Search", command=query_books).grid(row=0, column=2, padx=10, pady=5)

	tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year"), show="headings")
	tree.heading("ID", text="ID")
	tree.heading("Title", text="Title")
	tree.heading("Author", text="Author")
	tree.heading("Year", text="Year")
	tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

	root.mainloop()

if __name__ == "__main__":
	run_search_book_ui()
