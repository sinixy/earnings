import sqlite3

from models.enums import RoleEnum


class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_user(self, user_id: int, role: int = RoleEnum.USER):
        if user := self.get_user(user_id):
            return
        if role not in [RoleEnum.USER, RoleEnum.ADMIN]:
            raise ValueError('Invalid role')
        self.cursor.execute("INSERT INTO users VALUES (?, ?)", (user_id, role))
        self.connection.commit()

    def get_user(self, user_id: int):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

db = Database('database.db')


if __name__ == '__main__':
    from config import RECEIVER_ID
    db.cursor.execute('''CREATE TABLE "users" (
        "user_id"	INTEGER NOT NULL UNIQUE,
        "role"	INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY("user_id")
    );''')
    db.connection.commit()
    db.create_user(RECEIVER_ID, role=RoleEnum.ADMIN)