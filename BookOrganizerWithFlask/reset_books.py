from db_setup import get_connection

def reset_books_table():
    """Delete all data from books table (TRUNCATE)"""
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE books")
    db.commit()
    db.close()
    print("All book data has been deleted.")

if __name__ == "__main__":
    response = input("Are you sure you want to delete ALL book data? (yes/no): ")
    if response.lower() == 'yes':
        reset_books_table()
    else:
        print("Operation cancelled.")
