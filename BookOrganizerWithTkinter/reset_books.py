
from db_setup import get_connection
import tkinter as tk
from tkinter import messagebox

def reset_books_table():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE books")
    db.commit()
    db.close()

def run_reset_books_ui():
    def confirm_and_reset():
        answer = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete ALL book data?")
        if answer:
            reset_books_table()
            messagebox.showinfo("Success", "All book data deleted!")

    root = tk.Tk()
    root.title("Reset Books Table")
    tk.Label(root, text="Delete ALL book data from the table:").pack(padx=20, pady=10)
    tk.Button(root, text="Reset Table", command=confirm_and_reset, fg="red").pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_reset_books_ui()