from db_setup import get_connection

def delete_book(book_id):
    """Delete a book by ID"""
    db = get_connection()
    cursor = db.cursor()
    sql = "DELETE FROM books WHERE id = %s"
    val = (book_id,)
    cursor.execute(sql, val)
    db.commit()
    db.close()
    print(f"Book with id {book_id} successfully deleted.")

def get_books(search_text=None):
    """Get all books, optionally filtered by title or author"""
    db = get_connection()
    cursor = db.cursor()
    if search_text:
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s", (f"%{search_text}%", f"%{search_text}%"))
    else:
        cursor.execute("SELECT * FROM books")
    results = cursor.fetchall()
    db.close()
    return results

if __name__ == "__main__":
    # Example: delete book with id 1
    delete_book(1)
