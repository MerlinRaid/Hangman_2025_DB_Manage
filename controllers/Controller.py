from tkinter import END, filedialog, messagebox
import os
import sqlite3
from models.Database import Database


class Controller:
    def __init__(self, model, view):
        """
        Kontrolleri konstruktor
        :param model: main-is loodud mudel
        :param view:  main-is loodud view
        """
        self.model = model
        self.view = view
        self.database = self.model.database

        # Sidumine nuppudega
        self.view.get_btn_add.config(command=self.add_word)
        self.view.get_btn_edit.config(command=self.edit_word)
        self.view.get_btn_delete.config(command=self.delete_word)
        self.view.get_btn_open_db.config(command=self.open_database)

        # Rippmenüü funktsionaalsus
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.combobox_change)

        # Laadime algandmed tabelisse
        self.refresh_table()

    def combobox_change(self, event=None):
        """Muudab kategooria valiku loogikat."""
        if self.view.get_combo_categories.current() > 0:
            self.view.get_txt_category.delete(0, END)
            self.view.get_txt_category.config(state='disabled')
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')
            self.view.get_txt_category.focus()

    def add_word(self):
        """Lisab uue sõna andmebaasi."""
        word = self.view.get_txt_word.get().strip()
        category = self.view.get_txt_category.get().strip()

        if self.view.get_combo_categories.current() > 0:
            category = self.view.get_combo_categories.get()

        if word and category:
            self.database.add_word(word, category)
            self.refresh_table()
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)
        else:
            messagebox.showwarning("Viga", "Sõna ja kategooria peavad olema täidetud!")

    def edit_word(self):
        """Redigeerib valitud sõna."""
        selected = self.view.get_my_table.selection()
        if not selected:
            messagebox.showwarning("Viga", "Palun vali sõna tabelist!")
            return

        word_id = self.view.get_my_table.item(selected)['values'][1]
        new_word = self.view.get_txt_word.get().strip()
        new_category = self.view.get_txt_category.get().strip()

        if self.view.get_combo_categories.current() > 0:
            new_category = self.view.get_combo_categories.get()

        if new_word and new_category:
            self.database.update_word(word_id, new_word, new_category)
            self.refresh_table()
        else:
            messagebox.showwarning("Viga", "Sõna ja kategooria peavad olema täidetud!")

    def delete_word(self):
        """Kustutab valitud sõna."""
        selected = self.view.get_my_table.selection()
        if not selected:
            messagebox.showwarning("Viga", "Palun vali sõna tabelist!")
            return

        word_id = self.view.get_my_table.item(selected)['values'][1]
        self.database.delete_word(word_id)
        self.refresh_table()

    def refresh_table(self):
        """Uuendab tabeli sisu."""
        for item in self.view.get_my_table.get_children():
            self.view.get_my_table.delete(item)

        words = self.database.get_all_words()
        for index, (word_id, word, category) in enumerate(words, start=1):
            self.view.get_my_table.insert('', 'end', values=(index, word_id, word, category))


    def open_database(self):
        """Avab kasutaja valitud andmebaasi ja kontrollib selle struktuuri."""

        # Ava vaikimisi databases kaust (või projekti juurkaust)
        initial_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "databases")

        filename = filedialog.askopenfilename(
            title="Vali andmebaasi fail",
            filetypes=[("SQLite DB", "*.db")],
            initialdir=initial_dir  # Määrame vaikimisi kausta
        )

        if filename:
            if os.path.exists(filename):
                self.database.db_name = filename
                self.database.conn = sqlite3.connect(self.database.db_name)
                self.database.cursor = self.database.conn.cursor()

                # Kontrollime, kas tabel "words" eksisteerib
                try:
                    self.database.cursor.execute("SELECT 1 FROM words LIMIT 1")
                except sqlite3.OperationalError:
                    messagebox.showerror("Viga", "Valitud andmebaas ei sisalda 'words' tabelit!")
                    return

                self.refresh_table()
            else:
                messagebox.showerror("Viga", "Valitud andmebaasi ei leitud!")