from itertools import combinations, chain
from collections import Counter
import csv


def generation_list(total_person):
    """Создает список человек"""
    return [x + 1 for x in range(total_person)]


def count_elements(general_list, list_of_elements):
    """Считает количество переданных элементов в списке"""
    count = Counter(general_list)
    res = {i: count[i] for i in list_of_elements}
    return res


def get_a_combination(roll, count=2):
    """Составляет все пары для списка
    (также можно использовать для генерации любых других
    сочетаний указывая второй параметр)"""
    return list(combinations(roll, count))


def find_pairs(schedule):
    """Функция составляет пары для каждой смены в переданном расписании"""
    return [get_a_combination(shift) for shift in schedule]


def concatenate_lists(lists):
    """Функция сцкпляет несколько списков в один"""
    return list(chain(*lists))


class Main:
    def __init__(self):
        self.start()

    def debug(self):
        self.task = False  # self.task = True if input('Спрашивать ужимать дальше и какую смену удалять [y/n]: ') == 'y' else False
        self.number_of_people = 10  # self.number_of_people = int(input('Введите количество человек: '))
        self.people_in_shift = 6  # self.people_in_shift = int(input('Введите количество человек в смене: '))
        self.list_people = generation_list(self.number_of_people)

        self.name_file = '../data/import_10_6'  # input('Введите имя файла [имя по умолчанию: import]: ')
        self.name_file = 'import' if self.name_file == '' else self.name_file
        with open(self.name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            self.schedule = [list(map(int, row)) for row in reader]

        self.all_pairs = get_a_combination(self.list_people)
        self.all_shifts = get_a_combination(self.list_people, self.people_in_shift)
        self.schedule_list = []

        self.run(self.schedule)

    def start(self):
        self.task = True if input('Спрашивать ужимать дальше и какую смену удалять [y/n]: ') == 'y' else False
        self.number_of_people = int(input('Введите количество человек: '))
        self.people_in_shift = int(input('Введите количество человек в смене: '))
        self.list_people = generation_list(self.number_of_people)

        self.name_file = input('Введите имя файла [имя по умолчанию: import]: ')
        self.name_file = 'import' if self.name_file == '' else self.name_file
        with open(self.name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            self.schedule = [list(map(int, row)) for row in reader]

        self.all_pairs = get_a_combination(self.list_people)
        self.all_shifts = get_a_combination(self.list_people, self.people_in_shift)
        self.schedule_list = []

        self.run(self.schedule)

    def run(self, schedule):
        print('Начинаю ужимать расписание:')
        [print(i + 1, shift) for i, shift in enumerate(schedule)]
        print()
        # Основной алгоритм (ужатие)
        run = True
        while run:
            # Кол-во не встретившихся
            count_unmet = self.calc_count_unmet(schedule)

            # Если есть не встретившиеся пары
            if count_unmet != 0:
                # Пробуем изменять смены (пристаивая пары)
                changed = False
                # TODO
                # Список не встретившихся людей
                self.unmet_people = self.find_unmet_people(schedule)
                # Составляем список всех смен содержащих невстретившихся людей
                self.all_shifts_with_unmet_people = [self.all_shifts[i] for i in
                                                     self.find_shifts_with_unmet_people(self.all_shifts)]
                # Пробуем пристроить пару в одну из смен
                for index in range(len(schedule)):
                    # Пробуем уменьшить кол-во не встретившихся
                    test_schedule = self.change_shift(schedule, index)
                    # Если найденна смена с которой не встретившихся пар меньше меняем в расписании эту смену
                    if self.calc_count_unmet(test_schedule) < count_unmet:
                        schedule = test_schedule.copy()
                        changed = True
                        break
                if not changed:
                    if self.task:
                        print('Больше не могу изменять.')
                    run = False
            else:
                self.schedule_list.append(schedule.copy())
                if self.task:
                    [print(i + 1, shift) for i, shift in enumerate(schedule)]
                    if input('Ужимать? [y/n]: ') == 'y':
                        shift_index = self.calc_index_shifts(schedule)
                        if len(shift_index) > 1:
                            shift_index = int(input('Выберите одну из смен для удаления {}: '.format(
                                list(map(lambda x: x + 1, shift_index))))) - 1
                        else:
                            shift_index = shift_index[0]
                        print('Удаляю {} {} смену'.format(shift_index + 1, schedule.pop(shift_index)))
                    else:
                        break
                else:
                    shift_index = self.calc_index_shifts(schedule)[0]
                    schedule.pop(shift_index)
        # print('Список всех промежуточных состояний: {}'.format(self.schedule_list))
        print('Результат работы программы:')
        [print(i + 1, shift) for i, shift in enumerate(self.schedule_list[-1])]
        input('Для выхода из программы нажмите Enter')
        exit()

    def find_unmet(self, schedule):
        """Возвращает пары которые не встретились в полученном расписании"""
        # Кол-во встреч каждой из пар (словарь пара:кол-во)
        number_of_meetings = count_elements(list(chain(*find_pairs(schedule))), self.all_pairs)
        return [pair for pair, count in number_of_meetings.items() if count == 0]

    def calc_count_unmet(self, schedule):
        """Считает количество невстретившихся пар в расписании"""
        return len(self.find_unmet(schedule))

    def find_unmet_people(self, schedule):
        """Находит не встретившихся людей в переданом расписании, возвращает список этих людей"""
        return list(set(concatenate_lists(self.find_unmet(schedule))))

    def find_shifts_with_unmet_people(self, shifts):
        """Находит смены в которых содержатся не встретившиеся люди"""
        return list(set(i for i, shift in enumerate(shifts) for people in self.unmet_people if people in shift))

    def change_shift(self, schedule, index):
        """Функция перебирает все смены содержащие невстретившихся людей для выбранной и заменяет на ту в которой кол-во невстретившихся меньше"""
        # TODO
        test_schedule = schedule.copy()
        test_schedule.pop(index)
        for shift in self.all_shifts_with_unmet_people:
            new_schedule = test_schedule.copy()
            new_schedule.insert(index, shift)
            if self.calc_count_unmet(new_schedule) < self.calc_count_unmet(schedule):
                return new_schedule
        return schedule

    def calc_index_shifts(self, schedule):
        """Считает какие смены можно сократить в переданом ей расписании
        Находит смены в которых меньше всего пар встречавшихся минимальное кол-во раз"""
        # Пары для каждой смены образовавшиеся в нашем (переданном в функцию) расписании
        couples_in_shifts = find_pairs(schedule)
        # Кол-во встреч каждой из пар (словарь пара:кол-во)
        number_of_meetings = count_elements(concatenate_lists(couples_in_shifts), self.all_pairs)
        # Таблица: Кол-во пар в сменах которые встречались только один раз.
        table = [[number_of_meetings[pair] for pair in shift].count(1) for shift in couples_in_shifts]
        # Выбираем из неё те смены в которых таких пар минимально
        shift_numbers = [i for i, j in enumerate(table) if j == min(table)]
        return shift_numbers

    def save_to_file(self):
        """Функция сохраняет данные в файл"""
        pass


if __name__ == '__main__':
    Main()
