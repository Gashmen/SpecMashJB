import ezdxf

def create_points_of_drill_surface(doc,
                                   side = None,
                                   shell_name = None) -> dict[str:list]:
    '''
    Возвращает точки зоны сверловки
    :param doc: doc в котором сделан импорт оболочки
    :param side: leftside,rightside,upside,downside
    :param shell_name:VP.161610
    :return:{'x':[2,5,8,10],'y':[0,1,2]}
    '''
    return_dict = {'x':[],'y':[]}
    if '_' not in side:
        side = '_'+side

    block_name = shell_name+side

    lwpolyline = doc.blocks[block_name].query('LWPOLYLINE')[0]

    if lwpolyline:
        for xy_coordinate in lwpolyline.get_points():
            return_dict['x'].append(round(xy_coordinate[0],2))
            return_dict['y'].append(round(xy_coordinate[1],2))

        return_dict['x'] = tuple(sorted(set(return_dict['x'])))
        return_dict['y'] = tuple(sorted(set(return_dict['y'])))
        return return_dict

def return_max_possible_diametr_on_surface(dict_coordinates:dict)->float:
    '''
    Определение максимального размера для вставки кабельного ввода
    :param dict_coordinates: {'x':[2,5,8,10],'y':[0,1,2]} или {'x':[8,10],'y':[0,1]}
    :return: 8
    '''

    max_x = dict_coordinates['x'][-1] - dict_coordinates['x'][0]
    max_y = dict_coordinates['y'][-1] - dict_coordinates['y'][-2]

    return max(max_x,max_y)

def return_diametr_from_name(dict_all_names_dict:{str:float}, name_input:str)->float:
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
    if min_size_of_surface == max(min_size_of_surface,max_diam_from_side):
        return True
    else:
        return False

def define_rectangle_size_for_inputs(dict_with_x_y_coordinates:dict[str:list]):
    '''
    Определение размеров прямоугольника
    :param dict_with_x_y_coordinates: {'x':[2,5,8,10],'y':[0,1,2]}
    :return:{'xy0': [0,0], 'xy1': [10,40]}
    '''
    return_dict = {}
    return_dict['xy0'] = [dict_with_x_y_coordinates['x'][0], dict_with_x_y_coordinates['y'][-2]]
    return_dict['xy1'] = [dict_with_x_y_coordinates['x'][-1], dict_with_x_y_coordinates['y'][-1]]
    return return_dict


'''Первый уровень поиска - это в 1 ряд'''

def paint_circle_one_row(max_size:float,min_size:float, list_with_diametrs_float:list)->list:
    '''
    Выдаем координаты диаметров в соответсвие с тем, что list_with_diametrs уже отсортирован и получается
    выходной list будет иметь индексы такие же, как диаметр окружности

    :param max_size: max(x,y)
    :param min_size: min(x,y)
    :param list_with_diametrs_float: sorted(list_with_diametrs_float): [31,30,29,27]
    :return: [[0,10],[10,10]...
    '''
    return_list = list()
    check_max_size = max_size

    if len(list_with_diametrs_float) == 1:
        return_list.append([list_with_diametrs_float[0]/2,min_size/2])

    if len(list_with_diametrs_float) > 1:
        for count_diametr, diametr in enumerate(list_with_diametrs_float):
            if check_max_size >= 0:
                if diametr == list_with_diametrs_float[0] or diametr == list_with_diametrs_float[-1]:

                    check_max_size = max_size - diametr - 5

                    if count_diametr == 0:
                        return_list.append([list_with_diametrs_float[0]/2,min_size/2])

                    else:
                        return_list.append([return_list[-1][0] + 5 + list_with_diametrs_float[count_diametr-1]/2,
                                            min_size/2])

                else:
                    check_max_size = max_size - diametr - 10

                    return_list.append([return_list[-1][0] + 5 + list_with_diametrs_float[count_diametr - 1] / 2,
                                        min_size / 2])

            else:
                raise ValueError('Окружности не помещаются в одну строчку')

    return return_list


def calculate_coordinate_inputs_in_one_row(xy0:list,xy1:list, list_with_diametrs_name:list[str],dict_all_names_dict:dict[str:float])->dict:
    '''
    Выдает координаты окружностей по именам при расстановке в один ряд.
    ЕСЛИ ЧТО ТО НЕ ВХОДИТ ИЛИ НЕ ПОМЕЩАЕТСЯ ТО ВОЗВРАЩАЕТ FALSE
    :param xy0:
    :param xy1:
    :param list_with_diametrs_name:
    :return:
    '''
    return_dict = {}
    list_with_diametrs_float = sorted(
        [return_diametr_from_name(dict_all_names_dict=dict_all_names_dict,name_input=name_input)
            for name_input in list_with_diametrs_name],
        reverse=True)
    #Сразу обозначить по цифрам, чтобы обращаться через индексы списков
    for _ in range(0,len(list_with_diametrs_name)):
        return_dict[_] = {}

    max_size = max(xy1[0] - xy0[0], xy1[1] - xy0[1])
    min_size = min(xy1[0] - xy0[0], xy1[1] - xy0[1])
    if check_unreal_input(min_size_of_surface=min_size,
                          max_diam_from_side=list_with_diametrs_float[0]):
        list_coordinates = paint_circle_one_row(max_size=max_size,
                                                min_size=min_size,
                                                list_with_diametrs_float=list_with_diametrs_float)

    else:
        raise ValueError('Не помещается диаметр на сторону')


def create_coordinates_inputs_on_side_with_DIN(doc,
                                               coordinate_drill_surface:dict[str:list],
                                               side:str,
                                               list_with_inputs_name:list[str],
                                               dict_with_name_diametr:dict[str:float]):
    '''
    Создает координаты на стороне, где есть дин рейка
    :param doc: после импорта всех блоков
    :param side: leftside или rightside
    :param list_with_inputs_name:['ВЗ-Н25', 'ВЗ-Н25']
    :param dict_with_name_diametr:{'': None, 'ВЗ-Н12': 31.9, 'ВЗ-Н16': 36.2, 'ВЗ-Н20': 39.6, 'ВЗ-Н25': 47.3, 'ВЗ-Н25/Р': 47.3, 'ВЗ-Н32': 53.6, 'ВЗ-Н32/Р': 53.6, 'ВЗ-Н40': 64.9, 'ВЗ-Н50': 72.8, 'ВЗ-Н63': 84.3, 'ВЗ-Н75': 97.6, 'ВЗ-Н75А': 99.6, 'ВЗ-Н90': 112.6, 'ВЗ-Н90А': 119.6, 'ВЗ-Н90В': 119.6, 'ВЗ-Н100': 132.6, 'ВЗ-Н100А': 132.6, 'ВЗ-Н100В': 132.6, 'ВЗ-Н16-МР12': 36.2, 'ВЗ-Н20-МР15': 39.6, 'ВЗ-Н20-МР16': 40.6, 'ВЗ-Н20-МР18': 41.6, 'ВЗ-Н20-МР20': 42.6, 'ВЗ-Н20-МР22': 43.6, 'ВЗ-Н20-МР25': 44.6, 'ВЗ-Н25-МР18': 49.3, 'ВЗ-Н25-МР20': 50.3, 'ВЗ-Н25-МР22': 51.3, 'ВЗ-Н25-МР25': 52.3, 'ВЗ-Н25-МР32': 53.3, 'ВЗ-Н32-МР25': 53.6, 'ВЗ-Н32-МР32': 54.6, 'ВЗ-Н32-МР38': 55.6, 'ВЗ-Н40-МР38': 64.9, 'ВЗ-16Н-Т3/8G(B)': 36.2, 'ВЗ-16Н-Т1/2G(B)': 36.2, 'ВЗ-20Н-Т1/2G(B)': 39.6, 'ВЗ-20Н-Т3/4G(B)': 39.6, 'ВЗ-25Н-Т3/4G(B)': 47.3, 'ВЗ-25Н-Т1G(B)': 47.3, 'ВЗ-32Н-Т1G(B)': 53.6, 'ВЗ-32Н-Т1.1/4G(B)': 53.6, 'ВЗ-40Н-Т1.1/4G(B)': 64.9, 'ВЗ-40Н-Т1.1/2G(B)': 64.9, 'ВЗ-50Н-Т1.1/2G(B)': 72.8, 'ВЗ-50Н-Т2G(B)': 72.8, 'ВЗ-Б16': 36.2, 'ВЗ-Б20': 39.6, 'ВЗ-МБ20': 39.6, 'ВЗ-Б25': 47.3, 'ВЗ-МБ25': 47.3, 'ВЗ-МБ25/Р': 47.3, 'ВЗ-Б32': 53.6, 'ВЗ-МБ32': 53.6, 'ВЗ-МБ32/Р': 53.6, 'ВЗ-Б40': 64.9, 'ВЗ-МБ40': 64.9, 'ВЗ-Б50': 72.8, 'ВЗ-Б63': 84.3, 'ВЗ-Б75': 97.6, 'ВЗ-Б75А': 99.6, 'ВЗ-Б90': 112.6, 'ВЗ-Б90В': 112.6, 'ВЗ-П20': 39.6, 'ВЗ-П20А': 39.6, 'ВЗ-П20В': 39.6, 'ВЗ-П32': 53.6, 'ВЗ-П32А': 53.6, 'ВЗ-П32В': 53.6, 'ВЗ-К20': 42.6, 'ВЗ-К25': 49.6, 'ВЗ-К32': 59.2, 'ВЗ-К40': 75.8}
    :return:
    '''
    return_dict = {}

    return return_dict

def calculate_max_cable_input(list_with_inputs_name:list[str],
                              dict_with_name_diametr:dict[str:float]):
    '''
    Получает максимальный диаметр кабельного ввода
    :param list_with_inputs_name:
    :param dict_with_name_diametr:
    :return:
    '''



if __name__ == "__main__":
    drill_surface = create_points_of_drill_surface(doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf'),
                                                   side= 'rightside',
                                                   shell_name='VP.161610')
    full_name_dim = {'': None, 'ВЗ-Н12': 31.9, 'ВЗ-Н16': 36.2, 'ВЗ-Н20': 39.6, 'ВЗ-Н25': 47.3, 'ВЗ-Н25/Р': 47.3, 'ВЗ-Н32': 53.6, 'ВЗ-Н32/Р': 53.6, 'ВЗ-Н40': 64.9, 'ВЗ-Н50': 72.8, 'ВЗ-Н63': 84.3, 'ВЗ-Н75': 97.6, 'ВЗ-Н75А': 99.6, 'ВЗ-Н90': 112.6, 'ВЗ-Н90А': 119.6, 'ВЗ-Н90В': 119.6, 'ВЗ-Н100': 132.6, 'ВЗ-Н100А': 132.6, 'ВЗ-Н100В': 132.6, 'ВЗ-Н16-МР12': 36.2, 'ВЗ-Н20-МР15': 39.6, 'ВЗ-Н20-МР16': 40.6, 'ВЗ-Н20-МР18': 41.6, 'ВЗ-Н20-МР20': 42.6, 'ВЗ-Н20-МР22': 43.6, 'ВЗ-Н20-МР25': 44.6, 'ВЗ-Н25-МР18': 49.3, 'ВЗ-Н25-МР20': 50.3, 'ВЗ-Н25-МР22': 51.3, 'ВЗ-Н25-МР25': 52.3, 'ВЗ-Н25-МР32': 53.3, 'ВЗ-Н32-МР25': 53.6, 'ВЗ-Н32-МР32': 54.6, 'ВЗ-Н32-МР38': 55.6, 'ВЗ-Н40-МР38': 64.9, 'ВЗ-16Н-Т3/8G(B)': 36.2, 'ВЗ-16Н-Т1/2G(B)': 36.2, 'ВЗ-20Н-Т1/2G(B)': 39.6, 'ВЗ-20Н-Т3/4G(B)': 39.6, 'ВЗ-25Н-Т3/4G(B)': 47.3, 'ВЗ-25Н-Т1G(B)': 47.3, 'ВЗ-32Н-Т1G(B)': 53.6, 'ВЗ-32Н-Т1.1/4G(B)': 53.6, 'ВЗ-40Н-Т1.1/4G(B)': 64.9, 'ВЗ-40Н-Т1.1/2G(B)': 64.9, 'ВЗ-50Н-Т1.1/2G(B)': 72.8, 'ВЗ-50Н-Т2G(B)': 72.8, 'ВЗ-Б16': 36.2, 'ВЗ-Б20': 39.6, 'ВЗ-МБ20': 39.6, 'ВЗ-Б25': 47.3, 'ВЗ-МБ25': 47.3, 'ВЗ-МБ25/Р': 47.3, 'ВЗ-Б32': 53.6, 'ВЗ-МБ32': 53.6, 'ВЗ-МБ32/Р': 53.6, 'ВЗ-Б40': 64.9, 'ВЗ-МБ40': 64.9, 'ВЗ-Б50': 72.8, 'ВЗ-Б63': 84.3, 'ВЗ-Б75': 97.6, 'ВЗ-Б75А': 99.6, 'ВЗ-Б90': 112.6, 'ВЗ-Б90В': 112.6, 'ВЗ-П20': 39.6, 'ВЗ-П20А': 39.6, 'ВЗ-П20В': 39.6, 'ВЗ-П32': 53.6, 'ВЗ-П32А': 53.6, 'ВЗ-П32В': 53.6, 'ВЗ-К20': 42.6, 'ВЗ-К25': 49.6, 'ВЗ-К32': 59.2, 'ВЗ-К40': 75.8}

    value_diametr = return_diametr_from_name(dict_all_names_dict=full_name_dim,
                                             name_input='ВЗ-Н25')

    max_diametr_in_rectangle = return_max_possible_diametr_on_surface(dict_coordinates=drill_surface)

    if check_unreal_input(max_size_of_surface=max_diametr_in_rectangle,
                          max_diam_from_side=value_diametr):
        print(1)

    print(return_max_possible_diametr_on_surface(drill_surface))

    print(define_rectangle_size_for_inputs(dict_with_x_y_coordinates=drill_surface))
