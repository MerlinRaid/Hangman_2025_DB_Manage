from models.Database import Database

class Model:
    def __init__(self):
        self.database = Database()

    def get_categories(self):
        return self.database.get_categories()

    @property
    def categories(self):
        return self.get_categories()
