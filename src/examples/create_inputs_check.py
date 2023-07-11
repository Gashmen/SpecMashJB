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


def set_coordinate_one_row(y_coordinate:float, x_coordinate:float = None, ):
    '''
    Установка ввода в одной линии
    :param y_coordinate: Координата вставки y кабельного ввода calculate_y_one_row
    :param x_coordinate: calculate_x_one_row
    :return: [x,y]
    '''
    coordinate_input = [x_coordinate, y_coordinate]
    return coordinate_input

def set_input_name(dict_with_inputs_name_and_diam:dict[int:dict[str:float]], count:int):
    '''
    Выдача имени данного кабельного ввода
    :param dict_with_inputs_name_and_diam: {0:{ВЗ-Н50:25}, 1:{ВЗ-Н40, 20},...
    :param count: 0
    :return: ВЗ-Н50
    '''
    if dict_with_inputs_name_and_diam is not None:
        if hasattr(dict_with_inputs_name_and_diam, str(count)):
            name_of_input = dict_with_inputs_name_and_diam[count]
            return name_of_input
        else:
            raise ValueError('Отсутсвует аттрибут count в set_input_name')
    else:
        raise ValueError('Отсутсвует словарь dict_with_inputs_name_and_diam в set_input_name')

def build_dict_one_row(input_name:str, coordinate_input:list[float,float]):
    '''
    Создает словарь имя и координаты
    :param input_name:ВЗ-Н50
    :param coordinate_input:[x,y]
    :return:{ВЗ-Н50:[x,y]}
    '''
    dict_one_row = {input_name:coordinate_input}
    return dict_one_row

def find_start_of_rectangle_many_row()



def build_main_dict(main_dict:dict, count:int,dict_one_row:dict[str:list[float,float]]):
    '''
    Добавление в main dict нового участника
    :param main_dict: главный словарь заранее созданный
    :param count:0
    :param dict_one_row:{ВЗ-Н50:[x,y]}  build_dict_one_row
    :return:{0:{ВЗ-Н50:[x,y]},...}
    '''

    if hasattr(main_dict,str(count)) is False:
        main_dict[count] = dict_one_row
    else:
        raise ValueError('Уже добавлено значение под этим count   build_main_dict')


dict_with_all_info_from_start = dict_with_inputs_name_and_diam.copy()
count_input = 0
main_dict = dict()

while create_inputs.checking_clear_inputs_dict():
    if check_possible_to_add_all_inputs_in_one_row():
        if count_input == 0:
            start_rectangle = 0
        else:
            start_rectangle = find_start_of_rectangle_one_row()

        set_coordinate_one_row(y_coordinate=calculate_y_one_row(),
                          x_coordinate= calculate_x_one_row())

        set_input_name()
        build_dict_one_row()
        build_main_dict()
        count_input+=1
        dict_with_inputs_name_and_diam.pop(count_input,None)

    else:
        '''
        Нужно сделать уровни для дальнейшей работы
        level: int просто как count, но касающийся только width
        
        {level: {start_rectangle: x_coordinate,end_rectangle:x_coordinate + diam + 5, 0:{ВЗ-Н50:[x,y]},1:{ВЗ-Н40:[x,y]} }
        
        '''


        level = 0
        if count_input == 0:
            start_rectangle = 0
        else:
            start_rectangle = find_start_of_rectangle_one_row()














    '''Удаление кабельного ввода'''
    create_inputs.delete_input_from_dict()
    create_inputs.delete_diametr_from_list()