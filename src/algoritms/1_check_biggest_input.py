
'''
########################
ДАННЫЕ НА ВХОД
########################
'''


def check_unreal_input(min_size_of_surface: float,
                       max_diam_from_side: float):
    '''
    Проверка на возможность установки кабельного ввода в оболочку
    :param min_size_of_surface: Для прямоугольника-большая сторона прямоугольника, для 8угольника, max(Y2-Y1, X2-X0)

    :param max_diam_from_side:
    :return: True or False
    '''
    if min_size_of_surface == max(min_size_of_surface, max_diam_from_side):
        return True
    else:
        return False

if __name__ == '__main__':
    list_with_diametrs = [40, 80, 20, 10, 13, 65, 41]

    rectangle_x, rectrangle_y = 200, 80

    min_size_of_surface = min(rectangle_x, rectrangle_y)
    max_diam_from_side = max(list_with_diametrs)

    one = check_unreal_input(min_size_of_surface=min_size_of_surface,
                       max_diam_from_side=max_diam_from_side)
    print(one)