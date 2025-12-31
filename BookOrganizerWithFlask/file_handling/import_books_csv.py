import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import csv
from db_setup import get_connection

def import_books_from_csv(file_path='importingFile.csv'):
    """Import book records from a CSV file.

    Parameters
    - file_path: path to the csv file (defaults to 'importingFile.csv')

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

if __name__ == "__main__":
    # Example: import from a CSV file
    # import_books_from_csv(r"C:\path\to\mybooks.csv")
    import_books_from_csv()
