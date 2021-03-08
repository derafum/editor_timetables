import sqlite3


class Table:
    """Класс для работы таблицой"""

    def __init__(self, con, name):
        self.name = name
        self.con = con
        self.cursor = con.cursor()

    def checking_for_existence(self):
        """Проверяет наличие таблицы в БД False - есть True - нет"""
        self.cursor.execute(f'SELECT NAME FROM sqlite_master WHERE NAME = "{self.name}"')
        return not len(self.cursor.fetchall()) == 0

    def get_columns_names(self):
        self.cursor.execute(f'SELECT * FROM {self.name}')
        return list(map(lambda x: x[0], self.cursor.description))

    def create(self, columns):
        """Создаёт таблицу"""
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.name}({columns})')
        self.con.commit()

    def delete(self):
        """Удаляет таблицу"""
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.name}')
        self.con.commit()

    def append(self, args, values):
        """Добавляет строку в таблицу (можно указать какие столбцы чем заполнять)
        args и values - должены быть в приведённом виде"""
        self.cursor.execute(f'INSERT INTO {self.name}({args}) VALUES({values})')
        self.con.commit()

    def update(self, args, values, identifier):
        """Обновленяет данные таблицы"""
        self.cursor.execute(f'UPDATE {self.name} SET {args} = {values} WHERE id = {identifier}')
        self.con.commit()

    def read_all(self, display):
        """Чтение таблицы"""
        if self.checking_for_existence():
            self.cursor.execute(f'SELECT * FROM {self.name}')
            rows = [' '.join(list(map(str, row))) for row in self.cursor.fetchall()]
            if display:
                [print(row) for row in rows]
            return rows


class Main:
    """Основной класс управления бд"""

    def __init__(self, name):
        self.name_data_base = name
        self.connection = self.sql_connection()
        self.cursor = self.connection.cursor()

    def sql_connection(self):
        """Подключение бд"""
        try:
            return sqlite3.connect(self.name_data_base)
        except sqlite3.Error:
            print(sqlite3.Error)

    def get_names_tables(self):
        """Список таблиц в бд"""
        self.cursor.execute('SELECT NAME FROM sqlite_master WHERE TYPE = "table"')
        return [name[0] for name in self.cursor.fetchall()]

    def append_table(self, name, columns):
        """Создаёт таблицу"""
        table = Table(self.connection, name)
        table.create(columns)

    def check_table(self, name):
        """Проверяет существование таблицы в бд"""
        table = Table(self.connection, name)
        return table.checking_for_existence()

    def add_data_to_table(self, name, data):
        table = Table(self.connection, name)
        columns = ', '.join(table.get_columns_names())
        for line in data:
            values = ', '.join(['"' + ','.join(map(str, i)) + '"' for i in line])
            table.append(columns, values)


if __name__ == '__main__':
    Main('database.db')
