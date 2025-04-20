from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

UNCATEGORIZED_NAME = 'Uncategorized'

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    notes = db.relationship('Note', backref='section', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(300), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=True)

    def __repr__(self):
        return f'<Note {self.title}>'

def get_or_create_uncategorized():
    section = Section.query.filter_by(name=UNCATEGORIZED_NAME).first()
    if not section:
        section = Section(name=UNCATEGORIZED_NAME)
        db.session.add(section)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            section = Section.query.filter_by(name=UNCATEGORIZED_NAME).first()
    return section

@app.before_request
def create_tables():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        get_or_create_uncategorized()
        app.db_initialized = True

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        notes_text = request.form.get('notes', '')
        keywords = request.form.get('keywords', '')
        summary = request.form.get('summary', '')
        section_name = request.form.get('section', '').strip()
        section = None
        if section_name:
            section = Section.query.filter_by(name=section_name).first()
            if not section:
                section = Section(name=section_name)
                db.session.add(section)
                db.session.commit()
        new_note = Note(title=title, notes=notes_text, keywords=keywords, summary=summary, section=section)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('dashboard'))
    sections = Section.query.order_by(Section.name).all()
    notes_by_section = {section: section.notes for section in sections}
    return render_template('dashboard.html', notes_by_section=notes_by_section, sections=sections)

@app.route('/note/<int:note_id>', methods=['GET'])
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    sections = Section.query.order_by(Section.name).all()
    notes_by_section = {section: section.notes for section in sections}
    return render_template('dashboard.html', notes_by_section=notes_by_section, selected_note=note, sections=sections)

@app.route('/note/<int:note_id>/edit', methods=['POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    note.title = request.form['title']
    note.notes = request.form.get('notes', '')
    note.keywords = request.form.get('keywords', '')
    note.summary = request.form.get('summary', '')
    section_name = request.form.get('section', '').strip()
    if section_name:
        section = Section.query.filter_by(name=section_name).first()
        if not section:
            section = Section(name=section_name)
            db.session.add(section)
            db.session.commit()
        note.section = section
    else:
        note.section = None
    db.session.commit()
    return redirect(url_for('view_note', note_id=note.id))

@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/section/<int:section_id>/edit', methods=['POST'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)
    if section.name == UNCATEGORIZED_NAME:
        return redirect(url_for('dashboard'))
    new_name = request.form.get('new_name', '').strip()
    if new_name and new_name != UNCATEGORIZED_NAME:
        section.name = new_name
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/section/<int:section_id>/delete', methods=['POST'])
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    if section.name == UNCATEGORIZED_NAME:
        return redirect(url_for('dashboard'))
    uncategorized = get_or_create_uncategorized()
    for note in section.notes:
        note.section = uncategorized
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
