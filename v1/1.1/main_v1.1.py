"""
В версии 1.1 будет добавленно:
Разделение обязанностей каждый файл занимается своим                -
Рефакторинг кода                                                    -
Работа с БД (сохранение и получение данных из внешнего файла)       -
Оптимизация...                                                      -

Структура кода:
1.Подключение к БД (создание)
2.Зопрос от пользователя инфы
3.Сверка с данными
4.Принятие решения
"""
import make_a_schedule as mas
import db_management as dbm


class Main:
    def __init__(self):
        # Подключение бд
        self.db = dbm.Main('database.db')  # input('Введите имя БД'))
        self.run()

    def run(self):
        while True:
            name = 'timetables_'+'_'.join([input('Введите кол-во человек: '), input('Введите кол-во человек в смене: ')])
            if name in self.db.get_names_tables():
                print('Такая запись уже существует')
            else:
                print('Такой записи не найденно, считаем...')
                number_of_people, people_in_shift = map(int, name.split('_')[1:])
                self.add_note(name, mas.calc(number_of_people, people_in_shift))
                print('Запись успешно добавленна.')

    def add_note(self, name, timetables):
        columns = ', '.join([f"shift_{i+1} text" for i in range(len(timetables[0]))])
        self.db.append_table(name, columns)
        self.db.add_data_to_table(name, timetables)


if __name__ == '__main__':
    Main()
