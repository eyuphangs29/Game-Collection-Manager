import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'arel_universitesi_proje_anahtari'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    username = session.get('username')
    user_id = session.get('user_id')
    games = []

    # US3: Eğer kullanıcı giriş yapmışsa, sadece onun oyunlarını getir
    if user_id:
        db = get_db_connection()
        games = db.execute('SELECT * FROM games WHERE user_id = ?', (user_id,)).fetchall()
        db.close()

    return render_template('index.html', username=username, games=games)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            # Kayıt sonrası otomatik login
            user = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        except:
            return "Username already exists!"
        finally:
            db.close()
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                          (username, password)).fetchone()
        db.close()
        if user:
            session['username'] = user['username']
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        return "Invalid credentials!"
    return render_template('login.html')


@app.route('/add_game', methods=['POST'])
def add_game():
    # US2: Yeni oyun ekleme mantığı
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    genre = request.form['genre']
    status = request.form['status']
    user_id = session['user_id']

    db = get_db_connection()
    db.execute('INSERT INTO games (user_id, title, genre, status) VALUES (?, ?, ?, ?)',
               (user_id, title, genre, status))
    db.commit()
    db.close()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)