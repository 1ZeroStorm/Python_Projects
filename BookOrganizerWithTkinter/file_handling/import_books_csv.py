import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import csv
from db_setup import get_connection

def import_books_from_csv(file_path='importingFile.csv'):
    """Import book records from a CSV file.

    Parameters
    - file_path: path to the csv file (defaults to 'books_import.csv')

    Returns the number of records imported.
    """
    db = get_connection()
    cursor = db.cursor()

    inserted_count = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Expecting headers: title, author, year_published (case-sensitive)
            for row in reader:
                title = row.get('title') or row.get('Title')
                author = row.get('author') or row.get('Author')
                year = row.get('year_published') or row.get('year') or row.get('Year')
                if not title or not author:
                    # skip rows missing required fields
                    continue
                # try to coerce year to int if present
                if year:
                    try:
                        year_val = int(year)
                    except Exception:
                        year_val = None
                else:
                    year_val = None
                try:
                    cursor.execute(
                        "INSERT INTO books (title, author, year_published) VALUES (%s, %s, %s)",
                        (title, author, year_val)
                    )
                    inserted_count += 1
                except Exception as e:
                    # skip problematic rows but continue
                    print(f"Skipping row due to error: {e}")

        db.commit()
        print(f"Imported {inserted_count} books from {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    finally:
        db.close()
    return inserted_count
    
def run_import_ui():
    """Launch a small UI that lets the user choose a CSV and import it.

    This function is import-safe and can be called from other modules.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception:
        raise

    def choose_and_import():
        file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if not file_path:
            return
        count = import_books_from_csv(file_path)
        messagebox.showinfo('Import Complete', f'Imported {count} records from:\n{file_path}')

    root = tk.Tk()
    root.title('Import Books from CSV')
    tk.Label(root, text='Select a CSV file to import:').pack(padx=12, pady=8)
    tk.Button(root, text='Choose CSV & Import', command=choose_and_import).pack(pady=8)
    tk.Button(root, text='Close', command=root.destroy).pack(pady=4)
    root.mainloop()


if __name__ == "__main__":
    run_import_ui()