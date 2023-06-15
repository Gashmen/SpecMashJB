import ezdxf
import random
'''https://www.notion.so/di258/1-7ea0c37847564504aae770e297247076'''

'''1'''
def create_points_of_drill_surface(doc,
                                   side=None,
                                   shell_name=None) -> dict[str:list]:
    '''
    Возвращает точки зоны сверловки
    :param doc: doc в котором сделан импорт оболочки
    :param side: leftside,rightside,upside,downside
    :param shell_name:VP.161610
    :return:{'x':[2,5,8,10],'y':[0,1,2]}
    '''
    return_dict = {'x': [], 'y': []}
    if '_' not in side:
        side = '_' + side

    block_name = shell_name + side
    if block_name in [i.dxf.name for i in doc.blocks]:
        lwpolyline = doc.blocks[block_name].query('LWPOLYLINE')[0]

        if lwpolyline:
            for xy_coordinate in lwpolyline.get_points():
                return_dict['x'].append(round(xy_coordinate[0], 2))
                return_dict['y'].append(round(xy_coordinate[1], 2))

            return_dict['x'] = tuple(sorted(set(return_dict['x'])))
            return_dict['y'] = tuple(sorted(set(return_dict['y'])))
            return return_dict
    else:
        return None

'''2'''
def return_max_possible_diametr_on_surface(dict_coordinates: dict) -> float:
    '''
    Определение максимального размера для вставки кабельного ввода
    :param dict_coordinates: {'x':[2,5,8,10],'y':[0,1,2]} или {'x':[8,10],'y':[0,1]}
    :return: 8
    '''
    if dict_coordinates != None:
        max_x = dict_coordinates['x'][-1] - dict_coordinates['x'][0]
        max_y = dict_coordinates['y'][-1] - dict_coordinates['y'][-2]

        return min(max_x, max_y)
    else:
        return None

def return_diametr_from_name(dict_all_names_dict: {str: float}, name_input: str) -> float:
    '''
    Возвращает значение диаметра
    :param dict_all_names_dict:{'': None, 'ВЗ-Н12': 31.9, 'ВЗ-Н16': 36.2, 'ВЗ-Н20': 39.6, 'ВЗ-Н25': 47.3, 'ВЗ-Н25/Р': 47.3, 'ВЗ-Н32': 53.6, 'ВЗ-Н32/Р': 53.6, 'ВЗ-Н40': 64.9, 'ВЗ-Н50': 72.8, 'ВЗ-Н63': 84.3, 'ВЗ-Н75': 97.6, 'ВЗ-Н75А': 99.6, 'ВЗ-Н90': 112.6, 'ВЗ-Н90А': 119.6, 'ВЗ-Н90В': 119.6, 'ВЗ-Н100': 132.6, 'ВЗ-Н100А': 132.6, 'ВЗ-Н100В': 132.6, 'ВЗ-Н16-МР12': 36.2, 'ВЗ-Н20-МР15': 39.6, 'ВЗ-Н20-МР16': 40.6, 'ВЗ-Н20-МР18': 41.6, 'ВЗ-Н20-МР20': 42.6, 'ВЗ-Н20-МР22': 43.6, 'ВЗ-Н20-МР25': 44.6, 'ВЗ-Н25-МР18': 49.3, 'ВЗ-Н25-МР20': 50.3, 'ВЗ-Н25-МР22': 51.3, 'ВЗ-Н25-МР25': 52.3, 'ВЗ-Н25-МР32': 53.3, 'ВЗ-Н32-МР25': 53.6, 'ВЗ-Н32-МР32': 54.6, 'ВЗ-Н32-МР38': 55.6, 'ВЗ-Н40-МР38': 64.9, 'ВЗ-16Н-Т3/8G(B)': 36.2, 'ВЗ-16Н-Т1/2G(B)': 36.2, 'ВЗ-20Н-Т1/2G(B)': 39.6, 'ВЗ-20Н-Т3/4G(B)': 39.6, 'ВЗ-25Н-Т3/4G(B)': 47.3, 'ВЗ-25Н-Т1G(B)': 47.3, 'ВЗ-32Н-Т1G(B)': 53.6, 'ВЗ-32Н-Т1.1/4G(B)': 53.6, 'ВЗ-40Н-Т1.1/4G(B)': 64.9, 'ВЗ-40Н-Т1.1/2G(B)': 64.9, 'ВЗ-50Н-Т1.1/2G(B)': 72.8, 'ВЗ-50Н-Т2G(B)': 72.8, 'ВЗ-Б16': 36.2, 'ВЗ-Б20': 39.6, 'ВЗ-МБ20': 39.6, 'ВЗ-Б25': 47.3, 'ВЗ-МБ25': 47.3, 'ВЗ-МБ25/Р': 47.3, 'ВЗ-Б32': 53.6, 'ВЗ-МБ32': 53.6, 'ВЗ-МБ32/Р': 53.6, 'ВЗ-Б40': 64.9, 'ВЗ-МБ40': 64.9, 'ВЗ-Б50': 72.8, 'ВЗ-Б63': 84.3, 'ВЗ-Б75': 97.6, 'ВЗ-Б75А': 99.6, 'ВЗ-Б90': 112.6, 'ВЗ-Б90В': 112.6, 'ВЗ-П20': 39.6, 'ВЗ-П20А': 39.6, 'ВЗ-П20В': 39.6, 'ВЗ-П32': 53.6, 'ВЗ-П32А': 53.6, 'ВЗ-П32В': 53.6, 'ВЗ-К20': 42.6, 'ВЗ-К25': 49.6, 'ВЗ-К32': 59.2, 'ВЗ-К40': 75.8}
    :param name_input:'ВЗ-Н20'
    :return:39.6
    '''

    return dict_all_names_dict[name_input]


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

'''3'''
def define_rectangle_size_for_inputs(dict_with_x_y_coordinates: dict[str:list]):
    '''
    Определение размеров прямоугольника
    :param dict_with_x_y_coordinates: {'x':[2,5,8,10],'y':[0,1,2]}
    :return:{'xy0': [0,0], 'xy1': [10,40]}
    '''
    return_dict = {}
    return_dict['xy0'] = [dict_with_x_y_coordinates['x'][0], dict_with_x_y_coordinates['y'][-2]]
    return_dict['xy1'] = [dict_with_x_y_coordinates['x'][-1], dict_with_x_y_coordinates['y'][-1]]
    return return_dict


'''4'''
# Проверка помещаются ли в один ряд все кабельнные вводы.
def check_possible_to_add_all_inputs_in_one_row(max_size: float, list_with_diametrs_float: list):
    '''
    Если все ввода помещаются, и расстояние между ними = 5 мм, то значит их можно вставить
    :param max_size: max(x,y)
    :param min_size: min(x,y)
    :param list_with_diametrs_float:[47.3,39.6]
    :return: True or False
    '''
    check_max_size = max_size

    if len(list_with_diametrs_float) == 1:
        check_max_size -= list_with_diametrs_float[0]
    else:
        for count, diametr in enumerate(list_with_diametrs_float):
            if count == 0:
                check_max_size -= diametr
            elif count == len(list_with_diametrs_float)-1:
                check_max_size -= diametr
            else:
                check_max_size -= diametr
    #Если между каждым вводом есть расстояние больше 5мм, то все ок
    if check_max_size > 5 * len(list_with_diametrs_float)-1:
        return check_max_size
    else:
        return False

'''5'''
def paint_circle_one_row(x0, y0, min_size: float, list_with_diametrs_float: list) -> list:
    '''
    Выдаем координаты диаметров в соответсвие с тем, что list_with_diametrs уже отсортирован и получается
    выходной list будет иметь индексы такие же, как диаметр окружности

    :param max_size: max(x,y)
    :param min_size: min(x,y)
    :param list_with_diametrs_float: sorted(list_with_diametrs_float): [31,30,29,27]
    :return: [[0,10],[10,10]...
    '''
    return_list = list()

    if len(list_with_diametrs_float) == 1:
        return_list.append([x0 + list_with_diametrs_float[0] / 2, y0 + min_size / 2])

    else:
        for count_diametr, diametr in enumerate(list_with_diametrs_float):
            # Если первый ввод, то его поставить вначале
            if count_diametr == 0:
                return_list.append([x0 + (list_with_diametrs_float[0] / 2), y0+(min_size / 2)])
            # Если последний, то ставим вначале
            elif count_diametr == len(list_with_diametrs_float) - 1:
                return_list.append([return_list[-1][0] + (list_with_diametrs_float[count_diametr-1]/2) + (list_with_diametrs_float[count_diametr] / 2),
                                    y0+(min_size / 2)])
            else:
                return_list.append([return_list[-1][0] + (list_with_diametrs_float[count_diametr-1]/2) + (list_with_diametrs_float[count_diametr] / 2),
                                    y0+(min_size / 2)])

    return return_list

'''6'''
def move_inputs_one_row(coordinate_insert_input:list, free_length:float,max_size:float ):
    '''
    Двигаем input относительно того, сколько свободного места осталось
    :param coordinate_insert_input: [[0.10], [57.7,10]]
    :param free_length: 10 - Это оставшаяся длина после вставки всех inputs
    :return: [[0.10], [57.7,10]] - координаты также
    '''

    if len(coordinate_insert_input) == 1:
        coordinate_insert_input[0][0] = round(max_size/2,2)
    else:
        for count,coordinates in enumerate(coordinate_insert_input):
            coordinates[0] = round(coordinates[0] + (free_length) * ((count+1)/(len(coordinate_insert_input)+1)),2)
    return coordinate_insert_input

'''7'''
'''Объединение полученных результатов'''
def return_inputs_dict_with_coordinate(sorted_list_diametr_russian:list, coordinate:list)->dict[int:dict[str:list[float]]]:

    '''
    Возвращаем главный словарь, необходимый для создания input на чертеже в ui
    :param sorted_list_diametr_russian: ['ВЗ-Н32', 'ВЗ-Н25', 'ВЗ-Н20']
    :param coordinate: [[22.6, 39.88], [60.00000000000001, 39.88], [97.4, 39.88]]
    :return: {0: {'ВЗ-Н25': [32.11666666666667, 37.5]}, 1: {'ВЗ-Н25': [87.88333333333333, 37.5]}

    '''
    return_dict = {}
    for count,diametr_russian_name in enumerate(sorted_list_diametr_russian):
        return_dict[count] = {diametr_russian_name:coordinate[count]}
    return return_dict


'''Удаление /Р в название'''
def delete_extended_input(russian_input_name:str)->str:
    '''
    Удалить в название расширенный кабельнный ввод
    :param russian_input_name: 'ВЗ-Н32/Р'
    :return:'ВЗ-Н32'
    '''
    if russian_input_name != None:
        if '/Р' in russian_input_name:
            return russian_input_name.replace('/Р', '')
        else:
            return russian_input_name

'''Изменение имени стороны оболочки'''
def define_side(side_russian_name:str)->str:
    '''
    Получаем название rightside,leftside
    :param side_russian_name: А,Б,В,Г
    :return: rightside
    '''
    if side_russian_name != None:
        if "А" == side_russian_name:
            return 'upside'
        elif "Б" == side_russian_name:
            return 'rightside'
        elif "В" == side_russian_name:
            return 'downside'
        elif "Г" == side_russian_name:
            return 'leftside'
        else:
            return side_russian_name

'''Сортировка диаметров по русскому имени '''
def sort_list_diametr_russian(list_with_diametr_russian:list, dict_with_name_diametr:dict):
    '''
    Отсортировка списка с русскими именами вводов
    :param list_with_diametr_russian:['ВЗ-Н25', 'ВЗ-Н32','ВЗ-Н20']
    :param dict_with_name_diametr:{'': None, 'ВЗ-Н12': 31.9, 'ВЗ-Н16': 36.2, 'ВЗ-Н20': 39.6, 'ВЗ-Н25': 47.3...
    :return: ['ВЗ-Н32', 'ВЗ-Н25','ВЗ-Н20']
    '''

    list_with_sorted_names = sorted(list_with_diametr_russian, key=lambda x:dict_with_name_diametr[x],reverse=True)
    return list_with_sorted_names

''''''



if __name__ == "__main__":

    doc_base = 'C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf'
    full_name_dim = {'': None, 'ВЗ-Н12': 21.9, 'ВЗ-Н16': 26.2, 'ВЗ-Н20': 29.6, 'ВЗ-Н25': 37.3, 'ВЗ-Н25/Р': 37.3,
                     'ВЗ-Н32': 43.6, 'ВЗ-Н32/Р': 43.6, 'ВЗ-Н40': 54.9, 'ВЗ-Н50': 62.8, 'ВЗ-Н63': 74.3,
                     'ВЗ-Н75': 87.6, 'ВЗ-Н75А': 89.6, 'ВЗ-Н90': 102.6, 'ВЗ-Н90А': 109.6, 'ВЗ-Н90В': 109.6, 'ВЗ-Н100': 122.6,
                     'ВЗ-Н100А': 122.6, 'ВЗ-Н100В': 122.6, 'ВЗ-Н16-МР12': 26.2, 'ВЗ-Н20-МР15': 29.6,
                     'ВЗ-Н20-МР16': 30.6, 'ВЗ-Н20-МР18': 31.6, 'ВЗ-Н20-МР20': 32.6, 'ВЗ-Н20-МР22': 33.6,
                     'ВЗ-Н20-МР25': 34.6, 'ВЗ-Н25-МР18': 39.3, 'ВЗ-Н25-МР20': 40.3, 'ВЗ-Н25-МР22': 41.3, 'ВЗ-Н25-МР25': 42.3,
                     'ВЗ-Н25-МР32': 43.3, 'ВЗ-Н32-МР25': 43.6, 'ВЗ-Н32-МР32': 44.6, 'ВЗ-Н32-МР38': 45.6, 'ВЗ-Н40-МР38': 54.9,
                     'ВЗ-16Н-Т3/8G(B)': 26.2, 'ВЗ-16Н-Т1/2G(B)': 26.2, 'ВЗ-20Н-Т1/2G(B)': 29.6, 'ВЗ-20Н-Т3/4G(B)': 29.6,
                     'ВЗ-25Н-Т3/4G(B)': 37.3, 'ВЗ-25Н-Т1G(B)': 37.3, 'ВЗ-32Н-Т1G(B)': 43.6, 'ВЗ-32Н-Т1.1/4G(B)': 43.6,
                     'ВЗ-40Н-Т1.1/4G(B)': 54.9, 'ВЗ-40Н-Т1.1/2G(B)': 54.9, 'ВЗ-50Н-Т1.1/2G(B)': 62.8,
                     'ВЗ-50Н-Т2G(B)': 62.8, 'ВЗ-Б16': 26.200000000000003, 'ВЗ-Б20': 29.6, 'ВЗ-МБ20': 29.6,
                     'ВЗ-Б25': 37.3, 'ВЗ-МБ25': 37.3, 'ВЗ-МБ25/Р': 37.3, 'ВЗ-Б32': 43.6, 'ВЗ-МБ32': 43.6,
                     'ВЗ-МБ32/Р': 43.6, 'ВЗ-Б40': 54.9, 'ВЗ-МБ40': 54.9, 'ВЗ-Б50': 62.8,
                     'ВЗ-Б63': 74.3, 'ВЗ-Б75': 87.6, 'ВЗ-Б75А': 89.6, 'ВЗ-Б90': 102.6, 'ВЗ-Б90В': 102.6,
                     'ВЗ-П20': 29.6, 'ВЗ-П20А': 29.6, 'ВЗ-П20В': 29.6, 'ВЗ-П32': 43.6, 'ВЗ-П32А': 43.6,
                     'ВЗ-П32В': 43.6, 'ВЗ-К20': 32.6, 'ВЗ-К25': 39.6, 'ВЗ-К32': 49.2, 'ВЗ-К40': 65.8}

    shell_name = 'VP.161610'

    print(sort_list_diametr_russian(list_with_diametr_russian=['ВЗ-Н25', 'ВЗ-Н20','ВЗ-Н32'],
                                    dict_with_name_diametr=full_name_dim))
    #Его будем возвращать в самом конце
    '''
    Получение координат словарем dict_with_inputs_on_side для построения в dxf
    {'А': {0: {'ВЗ-Н25': [32.11666666666667, 37.5]}, 1: {'ВЗ-Н25': [87.88333333333333, 37.5]}},
    'Б': {0: {'ВЗ-Н25': [24.783333333333335, 37.5]}, 1: {'ВЗ-Н25': [73.21666666666667, 37.5]}},
    'В': {},
    'Г': {},
    'Крышка': {}}
    '''
    dict_with_inputs_on_side = {'А': ['ВЗ-Н25', 'ВЗ-Н25'], 'Б': ['ВЗ-Н25'], 'В': ['ВЗ-Н25', 'ВЗ-Н25'], 'Г': [],
                                'Крышка': []}
    dict_with_inputs_on_side_return = {'А': {}, 'Б': {}, "В": {}, "Г": {}, "Крышка": {}}

    for russian_shell_side in dict_with_inputs_on_side:
        shell_side = define_side(side_russian_name=russian_shell_side)
        shell_points = create_points_of_drill_surface(doc=ezdxf.readfile(doc_base),
                                                      side=shell_side,
                                                      shell_name=shell_name)

        possible_diametr_from_shell = return_max_possible_diametr_on_surface(dict_coordinates=shell_points)

        list_with_diamets_russian = dict_with_inputs_on_side[russian_shell_side]

        list_with_diametrs_float = sorted([return_diametr_from_name(dict_all_names_dict=full_name_dim,
                                                             name_input=russian_name_input)
                                    for russian_name_input in dict_with_inputs_on_side[russian_shell_side]])

        if list_with_diametrs_float != []:
            #Если вообще вставить нельзя ввод, т.е. есть больше диаметр, чем минимальная сторона.
            if check_unreal_input(min_size_of_surface=possible_diametr_from_shell,
                                  max_diam_from_side=list_with_diametrs_float[0]):
                print('Первая проверка пройдена')

                main_surface = define_rectangle_size_for_inputs(dict_with_x_y_coordinates=shell_points)
                print(main_surface)
                max_size = max(main_surface['xy1'][0]-main_surface['xy0'][0],
                               main_surface['xy1'][1]-main_surface['xy0'][1])
                min_size = min(main_surface['xy1'][0]-main_surface['xy0'][0],
                               main_surface['xy1'][1]-main_surface['xy0'][1])

                free_length = check_possible_to_add_all_inputs_in_one_row(max_size=max_size,
                                                                          list_with_diametrs_float=list_with_diametrs_float)

                if free_length:
                    print('Проверка в одну строку пройдена')
                    coordinate_inputs = paint_circle_one_row(x0=main_surface['xy0'][0],
                                                             y0=main_surface['xy0'][1],
                                                             min_size=min_size,
                                                             list_with_diametrs_float=list_with_diametrs_float)

                    coordinate_inputs = move_inputs_one_row(coordinate_insert_input=coordinate_inputs,
                                                            free_length=free_length,
                                                            max_size=max_size)
                    print(coordinate_inputs)

                    dict_with_inputs_on_side_return[russian_shell_side] = \
                        return_inputs_dict_with_coordinate(sorted_list_diametr_russian=
                                                               sort_list_diametr_russian(list_with_diamets_russian,full_name_dim),
                                                           coordinate=coordinate_inputs)
                else:
                    print('Проверка в одну строку не пройдена')


    print(dict_with_inputs_on_side_return)





