from itertools import combinations, chain
from collections import Counter


def find_pairs(shifts):
    """Функция составляет пары для каждой смены в переданном расписании"""
    return [get_a_combination(shift) for shift in shifts]


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


def print_timetables(timetables):
    """Распечатывает расписания"""
    for i, schedule in enumerate(timetables, 1):
        if len(timetables) > 1:
            print('Расписание №', i)
        print_schedule(schedule)


def print_schedule(schedule):
    """Распечатывает расписание"""
    for j, shift in enumerate(schedule, 1):
        print(str(j) + ')', *shift)
    print()


class Schedule:
    """Класс расписания который позволяет получать всю необходимую о нём информацию"""

    def __init__(self, shifts, identifier=0):
        # Список смен
        self.id = identifier
        # Список людей
        self.list_people = sorted(list(set(concatenate_lists(shifts))))
        # Список всех пар которые могут образовывать эти (объекты спика list people) люди
        self.all_pairs = get_a_combination(self.list_people)

        # Буфер в который сохраняются рабочие варианты расписаний
        self.tmp = []
        # Булевая переменная отвечает за состояние в плане изменения расписания
        self.changed = None

        # Вычисляемые свойсва класса:
        self.__shifts = shifts  # Они здесь для автоматического обновления всех ниже перечисленных свойств
        self.__couples_meeting_only_one_at_a_time = None  # Пары кол-во встреч которых = 1
        self.__couples_in_shifts = None  # Пары в каждой из смен
        self.__number_of_meetings = None  # Кол-во встреч каждой из пар
        self.__count_shifts = None  # Кол-во смен в расписании
        self.__unmet_couples = None  # Не встретившиеся пары
        self.__count_unmet = None  # Кол-во не встретившихся
        self.__unmet_people = None  # Не встретившиеся
        self.__shifts_with_unmet_people = None  # Смены в которых есть не встретившиеся
        self.__shortened_shifts = None  # Смены которые можно сократить

    @property
    def shifts(self):
        """Попугай"""
        self.update()
        return self.__shifts

    @shifts.setter
    def shifts(self, shifts):
        """Изменяет смены и обновляет выч. свойства"""
        self.__shifts = [shift[:] for shift in shifts]
        self.update()

    def update(self):
        """Затирает все посчитанные значения (чтоб они пересчитались)"""
        self.__couples_meeting_only_one_at_a_time = None
        self.__couples_in_shifts = None
        self.__number_of_meetings = None
        self.__count_shifts = None
        self.__unmet_couples = None
        self.__count_unmet = None
        self.__unmet_people = None
        self.__shifts_with_unmet_people = None
        self.__shortened_shifts = None

    def read(self):
        """Выводит расписание в консоль"""
        print_schedule(self.shifts)

    def save(self):
        """Сохраняет текущие смены"""
        self.tmp.append(self.shifts[:])

    def load(self, index=-1):
        """Восстанавливает сохранённое расписание"""
        self.shifts = [shift[:] for shift in self.tmp[index]] if len(self.tmp) else []

    def cut(self, index):
        """Занимается сокращением расписания"""
        print('Удаляю', index + 1, 'смену.')
        self.shifts.pop(index)

    def temp(self, index):
        """Возвращает копию объекта с удалённой сменой"""
        copy_shifts = [shift[:] for shift in self.shifts]
        temp = Schedule(copy_shifts, self.id + 1)
        temp.cut(index)
        return temp

    def change(self):
        """Занимается изменением расписания"""
        self.changed = False
        # Для каждой смены в которых есть люди из не встретившихся пар
        for index in self.shifts_with_unmet_people:
            self.change_shift(index)
            if self.changed:
                break

    def change_shift(self, index):
        """Пробует изменить смену"""
        # Список людей в данной смене которые образуют в Данной смене одиночные пары
        not_must_be_used = list(set(concatenate_lists(
            [pair for pair in self.couples_in_shifts[index] if pair in self.couples_meeting_only_one_at_a_time])))
        # Список людей которых будем пробовать заменить
        # (Исключаем тех которые в ДАННОЙ смене образуют единственную встречу)
        people = [human for human in self.shifts[index] if
                  human not in self.unmet_people and human not in not_must_be_used]
        # Список людей для замены
        people_for_replace = [human for human in self.unmet_people if human not in self.shifts[index]]

        # Для каждого из потенциально заменяемого
        for human in people:
            # Пробуем его заменить на одного из списка для замены
            for by_whom in people_for_replace:
                self.replace_a_person(index, human, by_whom)
                if self.changed:
                    break
            if self.changed:
                break

    def replace_a_person(self, index, human, on_whom):
        """Меняет одного на другого и проверяет уменьшилось ли кол-во не встретившихся, обновляет расписание"""
        test_shifts = [shift[:] for shift in self.shifts]
        test_shifts[index].pop(test_shifts[index].index(human))
        test_shifts[index].append(on_whom)
        test_shifts[index].sort()
        test_schedule = Schedule(test_shifts)
        if test_schedule.count_unmet < self.count_unmet:
            print('Изменяю в', index + 1, 'смене', human, 'на', on_whom)
            self.shifts = test_shifts
            self.changed = True

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
    def shortened_shifts(self):
        """Находит смены в которых меньше всего пар встречавшихся один раз"""
        if self.__shortened_shifts is None:
            # Кол-во пар в сменах которые встречались только один раз.
            table = [[self.number_of_meetings[pair] for pair in shift].count(1) for shift in self.couples_in_shifts]
            # Минимальное кол-во пар в сменах
            min_z = min(table)
            # Выбираем из неё те смены в которых таких пар минимально
            shift_numbers = [i for i, j in enumerate(table) if j == min_z]
            self.__shortened_shifts = shift_numbers
        return self.__shortened_shifts
