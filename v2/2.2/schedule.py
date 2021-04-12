from itertools import combinations, chain
from collections import Counter


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
    """Класс расписания который позволяет получать всю необходимую о нём информацию"""

    def __init__(self, people_in_total_and_in_shift, shifts):
        # Список смен
        self.shifts = shifts[:]
        # Кол-во людей и кол-во людей в смене
        self.number_of_people, self.people_in_shift = people_in_total_and_in_shift
        # Список людей
        self.list_people = generation_list(self.number_of_people)
        # Список всех пар которые могут образовывать эти (объекты спика list people) люди
        self.all_pairs = get_a_combination(self.list_people)

        # Буфер в который сохраняются рабочие варианты расписаний
        self.tmp = []
        # Булевая переменная отвечает за состояние в плане изменения расписания
        self.changed = False

        # Вычисляемые свойсва класса:
        self.__couples_meeting_only_one_at_a_time = None  # Пары кол-во встреч которых = 1
        self.__couples_in_shifts = None  # Пары в каждой из смен
        self.__number_of_meetings = None  # Кол-во встреч каждой из пар
        self.__count_shifts = None  # Кол-во смен в расписании
        self.__unmet_couples = None  # Не встретившиеся пары
        self.__count_unmet = None  # Кол-во не встретившихся
        self.__unmet_people = None  # Не встретившиеся
        self.__shifts_with_unmet_people = None  # Смены в которых есть не встретившиеся
        self.__shifts_in_which_the_number_of_pairs_met_once_is_minimal = None  # Смены которые можно сократить

    def update(self, shifts):
        """Затирает все посчитанные значения (чтоб они пересчитались) и обновляет смены"""
        self.shifts = shifts[:]
        self.__couples_meeting_only_one_at_a_time = None
        self.__couples_in_shifts = None
        self.__number_of_meetings = None
        self.__count_shifts = None
        self.__unmet_couples = None
        self.__count_unmet = None
        self.__unmet_people = None
        self.__shifts_with_unmet_people = None
        self.__shifts_in_which_the_number_of_pairs_met_once_is_minimal = None

    def read(self):
        """Выводит расписание в консоль"""
        [print(', '.join(map(str, shift))) for shift in self.shifts]
        print()

    def save(self):
        """Сохраняет текущие смены"""
        self.tmp.append(self.shifts[:])

    def load(self):
        """Восстанавливает последнее сохранённое расписание"""
        self.shifts = self.tmp[-1][:]

    def cut(self):
        """Занимается сокращением расписания"""
        # TODO Придумать как выбрать единственно верную смену под сокращение
        # Сокращаем первую смену из списка смен под сокращение
        shifts = self.shifts[:]
        shifts.pop(self.shifts_in_which_the_number_of_pairs_met_once_is_minimal[0])
        self.update(shifts)

    def change(self):
        """Занимается изменением расписания"""
        print(self.unmet_couples)
        self.changed = False
        index = self.shifts_in_which_the_number_of_pairs_met_once_is_minimal[0]
        people_for_change = self.list_people[:]
        shift = self.shifts[index]
        remaining_shifts = self.shifts[:]
        remaining_shifts.pop(index)
        [people_for_change.pop(people_for_change.index(people)) for people in shift if
         people in self.unmet_people and people in people_for_change]
        pairs = [pair for pair in self.couples_in_shifts[index] if pair in self.couples_meeting_only_one_at_a_time]
        [people_for_change.pop(people_for_change.index(people)) for people in set(concatenate_lists(pairs)) if
         people in people_for_change]
        people_under_change = set(people_for_change) & set(shift)
        print(index, shift)
        print(people_under_change, people_for_change)
        for u in people_under_change:
            for f in people_for_change:
                test_shift = shift[:]
                test_shift.pop(test_shift.index(u))
                test_shift.append(f)
                test_shift.sort()
                print(remaining_shifts + [test_shift])
                test_schedule = Schedule([self.number_of_people, self.people_in_shift],
                                         remaining_shifts + [test_shift])
                test_schedule.read()
                print('*', test_schedule.count_unmet, self.count_unmet)
                if test_schedule.count_unmet < self.count_unmet:
                    self.changed = True
                    self.update(test_schedule.shifts[:])
                    break

    @property
    def count_shifts(self):
        """Кол-во пар в расписании"""
        if self.__count_shifts is None:
            self.__count_shifts = len(self.shifts)
        return self.__count_shifts

    @property
    def unmet_couples(self):
        """Пары которые не встретились"""
        # Кол-во встреч каждой из пар (словарь пара:кол-во)
        if self.__unmet_couples is None:
            number_of_meetings = count_elements(concatenate_lists(find_pairs(self.shifts)), self.all_pairs)
            self.__unmet_couples = [pair for pair, count in number_of_meetings.items() if count == 0]
        return self.__unmet_couples

    @property
    def count_unmet(self):
        """Количество невстретившихся пар"""
        if self.__count_unmet is None:
            self.__count_unmet = len(self.unmet_couples)
        return self.__count_unmet

    @property
    def unmet_people(self):
        """Список не встретившиеся людей"""
        if self.__unmet_people is None:
            self.__unmet_people = list(set(concatenate_lists(self.unmet_couples)))
        return self.__unmet_people

    @property
    def shifts_with_unmet_people(self):
        """Смены в которых содержатся не встретившиеся люди"""
        if self.__shifts_with_unmet_people is None:
            self.__shifts_with_unmet_people = list(
                set(i for i, shift in enumerate(self.shifts) for people in self.unmet_people if people in shift))
        return self.__shifts_with_unmet_people

    @property
    def couples_meeting_only_one_at_a_time(self):
        """Пары которые встречались только один раз"""
        if self.__couples_meeting_only_one_at_a_time is None:
            self.__couples_meeting_only_one_at_a_time = [pair for pair in self.all_pairs if
                                                         self.number_of_meetings[pair] == 1]
        return self.__couples_meeting_only_one_at_a_time

    @property
    def couples_in_shifts(self):
        """Пары для каждой смены образовавшиеся в нашем расписании"""
        if self.__couples_in_shifts is None:
            self.__couples_in_shifts = find_pairs(self.shifts)
        return self.__couples_in_shifts

    @property
    def number_of_meetings(self):
        """Кол-во встреч каждой из пар (словарь пара:кол-во)"""
        if self.__number_of_meetings is None:
            self.__number_of_meetings = count_elements(concatenate_lists(self.couples_in_shifts), self.all_pairs)
        return self.__number_of_meetings

    @property
    def shifts_in_which_the_number_of_pairs_met_once_is_minimal(self):
        """Находит смены в которых меньше всего пар встречавшихся один раз"""
        if self.__shifts_in_which_the_number_of_pairs_met_once_is_minimal is None:
            # Кол-во пар в сменах которые встречались только один раз.
            table = [[self.number_of_meetings[pair] for pair in shift].count(1) for shift in self.couples_in_shifts]
            # Минимальное кол-во пар в сменах
            min_z = min(table)
            # Выбираем из неё те смены в которых таких пар минимально
            shift_numbers = [i for i, j in enumerate(table) if j == min_z]
            self.__shifts_in_which_the_number_of_pairs_met_once_is_minimal = shift_numbers
        return self.__shifts_in_which_the_number_of_pairs_met_once_is_minimal
