import csv
from db_setup import get_connection

def import_books_from_csv(filepath):
    db = get_connection()
    cursor = db.cursor()
    
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                title = row.get("title")
                author = row.get("author")
                
                # Flexible: bisa baca 'year' ATAU 'year_published'
                year = row.get("year_published") or row.get("year") or None
                
                # Cek kolom wajib
                if not title or not author:
                    print(f"SKIP Data tidak valid: {row}")
                    continue
                
                # Cek apakah sudah ada
                cursor.execute("SELECT id FROM books WHERE title=%s", (title,))
                if cursor.fetchone():
                    print(f"SKIP '{title}' sudah ada")
                    continue
                
                cursor.execute("""
                    INSERT INTO books (title, author, year_published)
                    VALUES (%s, %s, %s)
                """, (title, author, year))
        
        db.commit()
        print("[IMPORT] Import selesai tanpa error")
        
    except Exception as e:
        print("[IMPORT ERROR]: ", e)
        
    finally:
        cursor.close()
        db.close()