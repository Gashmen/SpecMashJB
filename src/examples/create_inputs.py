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

    max_x = dict_coordinates['x'][-1] - dict_coordinates['x'][-2]
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


def check_unreal_input(max_size_of_surface: float,
                       max_diam_from_side: float):
    '''
    Проверка на возможность установки кабельного ввода в оболочку
    :param max_size_of_surface: Для прямоугольника-большая сторона прямоугольника, для 8угольника, max(Y2-Y1, X2-X0)

    :param max_diam_from_side:
    :return: True or False
    '''
    if max_size_of_surface == max(max_size_of_surface,max_diam_from_side):
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
    return_dict['xy0'] = [dict_with_x_y_coordinates['x'][-2], dict_with_x_y_coordinates['y'][-2]]
    return_dict['xy1'] = [dict_with_x_y_coordinates['x'][-1], dict_with_x_y_coordinates['y'][-1]]
    return return_dict

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

