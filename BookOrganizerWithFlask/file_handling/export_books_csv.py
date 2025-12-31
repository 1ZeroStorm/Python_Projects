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

if __name__ == '__main__':
    # Example: export to current directory
    export_books_to_csv()
    
    # Example: export to specific directory
    # export_books_to_csv(output_dir=r"C:\path\to\folder")
