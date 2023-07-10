import create_inputs

def check_possible_to_add_all_inputs_in_one_row(free_space: float, list_with_diametrs_float: list):
    '''
    Если все ввода помещаются, и расстояние между ними = 5 мм, то значит их можно вставить
    :param free_space: max(x,y)
    :param min_size: min(x,y)
    :param list_with_diametrs_float:[47.3,39.6]
    :return: True or False
    '''

    if free_space >= sum(list_with_diametrs_float) + 5 * (len(list_with_diametrs_float)-1):
        return True
    else:
        return False

def calculate_y_one_row(mid_of_width:float):
    '''
    Получение координаты y для установки в одну линию
    :param mid_of_width: ширина прямоугольника
    :return: y_coordinate
    '''
    y_coordinate = mid_of_width/2
    return y_coordinate

def find_start_of_rectangle_one_row(start_rectangle:float = None, diametr_float:float=None):
    '''
    Поиск старта начала следующего прямоугольника для зарисовки в одну линию
    :param start_rectangle: начало координаты предыдущего прямоугольника, если у первого, то все
    :param diametr_float: диаметр
    :return:
    '''
    if diametr_float == None:
        raise ValueError('Не задан диаметр для начала зоны сверловки find_start_of_rectangle_one_row')
    if start_rectangle == None:
        next_start_rectangle = diametr_float + 5
        return next_start_rectangle
    else:
        next_start_rectangle = start_rectangle +  diametr_float + 5
        return next_start_rectangle

def calculate_x_one_row(start_rectangle_for_paint:float = None, diametr_float:float=None):
    '''
    Получение координаты x для установки кабельного ввода
    :param start_rectangle_for_paint: Координата начала зоны сверления для данного уровня. получается так, что к предыдущему началу прибавляем диаметр и 5мм
    :param diametr_float: диаметр текущей окружности
    :return: x_coordinate
    '''
    if start_rectangle_for_paint ==None:
        raise ValueError('Не было предыдущей координаты')
    if diametr_float == None:
        raise ValueError('Не задан диаметр для получения координаты x')
    if start_rectangle_for_paint != None and diametr_float != None:
        x_coordinate = start_rectangle_for_paint + diametr_float/2
        return x_coordinate


def set_input_one_row(mid_of_width:float, x_coordinate:float = None, ):
    '''
    Установка ввода в одной линии
    :param mid_of_width: calculate_y_one_row
    :param x_coordinate: calculate_x_one_row
    :return:
    '''



while create_inputs.checking_clear_inputs_dict():
    if check_possible_to_add_all_inputs_in_one_row():



    '''Удаление кабельного ввода'''
    create_inputs.delete_input_from_dict()
    create_inputs.delete_diametr_from_list()