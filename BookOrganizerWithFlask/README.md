# Book Organizer — Flask + XAMPP (MySQL)

A simple Flask web application to manage a collection of books. Perform CRUD operations, search your library, and import/export book lists via CSV.

--

## Features
- Create, read, update, and delete books (CRUD)
- Search books by title, author, or year
- Import and export books using CSV
- Reset the database to its initial state
- Clean and user-friendly web interface

--

## Prerequisites
- Python 3.8 or newer
- XAMPP (MySQL) — make sure MySQL is running
- Python packages: `flask`, `mysql-connector-python` (install with pip)

## Quick start
1. Start MySQL from XAMPP.
2. Open the project folder in your IDE or terminal.
3. (Optional) Initialize the database and tables:

	```bash
	python db_setup.py
	```

4. Run the web app:

	```bash
	python app.py
	```

5. Copy the local address shown in the terminal (for example, `http://127.0.0.1:5000`) and open it in your browser.

You're ready to manage your book collection from the browser.