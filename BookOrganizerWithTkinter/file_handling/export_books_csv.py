import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import csv
from db_setup import get_connection

def export_books_to_csv(filename='books_export.csv', output_dir=None):
    """Export all book records to CSV.

    Parameters
    - filename: name of the csv file (defaults to 'books_export.csv')
    - output_dir: optional directory path where the file will be saved. If None,
      the current working directory is used.

    Returns the full path to the written file.
    """
    db = get_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
    else:
        path = filename

    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'author', 'year_published'])  # Header row
        writer.writerows(rows)

    cursor.close()
    db.close()
    print(f"Exported {len(rows)} books to {path}")
    return path


# --- Small UI to pick an export directory and run export (importable) ---
def run_export_ui():
    """Launch a tiny UI letting the user pick a folder and export the CSV there.

    This function is import-safe (you can import it and call run_export_ui() from
    another module).
    """
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception:
        raise

    def choose_and_export():
        folder = filedialog.askdirectory()
        if not folder:
            return
        out_path = export_books_to_csv(output_dir=folder)
        messagebox.showinfo("Export Complete", f"Exported to: {out_path}")

    root = tk.Tk()
    root.title("Export Books to CSV")
    tk.Label(root, text="Choose folder to save exported CSV:").pack(padx=12, pady=8)
    tk.Button(root, text="Choose Folder & Export", command=choose_and_export).pack(pady=8)
    tk.Button(root, text="Close", command=root.destroy).pack(pady=4)
    root.mainloop()


if __name__ == '__main__':
    run_export_ui()