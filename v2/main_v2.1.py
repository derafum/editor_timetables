from itertools import combinations, chain
from collections import Counter


class Schedule:
    def __init__(self, people_in_total_and_in_shift, shifts):
        # Список смен
        self.shifts = shifts
        # Кол-во людей и кол-во людей в смене
        self.number_of_people, self.people_in_shift = people_in_total_and_in_shift
        # Список людей
        self.list_people = self.generation_list(self.number_of_people)
        # Список всех пар которые могут образовывать эти (объекты спика list people) люди
        self.all_pairs = self.get_a_combination(self.list_people)

    @property
    def unmet(self):
        """Возвращает пары которые не встретились в полученном расписании"""
        # Кол-во встреч каждой из пар (словарь пара:кол-во)
        number_of_meetings = self.count_elements(self.concatenate_lists(self.find_pairs()), self.all_pairs)
        return [pair for pair, count in number_of_meetings.items() if count == 0]

    @property
    def count_unmet(self):
        """Считает количество невстретившихся пар в расписании"""
        return len(self.unmet)

    @property
    def unmet_people(self):
        """Находит не встретившихся людей в переданом расписании, возвращает список этих людей"""
        return list(set(self.concatenate_lists(self.unmet)))

    @property
    def shifts_with_unmet_people(self):
        """Находит смены в которых содержатся не встретившиеся люди"""
        return list(set(i for i, shift in enumerate(self.shifts) for people in self.unmet_people if people in shift))

    @property
    def abbreviated_shifts(self):
        """Считает какие смены можно сократить в переданом ей расписании
        Находит смены в которых меньше всего пар встречавшихся минимальное кол-во раз"""
        # Пары для каждой смены образовавшиеся в нашем (переданном в функцию) расписании
        couples_in_shifts = self.find_pairs()
        # Кол-во встреч каждой из пар (словарь пара:кол-во)
        number_of_meetings = self.count_elements(self.concatenate_lists(couples_in_shifts), self.all_pairs)
        # Таблица: Кол-во пар в сменах которые встречались только один раз.
        table = [[number_of_meetings[pair] for pair in shift].count(1) for shift in couples_in_shifts]
        # Выбираем из неё те смены в которых таких пар минимально
        shift_numbers = [i for i, j in enumerate(table) if j == min(table)]
        return shift_numbers

    def find_pairs(self):
        """Функция составляет пары для каждой смены в переданном расписании"""
        return [self.get_a_combination(shift) for shift in self.shifts]

    @staticmethod
    def generation_list(total_person):
        """Создает список человек"""
        return [x + 1 for x in range(total_person)]

    @staticmethod
    def count_elements(general_list, list_of_elements):
        """Считает количество переданных элементов в списке"""
        count = Counter(general_list)
        res = {i: count[i] for i in list_of_elements}
        return res

    @staticmethod
    def get_a_combination(roll, count=2):
        """Составляет все пары для списка
        (также можно использовать для генерации любых других
        сочетаний указывая второй параметр)"""
        return list(combinations(roll, count))

    @staticmethod
    def concatenate_lists(lists):
        """Функция сцкпляет несколько списков в один"""
        return list(chain(*lists))


if __name__ == '__main__':
    pass
