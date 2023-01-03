import sqlite3

class BotDB:

    def __init__(self, db_file) -> None:
        """Инициализация соединения с БД"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверка, есть ли юзер в БД"""
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Получение id пользователя в базе по его user_id в телеграме"""
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        """Добавление пользователя в БД"""
        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        """Добавление записи о доходе/расходе в БД"""
        self.cursor.execute("INSERT INTO 'records' ('user_id', 'operation', 'value') VALUES (?, ?, ?)",
            (self.get_user_id(user_id),
            operation == '+',
            value))
        return self.conn.commit()

    def get_records(self, user_id, within = '+'):
        """Получение истории операций за определенный период"""

        if (within == 'day'):
            result = self.cursor.execute("SELECT * FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))

        elif (within == 'week'):
            result = self.cursor.execute("SELECT * FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))

        elif (within == 'month'):
            result = self.cursor.execute("SELECT * FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))

        elif (within == 'year'):
            result = self.cursor.execute("SELECT * FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of year') AND datetime('now', 'localtime') ORDER BY 'date'",
                self.get_user_id(user_id))

        else:
            result = self.cursor.execute("SELECT * FROM 'records' WHERE 'user_id' = ? ORDER BY 'date'",
                self.get_user_id(user_id))
    
        return result.fetchall()

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()