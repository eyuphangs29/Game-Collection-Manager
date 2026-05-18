import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for
from logic import validate_game_entry

app = Flask(__name__)
app.secret_key = 'arel_universitesi_proje_anahtari'

def get_db_connection():
    """Veritabanı bağlantısı kurar."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Ana Sayfa: Oyunları listeler."""
    username = session.get('username')
    user_id = session.get('user_id')
    games = []

    if user_id:
        db = get_db_connection()
        # US3: Kullanıcının oyunlarını ham SQL ile çekiyoruz
        games = db.execute('SELECT * FROM games WHERE user_id = ?', (user_id,)).fetchall()
        db.close()

    return render_template('index.html', username=username, games=games)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Kayıt olma mantığı."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            user = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            db.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş yapma mantığı."""
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
    """Oyun Ekleme: Form verilerini SQL ile kaydeder."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Formdan gelen veriler
    title = request.form.get('title')
    genre = request.form.get('genre')
    status = request.form.get('status')

    # Rating kontrolü
    rating_raw = request.form.get('rating')
    rating = int(rating_raw) if rating_raw and rating_raw.isdigit() else 0

    review_content = request.form.get('review', '')

    if not validate_game_entry(title, rating):
        return "Invalid data entry!", 400

    user_id = session['user_id']

    db = get_db_connection()
    # US2: Ham SQL sorgusu
    db.execute('''
        INSERT INTO games (user_id, title, genre, status, rating, review) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, title, genre, status, rating, review_content))
    db.commit()
    db.close()

    return redirect(url_for('index'))

@app.route('/delete_game/<int:game_id>')
def delete_game(game_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    db.execute('DELETE FROM games where id = ? AND user_id = ?',(game_id, session['user_id']))
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route('/update_status/<int:game_id>')
def update_status(game_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    game = db.execute('SELECT status FROM games WHERE id = ? AND user_id = ?',
                      (game_id, session['user_id'])).fetchone()
    if game:
        new_status = "Completed" if game['status'] == "Playing" else "Playing"
        db.execute('UPDATE games SET status = ? WHERE id = ? AND user_id = ?',
                   (new_status, game_id, session['user_id']))
        db.commit()

    db.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Çıkış yapma."""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)