from db_setup import get_connection
from mysql.connector import Error as MySQLError
import pdb

def create_book(title, author, year):
    """Add a book with error handling and logging"""
    try:
        #pdb.set_trace() # breakpoint 1 - start debugging
        db = get_connection()
        print('Database connection established.')

        cursor = db.cursor()

        # cek input
        print(f"Input received - Title: {title}, Author: {author}, Year: {year}")
        #pdb.set_trace() # breakpoint 2 - before executing SQL

        sql = "INSERT INTO books (title, author, year_published) VALUES (%s, %s, %s)"
        val = (title, author, year)
        cursor.execute(sql, val)
        db.commit()

        print('Book added successfully:', title)
    except MySQLError as e:
        print('Failed to add book, please check input or connection:', e)
    except Exception as e:
        print('An unexpected error occurred:', e)
    finally:
        try:
            cursor.close()
            db.close()
            print('Database connection closed.')
        except Exception:
            pass

if __name__ == "__main__":
    create_book("Laskar Pelangi", "Andrea Hirata", 2005)
