# Notetaker App

## Purpose
The Notetaker App is a web-based note-taking dashboard designed for organizing and managing notes for an online software engineering course. It allows users to create, view, edit, and delete notes, and group them by course sections (categories). Each note can include a title, detailed notes, keywords, and a summary. Sections can be managed, and notes can be moved between sections. The app is built with Flask, uses SQLite for storage, and supports database migrations with Flask-Migrate.

## Features
- Create, view, edit, and delete notes
- Group notes by section (category)
- Edit and delete sections (except 'Uncategorized')
- Move notes to 'Uncategorized' when a section is deleted
- Responsive dashboard UI with sidebar navigation
- Database migrations with Flask-Migrate

## Usage

### 1. Clone the repository
```
git clone https://github.com/NeoSkosana/notetaker-app.git
cd notetaker-app
```

### 2. Set up a virtual environment (recommended)
```
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set up the database
Initialize migrations (only once):
```
flask db init
```
Generate migration for the current models:
```
flask db migrate -m "Initial migration"
```
Apply the migration:
```
flask db upgrade
```

### 5. Run the app
```
python app.py
```
Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Project Structure
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates (dashboard.html)
- `static/` - Static files (CSS, JS)
- `migrations/` - Database migration scripts
- `instance/notes.db` - SQLite database file

## License
This project is open source and available under the MIT License.
