CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    genre TEXT,
    status TEXT DEFAULT 'Playing',
    rating INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);