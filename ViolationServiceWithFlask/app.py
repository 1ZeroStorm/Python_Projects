from flask import Flask
import mysql.connector
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')

# DB configuration 
def get_db_config():
    return {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'violation_db'
    }

#get connection to sql
def get_connection(use_database=True):
    cfg = get_db_config()
    params = {
        'host': cfg['host'],
        'user': cfg['user'],
        'password': cfg['password'],
        'autocommit': False
    }
    if use_database:
        params['database'] = cfg['database']
    return mysql.connector.connect(**params)



def ensure_db():
    # create database if missing
    cfg = get_db_config()
    conn = get_connection(use_database=False)
    try:
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{cfg['database']}` DEFAULT CHARACTER SET utf8mb4")
        conn.commit()
    finally:
        cur.close()
        conn.close()

    # create table
    conn = get_connection(use_database=True)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS violations (
              id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(200) NOT NULL,
              absen VARCHAR(50),
              kelas VARCHAR(50),
              violation_type VARCHAR(100),
              reason TEXT
            ) 
            """
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()


# --- Wire up repository/service and register routes ---
from violation_repository import ViolationRepository
from violation_service import ViolationService
from views import register_routes

if __name__ == '__main__':
    ensure_db()  # Create database and tables if they don't exist
    repo = ViolationRepository(get_connection)
    service = ViolationService(repo)
    register_routes(app, service, repo)

    app.run(debug=True)