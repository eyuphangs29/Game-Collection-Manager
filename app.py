import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'arel_proje_anahtari' # Session için gerekli [cite: 20]

def get_db_connection():
    # Ham SQL yönetimi için sqlite3 bağlantısı [cite: 26, 45]
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "Game Collection Manager Hazır!"

if __name__ == '__main__':
    app.run(debug=True)