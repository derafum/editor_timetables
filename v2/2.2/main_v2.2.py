from get_schedule import get_schedule


def main(schedule):
    """Основной алгоритм"""
    while True:
        schedule.read()
        # Если все встретились
        if schedule.count_unmet == 0:
            # Сохраняем и сокращаем расписание
            schedule.save()
            schedule.cut()
        else:
            # Пробуем изменить расписание
            schedule.change()
            # Если не вышло
            if not schedule.changed:
                # Возвращаем последний рабочий вариант
                schedule.load()
                break
    return schedule.shifts


if __name__ == '__main__':
    print(main(get_schedule()))
