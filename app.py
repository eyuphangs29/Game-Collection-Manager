import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# Hocanın istediği 'Sessions & Cookies' için gizli anahtar şart
app.secret_key = 'arel_universitesi_proje_anahtari'


def get_db_connection():
    # Ham SQL (Raw SQL) yönetimi için sqlite3 bağlantısı
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Verilere isimle (user['id'] gibi) erişmek için
    return conn


@app.route('/')
def index():
    # Session içinde username var mı diye bakıyoruz
    username = session.get('username')
    return render_template('index.html', username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        try:
            # HOCANIN ŞARTI: Raw SQL INSERT
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            # Kayıt sonrası otomatik login yapalım
            session['username'] = username
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: Username might be taken. Details: {e}"
        finally:
            db.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db_connection()
        # HOCANIN ŞARTI: Raw SQL SELECT
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                          (username, password)).fetchone()
        db.close()

        if user:
            # Session verilerini dolduruyoruz
            session['username'] = user['username']
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return "Invalid username or password!"

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Session'ı temizleyerek çıkış yaptırıyoruz
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)