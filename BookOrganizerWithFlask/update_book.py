from db_setup import get_connection

def update_author(book_id, new_author):
    """Update author for a book by ID"""
    db = get_connection()
    cursor = db.cursor()
    sql = "UPDATE books SET author = %s WHERE id = %s"
    val = (new_author, book_id)
    cursor.execute(sql, val)
    db.commit()
    print(f'Book with id {book_id} successfully updated.')
    db.close()

if __name__ == "__main__":
    # Example: update book id 1 with new author
    update_author(1, "New Author Name")
