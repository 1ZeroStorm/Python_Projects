from flask import Flask, render_template, request, redirect, send_file, flash
from create_book import create_book
from read_books import read_books
from update_book import update_author
from delete_book import delete_book
from search_books import search_books_by_author
from reset_books import reset_books_table
from file_handling.export_books_csv import export_books_to_csv
from file_handling.import_books_csv import import_books_from_csv
from db_setup import setup_database
import os

# Get the directory where app.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize Flask with template folder set to current directory
app = Flask(__name__, template_folder=current_dir)
app.secret_key = "supersecretkey"  # untuk flash message

# ---
# HOME_PAGE
# ---
@app.route("/")
def home():
    return render_template("home.html")

# ---
# LIST & ADD BOOKS
# ---
@app.route("/books")
def books():
    data = read_books()
    return render_template("books.html", books=data)

@app.route("/add", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    create_book(title, author, int(year))
    return redirect("/books")

# ---
# DELETE BOOK
# ---
@app.route("/delete/<int:id>")
def delete(id):
    delete_book(id)
    return redirect("/books")

# ---
# EDIT BOOK
# ---
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        new_author = request.form["author"]
        update_author(id, new_author)
        return redirect("/books")
    
    return render_template("edit_books.html", id=id)

# ---
# SEARCH BOOKS
# ---
@app.route("/search")
def search():
    keyword = request.args.get("author", "")
    if keyword:
        results = search_books_by_author(keyword)
    else:
        results = []
    return render_template("search.html", results=results, keyword=keyword)

# ---
# EXPORT CSV
# ---
@app.route("/export")
def export():
    try:
        # Export to current directory
        filepath = export_books_to_csv(filename='books_export.csv', output_dir=current_dir)
        # Send the file to the user for download
        return send_file(filepath, as_attachment=True, download_name='books_export.csv')
    except Exception as e:
        flash(f"Export failed: {e}", "danger")
        return redirect("/books")

# ---
# IMPORT CSV
# ---
@app.route("/import", methods=["GET", "POST"])
def import_csv():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected", "danger")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "danger")
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            filename = "temp_upload.csv"
            file.save(filename)
            try:
                import_books_from_csv(filename)
                flash("Import successful!", "success")
            except Exception as e:
                flash(f"Import failed: {e}", "danger")
            finally:
                if os.path.exists(filename):
                    os.remove(filename)
            return redirect("/books")
        else:
            flash("File must be a CSV", "danger")
            return redirect(request.url)
    
    return render_template("import_page.html")

# ---
# RESET DATA
# ---
@app.route("/reset")
def reset():
    reset_books_table()
    flash("All data has been reset!", "warning")
    return redirect("/")

if __name__ == "__main__":
    # Setup database jika belum ada
    setup_database()
    app.run(debug=True)