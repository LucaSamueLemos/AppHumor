import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mood.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Tabela de registros de humor
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                emotion TEXT NOT NULL,
                notes TEXT,
                chat_history TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    # Operações de usuário
    def create_user(self, username, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        return cursor.fetchone()

    # Operações de registros
    def save_mood_entry(self, user_id, emotion, notes, chat_history):
        cursor = self.conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO mood_entries (user_id, date, emotion, notes, chat_history)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date, emotion, notes, chat_history))
        self.conn.commit()

    def get_month_entries(self, user_id, year, month):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT date, emotion, notes 
            FROM mood_entries 
            WHERE user_id = ? 
            AND strftime('%Y', date) = ? 
            AND strftime('%m', date) = ?
        ''', (user_id, f"{year:04}", f"{month:02}"))
        return cursor.fetchall()