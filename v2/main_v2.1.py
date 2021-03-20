from itertools import combinations, chain
from collections import Counter
import csv


def find_pairs(shifts):
    """Функция составляет пары для каждой смены в переданном расписании"""
    return [get_a_combination(shift) for shift in shifts]


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


def concatenate_lists(lists):
    """Функция сцкпляет несколько списков в один"""
    return list(chain(*lists))


class Schedule:
    def __init__(self, people_in_total_and_in_shift, shifts):
        # Список смен
        self.shifts = shifts
        # Кол-во людей и кол-во людей в смене
        self.number_of_people, self.people_in_shift = people_in_total_and_in_shift
        # Список людей
        self.list_people = generation_list(self.number_of_people)
        # Список всех пар которые могут образовывать эти (объекты спика list people) люди
        self.all_pairs = get_a_combination(self.list_people)

        # Вычисляемые свойсва класса:
        self.__count_shifts = None
        self.__unmet_couples = None
        self.__count_unmet = None
        self.__unmet_people = None
        self.__shifts_with_unmet_people = None
        self.__abbreviated_shifts = None

    def update(self):
        """Затирает все посчитанные значения (чтоб они пересчитались)"""
        self.__count_shifts = None
        self.__unmet_couples = None
        self.__count_unmet = None
        self.__unmet_people = None
        self.__shifts_with_unmet_people = None
        self.__abbreviated_shifts = None

    def read(self):
        [print(shift) for shift in self.shifts]

    @property
    def count_shifts(self):
        if self.__count_shifts is None:
            self.__count_shifts = len(self.shifts)
        return self.__count_shifts

    @property
    def unmet_couples(self):
        """Возвращает пары которые не встретились"""
        # Кол-во встреч каждой из пар (словарь пара:кол-во)
        if self.__unmet_couples is None:
            number_of_meetings = count_elements(concatenate_lists(find_pairs(self.shifts)), self.all_pairs)
            self.__unmet_couples = [pair for pair, count in number_of_meetings.items() if count == 0]
        return self.__unmet_couples

    @property
    def count_unmet(self):
        """Считает количество невстретившихся пар"""
        if self.__count_unmet is None:
            self.__count_unmet = len(self.unmet_couples)
        return self.__count_unmet

    @property
    def unmet_people(self):
        """Находит не встретившихся людей, возвращает список этих людей"""
        if self.__unmet_people is None:
            self.__unmet_people = list(set(concatenate_lists(self.unmet_couples)))
        return self.__unmet_people

    @property
    def shifts_with_unmet_people(self):
        """Находит смены в которых содержатся не встретившиеся люди"""
        if self.__shifts_with_unmet_people is None:
            self.__shifts_with_unmet_people = list(
                set(i for i, shift in enumerate(self.shifts) for people in self.unmet_people if people in shift))
        return self.__shifts_with_unmet_people

    @property
    def abbreviated_shifts(self):
        """Считает какие смены можно сократить
        Находит смены в которых меньше всего пар встречавшихся 1 раз"""
        if self.__shifts_with_unmet_people is None:
            # Пары для каждой смены образовавшиеся в нашем (переданном в функцию) расписании
            couples_in_shifts = find_pairs(self.shifts)
            # Кол-во встреч каждой из пар (словарь пара:кол-во)
            number_of_meetings = count_elements(concatenate_lists(couples_in_shifts), self.all_pairs)
            # Таблица: Кол-во пар в сменах которые встречались только один раз.
            table = [[number_of_meetings[pair] for pair in shift].count(1) for shift in couples_in_shifts]
            # Выбираем из неё те смены в которых таких пар минимально
            shift_numbers = [i for i, j in enumerate(table) if j == min(table)]
            self.__shifts_with_unmet_people = shift_numbers
        return self.__shifts_with_unmet_people


class Main:
    def __init__(self):
        self.people_in_total_and_in_shift = [10, 6]
        # map(int, input('Введите количество человек: '), input('Введите количество человек в смене: '))

        self.name_file = ''  # input('Введите имя файла [имя по умолчанию: import]: ')
        self.name_file = '../data/import_10_6' if self.name_file == '' else self.name_file
        with open(self.name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            self.schedule = Schedule(self.people_in_total_and_in_shift, [list(map(int, row)) for row in reader])


if __name__ == '__main__':
    Main()
