from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('journal.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS entries
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        date TEXT NOT NULL)''')

init_db()

@app.route('/')
def index():
    with sqlite3.connect('journal.db') as conn:
        entries = conn.execute('SELECT * FROM entries').fetchall()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect('journal.db') as conn:
            conn.execute('INSERT INTO entries (title, content, date) VALUES (?, ?, ?)', (title, content, date))
        return redirect(url_for('index'))
    return render_template('add_entry.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    with sqlite3.connect('journal.db') as conn:
        entry = conn.execute('SELECT * FROM entries WHERE id = ?', (entry_id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect('journal.db') as conn:
            conn.execute('UPDATE entries SET title = ?, content = ?, date = ? WHERE id = ?', (title, content, date, entry_id))
        return redirect(url_for('index'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete/<int:entry_id>')
def delete_entry(entry_id):
    with sqlite3.connect('journal.db') as conn:
        conn.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
