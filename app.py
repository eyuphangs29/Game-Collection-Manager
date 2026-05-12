import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# Session verilerini şifrelemek için gerekli
app.secret_key = 'Arel_university_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    username = session.get("username")
    return render_template('index.html' , username = username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db_connection()
        try:
            # HOCANIN İSTEDİĞİ RAW SQL:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            # Kayıt başarılı olunca kullanıcıyı otomatik giriş yapmış sayalım (Session)
            session['username'] = username
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: This username is probably already taken. Details: {e}"
        finally:
            db.close()

        return render_template('register.html')

        # Çıkış yapma rotası (Session'ı temizler)
        @app.route('/logout')
        def logout():
            session.clear()
            return redirect(url_for('index'))

        if __name__ == '__main__':
            app.run(debug=True)