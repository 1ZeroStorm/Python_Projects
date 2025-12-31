# Book Organizer — Tkinter + MySQL

A small desktop application built with Tkinter to manage a personal book collection. Supports adding, viewing, searching, updating, deleting, importing/exporting, and resetting the books table (MySQL).

--

## Features
- Add, view, update, and delete books (CRUD)
- Search books by author or title
- Export and import (CSV) utilities (see `file_handling`)
- Reset the books table to its initial state
- Simple desktop GUI using Tkinter

--

## Prerequisites
- Python 3.8 or newer
- MySQL (XAMPP or standalone) running on `localhost`
- Python packages: `mysql-connector-python`
- `tkinter` (usually included with standard Python)

Install the Python dependency with pip:

```bash
pip install mysql-connector-python
```

## Quick start
1. Start your MySQL server (for example, start MySQL from XAMPP).
2. (Optional) Initialize the database and tables:

   ```bash
   python db_setup.py
   ```

3. Run the application main menu:

   ```bash
   python main.py
   ```

4. Use the GUI to add, view, search, update, or delete books.

## Notes
- The app logs to `app.log` in the project directory.
- GUI windows are individual dialogs; use the main menu (`main.py`) to open features.

