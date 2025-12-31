
from db_setup import get_connection
import tkinter as tk
from tkinter import messagebox, ttk

def delete_book(book_id):
    db = get_connection()
    cursor = db.cursor()
    sql = "DELETE FROM books WHERE id = %s"
    val = (book_id,)
    cursor.execute(sql, val)
    db.commit()
    db.close()

def get_books(search_text=None):
    db = get_connection()
    cursor = db.cursor()
    if search_text:
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", (f"%{search_text}%", f"%{search_text}%"))
    else:
        cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    db.close()
    return results

def run_delete_book_ui():
    def refresh_books():
        for i in tree.get_children():
            tree.delete(i)
        books = get_books(search_var.get())
        for row in books:
            tree.insert("", "end", values=row)

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "No book selected!")
            return
        for item in selected:
            book_id = tree.item(item, "values")[0]
            delete_book(book_id)
        refresh_books()
        messagebox.showinfo("Deleted", "Book(s) deleted!")

    root = tk.Tk()
    root.title("Delete Book")

    search_var = tk.StringVar()
    tk.Label(root, text="Search:").grid(row=0, column=0, padx=10, pady=5)
    search_entry = tk.Entry(root, textvariable=search_var, width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Search", command=refresh_books).grid(row=0, column=2, padx=10, pady=5)

    tree = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year"), show="headings", selectmode="extended")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    tk.Button(root, text="🗑 Delete Selected", command=on_delete, fg="red").grid(row=2, column=0, columnspan=3, pady=10)

    refresh_books()
    root.mainloop()

if __name__ == "__main__":
    run_delete_book_ui()