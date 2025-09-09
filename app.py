from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "youtube_manager.db"

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        time TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = "dev-secret-for-local"  # change for production

@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    videos = conn.execute('SELECT * FROM videos ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', videos=videos)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        time = request.form.get('time','').strip()
        if not name:
            flash('Name is required', 'error')
            return redirect(url_for('add'))
        conn = get_db_connection()
        conn.execute('INSERT INTO videos (name, time) VALUES (?, ?)', (name, time))
        conn.commit()
        conn.close()
        flash('Video added', 'success')
        return redirect(url_for('index'))
    return render_template('add_edit.html', action='Add', video=None)

@app.route('/edit/<int:video_id>', methods=['GET','POST'])
def edit(video_id):
    conn = get_db_connection()
    video = conn.execute('SELECT * FROM videos WHERE id = ?', (video_id,)).fetchone()
    if not video:
        conn.close()
        flash('Video not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name','').strip()
        time = request.form.get('time','').strip()
        if not name:
            flash('Name is required', 'error')
            return redirect(url_for('edit', video_id=video_id))
        conn.execute('UPDATE videos SET name = ?, time = ? WHERE id = ?', (name, time, video_id))
        conn.commit()
        conn.close()
        flash('Video updated', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('add_edit.html', action='Edit', video=video)

@app.route('/delete/<int:video_id>', methods=['POST'])
def delete(video_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM videos WHERE id = ?', (video_id,))
    conn.commit()
    conn.close()
    flash('Video deleted', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
