from db_setup import get_connection

def read_books():
    """Display all books from database"""
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    for row in results:
        print(row)
    db.close()
    return results

def read_books_limit(n):
    """Get all books with id <= n"""
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id <= %s", (n,))
    results = cursor.fetchall()
    db.close()
    return results

if __name__ == "__main__":
    read_books()
