from time import time
import sys

# Режим отладки
DEBUG = True

# Использовать временный файл для сохранения временных результатов
use_temp_file = True
name_temp_file = 'temp_' + str(round(time())) + '.txt'
view_temp_file = False

# Выполнять перебор всех возможных вариантов удаления смен
consider_all_deletion_options = True

# ===================Отображение работы=======================
display_work = False

display_delete = True  # Показывать удаление смен
display_change = True  # Показывать изменение смен
display_cant_change = True  # Показывать моменты когда изменять больше не получается
display_all_meet = True  # Показывать когда все встретились
display_variants_for_delete = True  # Показывать варианты для удаления смен
display_consideration_of_disposal_options = True  # Показывать ход перебора удаления различных смен

sys.setrecursionlimit(10 ** 9)
