import mysql.connector

def get_connection():
    return  mysql.connector.connect(
        host = 'localhost',
        user='root',
        password='',
        database='library_db'
    ) 

def setup_database():
    db = mysql.connector.connect(
        host = 'localhost',
        user='root',
        password=''
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    db.close()

    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   title VARCHAR(100),
                   author VARCHAR(50),
                   year_published YEAR
                   )    
    """)
    db.close()
        print("Database and tables are ready to use")

if __name__ == "__main__":
    setup_database()