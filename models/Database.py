import os
import sqlite3
from tkinter.ttk import Treeview, Scrollbar
import sys

class Database:
    db_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "databases")
    db_name = os.path.join(db_folder, "hangman_2025.db")
    table_words = "words"

    def __init__(self):
        """Kontrollib ja loob andmebaasi, kui seda pole."""
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)

        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        """Loome tabelid, kui neid pole."""
        self.create_words_table()

        """Kontrollime, kas words tabel on tühi."""
        self.check_words_not_empty()

    def create_words_table(self):
        """Loob words tabeli, kui see puudub."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def check_words_not_empty(self):
        """Kontrollib, kas words tabelis on vähemalt üks kirje."""
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_words}")
        count = self.cursor.fetchone()[0]
        if count == 0:
            print("Words tabel on tühi! Võid lisada sõnu.")

    def add_word(self, word, category):
        """Lisab uue sõna ja kategooria."""
        self.cursor.execute("INSERT INTO words (word, category) VALUES (?, ?)", (word, category))
        self.conn.commit()

    def get_all_words(self):
        """Tagastab kõik sõnad andmebaasist."""
        self.cursor.execute("SELECT * FROM words ORDER BY category")
        return self.cursor.fetchall()

    def delete_word(self, word_id):
        """Kustutab sõna ID alusel."""
        self.cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
        self.conn.commit()

    def update_word(self, word_id, new_word, new_category):
        """Uuendab sõna ja kategooriat ID alusel."""
        self.cursor.execute("UPDATE words SET word = ?, category = ? WHERE id = ?", (new_word, new_category, word_id))
        self.conn.commit()

    def get_categories(self):
        """Tagastab kõik unikaalsed kategooriad."""
        self.cursor.execute("SELECT DISTINCT category FROM words")
        categories = [row[0] for row in self.cursor.fetchall()]
        categories.sort()
        categories.insert(0, "Vali kategooria")
        return categories

    def close(self):
        """Sulgeb andmebaasi ühenduse."""
        self.conn.close()


