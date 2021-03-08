import sqlite3


class Table:
    def __init__(self, con, name):
        self.name = name
        self.con = con
        self.cursor = con.cursor()

    def checking_for_existence(self):
        """Проверяет наличие таблицы в БД False - есть True - нет"""
        self.cursor.execute(f'SELECT NAME FROM sqlite_master WHERE NAME = "{self.name}"')
        return not len(self.cursor.fetchall()) == 0

    def create(self, columns):
        """Создаёт таблицу"""
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.name}(id integer PRIMARY KEY, {columns})')
        self.con.commit()

    def delete(self):
        """Удаляет таблицу"""
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.name}')
        self.con.commit()

    def append(self, args, values):
        """Добавляет строку в таблицу (можно указать какие столбцы чем заполнять)
        args и values - должены быть в приведённом виде"""
        print(values)
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
    def __init__(self):
        self.name_data_base = 'database.db'
        self.connection = self.sql_connection()
        self.cursor = self.connection.cursor()
        table = Table(self.connection, 'timetables_6_10')
        schedule = [
            [1, 2, 3, 6, 7, 8],
            [1, 2, 4, 5, 7, 9],
            [1, 3, 5, 6, 9, 10],
            [2, 4, 6, 7, 8, 10],
            [3, 4, 5, 6, 8, 9]]
        args = ', '.join([f"shift_{i+1} text" for i in range(len(schedule))])
        if not table.checking_for_existence():
            table.create(args)
        # table.append(args)
        table.read_all(True)


    def sql_connection(self):
        """ Подключение бд"""
        try:
            print("БД успешно подключенна")
            return sqlite3.connect(self.name_data_base)
        except sqlite3.Error:
            print(sqlite3.Error)

    def sql_get_all_names_tables(self):
        """Список таблиц в бд"""
        self.cursor.execute('SELECT NAME FROM sqlite_master WHERE TYPE = "table"')
        print(self.cursor.fetchall())


if __name__ == '__main__':
    Main()
