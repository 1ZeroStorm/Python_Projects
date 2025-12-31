from db_setup import get_connection

def search_books_by_author(author):
    """Search books by author name"""
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE author = %s", (author,))
    results = cursor.fetchall()
    db.close()
    return results

if __name__ == "__main__":
    # Example: search for books by 'Andrea Hirata'
    results = search_books_by_author('Andrea Hirata')
    for row in results:
        print(row)
