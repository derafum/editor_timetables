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
        self.changed = None

        # Вычисляемые свойсва класса:
        self.__couples_meeting_only_one_at_a_time = None  # Пары кол-во встреч которых = 1
        self.__couples_in_shifts = None  # Пары в каждой из смен
        self.__number_of_meetings = None  # Кол-во встреч каждой из пар
        self.__count_shifts = None  # Кол-во смен в расписании
        self.__unmet_couples = None  # Не встретившиеся пары
        self.__count_unmet = None  # Кол-во не встретившихся
        self.__unmet_people = None  # Не встретившиеся
        self.__shifts_with_unmet_people = None  # Смены в которых есть не встретившиеся
        self.__shortened_shifts = None  # Смены которые можно сократить

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
        self.__shortened_shifts = None

    def read(self):
        """Выводит расписание в консоль"""
        [print(str(i) + ')', ' '.join(map(str, shift))) for i, shift in enumerate(self.shifts, 1)]
        print()

    def save(self):
        """Сохраняет текущие смены"""
        self.tmp.append(self.shifts[:])

    def load(self, index=-1):
        """Восстанавливает сохранённое расписание"""
        self.shifts = self.tmp[index][:]

    def cut(self):
        """Занимается сокращением расписания"""
        # TODO Придумать как выбрать единственно верную смену под сокращение
        # Сокращаем первую смену из списка смен под сокращение
        shifts = self.shifts[:]
        shifts.pop(self.shortened_shifts[0])
        print('Удаляю', self.shortened_shifts[0] + 1, 'смену.')
        self.update(shifts)

    def change(self):
        """Занимается изменением расписания"""
        self.changed = False
        # Для каждой смены в которых есть люди из не встретившихся пар
        for index in self.shifts_with_unmet_people:
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
                    self.change_shift(index, human, by_whom)
                    if self.changed:
                        break
                if self.changed:
                    break
            if self.changed:
                break

    def change_shift(self, index, human, by_whom):
        """Меняет одного на другого и проверяет удачно ли это изменение"""
        # print(index, human, by_whom)
        test_shifts = [shift[:] for shift in self.shifts[:]]
        test_shifts[index].pop(test_shifts[index].index(human))
        test_shifts[index].append(by_whom)
        test_shifts[index].sort()
        test_schedule = Schedule([self.number_of_people, self.people_in_shift], test_shifts)
        if test_schedule.count_unmet < self.count_unmet:
            print('Изменяю', index + 1, 'смену', self.shifts[index], 'на', test_shifts[index])
            self.update(test_shifts[:])
            self.changed = True

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
