
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'king_yuvi_secret'

def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username mryuvi,
                password yuviking,
                approved INTEGER DEFAULT 0
            )
        ''')

@app.route('/')
def home():
    if 'user' in session:
        username = session['user']
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT approved FROM users WHERE username=?", (username,))
            result = cur.fetchone()
            if result and result[0] == 1:
                return render_template("dashboard.html", user=username)
            else:
                return render_template("not_approved.html")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            if user:
                session['user'] = username
                return redirect(url_for('home'))
            else:
                return render_template("login.html", error="❌ Invalid credentials")
    return render_template("login.html", error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return render_template("register.html", message="✅ Registered! Wait for admin approval.")
        except sqlite3.IntegrityError:
            return render_template("register.html", message="❌ Username already exists")
    return render_template("register.html", message=None)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/admin/users')
def admin_users():
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, approved FROM users")
        users = cur.fetchall()
    html = "<h2>Admin – Manage Users</h2><ul>"
    for uid, uname, appr in users:
        status = "✅" if appr else "❌"
        action = "" if appr else f"<a href='/admin/approve/{uid}'>Approve</a>"
        html += f"<li>{uname} — {status} {action}</li>"
    html += "</ul><p><a href='/logout'>Back</a></p>"
    return html

@app.route('/admin/approve/<int:user_id>')
def approve_user(user_id):
    with sqlite3.connect('users.db') as conn:
        conn.execute("UPDATE users SET approved=1 WHERE id=?", (user_id,))
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
