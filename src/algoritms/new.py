import math
def calculate_coordinates_for_inputs_in_one_row(x, y, dict_with_diametrs:list,all_name_inputs:dict):
    '''

    :param x: 120.0
    :param y: 75.0
    :param dict_with_diametrs: ['ВЗ-Н32', 'ВЗ-Н32']
    :param all_name_inputs: {'': None, 'ВЗ-Н12': 31.9, 'ВЗ-Н16': 36.2, 'ВЗ-Н20': 39.6, 'ВЗ-Н25': 47.3, 'ВЗ-Н25/Р': 47.3, 'ВЗ-Н32': 53.6, 'ВЗ-Н32/Р': 53.6, 'ВЗ-Н40': 64.9, 'ВЗ-Н50': 72.8, 'ВЗ-Н63': 84.3, 'ВЗ-Н75': 97.6, 'ВЗ-Н75А': 99.6, 'ВЗ-Н90': 112.6, 'ВЗ-Н90А': 119.6, 'ВЗ-Н90В': 119.6, 'ВЗ-Н100': 132.6, 'ВЗ-Н100А': 132.6, 'ВЗ-Н100В': 132.6, 'ВЗ-Н16-МР12': 36.2, 'ВЗ-Н20-МР15': 39.6, 'ВЗ-Н20-МР16': 40.6, 'ВЗ-Н20-МР18': 41.6, 'ВЗ-Н20-МР20': 42.6, 'ВЗ-Н20-МР22': 43.6, 'ВЗ-Н20-МР25': 44.6, 'ВЗ-Н25-МР18': 49.3, 'ВЗ-Н25-МР20': 50.3, 'ВЗ-Н25-МР22': 51.3, 'ВЗ-Н25-МР25': 52.3, 'ВЗ-Н25-МР32': 53.3, 'ВЗ-Н32-МР25': 53.6, 'ВЗ-Н32-МР32': 54.6, 'ВЗ-Н32-МР38': 55.6, 'ВЗ-Н40-МР38': 64.9, 'ВЗ-16Н-Т3/8G(B)': 36.2, 'ВЗ-16Н-Т1/2G(B)': 36.2, 'ВЗ-20Н-Т1/2G(B)': 39.6, 'ВЗ-20Н-Т3/4G(B)': 39.6, 'ВЗ-25Н-Т3/4G(B)': 47.3, 'ВЗ-25Н-Т1G(B)': 47.3, 'ВЗ-32Н-Т1G(B)': 53.6, 'ВЗ-32Н-Т1.1/4G(B)': 53.6, 'ВЗ-40Н-Т1.1/4G(B)': 64.9, 'ВЗ-40Н-Т1.1/2G(B)': 64.9, 'ВЗ-50Н-Т1.1/2G(B)': 72.8, 'ВЗ-50Н-Т2G(B)': 72.8, 'ВЗ-Б16': 36.2, 'ВЗ-Б20': 39.6, 'ВЗ-МБ20': 39.6, 'ВЗ-Б25': 47.3, 'ВЗ-МБ25': 47.3, 'ВЗ-МБ25/Р': 47.3, 'ВЗ-Б32': 53.6, 'ВЗ-МБ32': 53.6, 'ВЗ-МБ32/Р': 53.6, 'ВЗ-Б40': 64.9, 'ВЗ-МБ40': 64.9, 'ВЗ-Б50': 72.8, 'ВЗ-Б63': 84.3, 'ВЗ-Б75': 97.6, 'ВЗ-Б75А': 99.6, 'ВЗ-Б90': 112.6, 'ВЗ-Б90В': 112.6, 'ВЗ-П20': 39.6, 'ВЗ-П20А': 39.6, 'ВЗ-П20В': 39.6, 'ВЗ-П32': 53.6, 'ВЗ-П32А': 53.6, 'ВЗ-П32В': 53.6, 'ВЗ-К20': 42.6, 'ВЗ-К25': 49.6, 'ВЗ-К32': 59.2, 'ВЗ-К40': 75.8}
    :return:
    '''

    dict_with_added_diametrs_in_rectangle = dict()
    '''dict_with_added_diametrs_in_rectangle = {0: {'ВЗ-Б32': [26.8, 37.5]}, 1: {'ВЗ-Б32': [80.4, 37.5]}}'''
    max_size = max(x, y)
    min_size = min(x, y)
    last_added_diametr = 0.0
    for key,name_of_diamert in enumerate(list(dict_with_diametrs)):
        diametr_input = all_name_inputs[name_of_diamert]
        if diametr_input <= min_size and diametr_input <= max_size:
            dict_with_added_diametrs_in_rectangle[key] = \
                {name_of_diamert:[last_added_diametr+diametr_input/2,min_size/2]}
            last_added_diametr += diametr_input
            max_size -= (diametr_input)
    #Получение расстояния до правого края : длина - последняя точка вставки - радиус последней окружности вставки.
    if dict_with_added_diametrs_in_rectangle != {}:

        distance_between_max_cord_and_shell_wall = max(x, y) - \
                                            list(list(dict_with_added_diametrs_in_rectangle.values())[-1].values())[0][0] - \
                                            all_name_inputs[list(list(dict_with_added_diametrs_in_rectangle.values())[-1].keys())[0]]/2
    if dict_with_added_diametrs_in_rectangle != {}:
        for key,i in dict_with_added_diametrs_in_rectangle.items():
            for diametr,coord_x in i.items():
                dict_with_added_diametrs_in_rectangle[key][diametr][0] =\
                coord_x[0] + distance_between_max_cord_and_shell_wall *((key+1)/(len(dict_with_added_diametrs_in_rectangle.keys())+1))
    return dict_with_added_diametrs_in_rectangle

#['ВЗ-Н20', 'ВЗ-Н20', 'ВЗ-Н20', 'ВЗ-Н20']

#Лист сверху передается нижнему по входит или не входит
def create_levels(x, y, list_with_diametrs):
    dict_with_diametr_and_level = dict()
    min_size = min(x, y)
    level = min_size // min(list_with_diametrs)
    for diametr_input in list_with_diametrs:
        dict_with_diametr_and_level[diametr_input] = math.ceil(diametr_input / min(list_with_diametrs))
    return dict_with_diametr_and_level

def calculate_coordinates_for_inputs_test(x,y,list_with_diametrs):
    '''
    :param x: длина
    :param y: ширина
    :param list_with_diametrs: Словарь, который уже передается со списком, в котором каждый диаметр меньше Min(x,y)
    и ко всем диаметрам добавлено по 10 мм
    :return:
    '''
    max_size = max(x,y)
    min_size = min(x,y)
    list_with_diametrs = sorted(list_with_diametrs,reverse=True)
    level = 0
    level_box = f'{level}_{list_with_diametrs[0]}'
    level_box_for_packing = list_with_diametrs[0]
    dict_key_level_value_alldiametrs_in_level = {level_box:[level_box_for_packing]}
    level_size = min_size*1
    hight_size  = max_size
    for cont,value in enumerate(list_with_diametrs):
        if cont != 0:
            if hight_size >= value:
                if level_size - level_box_for_packing >= value:
                    level_size -= value
                    dict_key_level_value_alldiametrs_in_level[level_box].append(value)
                else:
                    level_size = min_size*1
                    level +=1
                    level_box = f'{level}_{value}'
                    level_box_for_packing = value
                    dict_key_level_value_alldiametrs_in_level[level_box] = [level_box_for_packing]
                    hight_size -= level_box_for_packing
    return dict_key_level_value_alldiametrs_in_level

'''Определение сечения по макс и мин диапазону'''

def change_cooma_to_dot(cell_excel_file:str):
    '''Проверка запятой, т.к. в excel или человек может написать числа float пишутся через запятую, а тут через точку
    cell_excel_file : self.main_dict[self.manufacturerInputsComboBox.currentText()][
                                            'Кабельные вводы']['Диаметр обжимаемого кабеля мин'] = 49,3
    '''
    if ',' in cell_excel_file:
        return cell_excel_file.replace(',','.')
    else:
        return cell_excel_file

def define_max_input(max_value:str):
    '''Определяем наибольший диаметр'''
    if max_value != '':
        value_max = float(change_cooma_to_dot(max_value))
        return value_max
    else:
        value_max = 0.0
        return value_max

def define_min_input(min_value:str):
    '''Определяем наименьший диаметр'''
    if min_value != '':
        value_min = float(change_cooma_to_dot(min_value))
        return value_min
    else:
        value_min = 0.0
        return value_min

def check_that_max_more_then_min(max_value = 0,min_value = 0):
    '''Проверяем, если max > min все ок, если меньше, то не ок, и выдаем False'''
    if max_value > min_value:
        return True
    else:
        return False

def second_type_of_creating_circle(x:float,y:float,list_with_diametrs:list):

    '''
    Второй путь для создания окружностей
    :param x: 120.0
    :param y: 75.0
    :param list_with_diametrs: [['ВЗ-Н32',31.9], ['ВЗ-Н32',31.9]]
    :return:
    '''

    height_shell = min(x,y)
    list_with_diametrs_sorted = sorted(list_with_diametrs,key = lambda x: x[1], reverse=True)

    for key,i in enumerate(list_with_diametrs_sorted):
        i.insert(0, key)
        list_with_diametrs_sorted[key] = i
    list_for_deliting = list_with_diametrs_sorted.copy()

    dict_level_input = dict()
    level = 0
    '''
            1.Добавляем сначала первый по сорту кабельный ввод, удаляем его из списка для удаления, по которому цикл while работает
            2.Ищем оставшуюся высоту
            3.Прибавляем итерационный номер по вводам сначала
            [0,'ВЗ-Н32',31.9] - вот такого вида лист
            '''
    while list_for_deliting != []:

        dict_level_input[level] = [list_for_deliting[0]]
        height_shell_residue = height_shell - list_for_deliting[0][2]
        list_for_deliting.remove(list_for_deliting[0])

        '''
        1. Второй цикл while для проверки, еще есть место для добавления ввода. Если последний нижний не помещается, то 
        значит и остальные не поместятся 
        2. Если в list_for_deliting еще есть ввод, то вставляем 
        '''

        while height_shell_residue >= list_for_deliting[-1][2]:
            if len(list_for_deliting) > 1:
                dict_level_input[level].append(list_for_deliting[-1])
                height_shell_residue -= list_for_deliting[-1][2]
                list_for_deliting.remove(list_for_deliting[-1])
            elif len(list_for_deliting) == 1:
                dict_level_input[level].append(list_for_deliting[-1])
                height_shell_residue -= list_for_deliting[-1][2]
                list_for_deliting.remove(list_for_deliting[-1])
                break
            else:
                break

        level +=1
        height_shell_residue = height_shell

    '''Сортировка полученного результата'''
    for i in dict_level_input:
        dict_level_input[i] = sorted(dict_level_input[i],key=lambda x: x[2],reverse=True)

    return dict_level_input

def set_one_of_the_top(x:float,y:float,dict_after_second_type_of_creating:dict):
    '''

    :param x: 120.0
    :param y: 120.0
    :param dict_after_second_type_of_creating:{
    0: [[0, 'ВЗ-Н32', 32.3], [4, 'ВЗ-Н32', 31.1], [5, 'ВЗ-Н32', 31.0]],
    1: [[1, 'ВЗ-Н32', 31.9], [2, 'ВЗ-Н32', 31.7], [3, 'ВЗ-Н32', 31.5]]
    }
    :return:
    [['ВЗ-Н32', [16.15, 25.68]], ['ВЗ-Н32', [16.15, 65.91]],
    ['ВЗ-Н32', [16.15, 105.5]], ['ВЗ-Н32', [48.25, 25.25]],
    ['ВЗ-Н32', [48.25, 65.35]], ['ВЗ-Н32', [48.25, 105.25]]]
    '''
    list_coords = []
    x_coord = 0
    max_coord = max(x,y)
    min_coord = min(x,y)

    for level, inputs in dict_after_second_type_of_creating.items():
        delta_on_y = min_coord - sum([i[2] for i in inputs])#Разница между y1 и суммарным диаметром всех окружностей
        max_len_on_level = inputs[0][2]#Максимальный диаметр на этом уровне
        x_coord_on_level = x_coord + max_len_on_level / 2 #координата x вставки на уровне
        y_coord_on_level = 0 #Переменная, для прибавления диаметров вставленных уже окружностей
        for count_input, input_on_level in enumerate(inputs):
            '''list_coords = ['ВЗ-Н32',[17.3,28.4]]'''
            list_coords.append([input_on_level[1],
                                [x_coord_on_level,y_coord_on_level + input_on_level[2]/2 +
                                 delta_on_y * (count_input+1)/len(inputs)+1]])
            y_coord_on_level += input_on_level[2]
        x_coord+=max_len_on_level

    return list_coords




def third_type_of_creating_circle(x:float,y:float,list_with_diametrs:list):

    '''
    :param x: 120.0
    :param y: 75.0
    :param list_with_diametrs: [['ВЗ-Н32', 31.9], ['ВЗ-Н32', 31.9]]
    :return:
    [['ВЗ-Н32', [16.15, 25.68]], ['ВЗ-Н32', [16.15, 65.91]],
    ['ВЗ-Н32', [16.15, 105.5]], ['ВЗ-Н32', [48.25, 25.25]],
    ['ВЗ-Н32', [48.25, 65.35]], ['ВЗ-Н32', [48.25, 105.25]]]
    '''

    height_shell = min(x, y)
    list_with_diametrs_sorted = sorted(list_with_diametrs, key=lambda x: x[1], reverse=True)
    max_coordinate = max(x,y)

    list_added_diam = []


    # for name,diametr in list_with_diametrs:
    #     if height_shell >= diametr:
    #         list_added_diam.append([name,diametr])
    #     else:





dict_size = {'ВА.261609':{'A':212, 'Б':84, "Высота":65},
             "ВА.121209":{'A':57, 'Б':78, "Высота":80},
             "ВА.221209":{'A':178, 'Б':57, "Высота":80},
             "ВА.221810":{'A':178, 'Б':57, "Высота":80},
             "ВА.161610":{'A':94, 'Б':116, "Высота":90},
             "ВП.110806":{'A':71, 'Б':30, "Высота":45},
             "ВП.121209":{'A':58, 'Б':82, "Высота":80},
             "ВП.221209":{'A':177, 'Б':57, "Высота":80},
             "ВП.150807":{'A':110, 'Б':34, "Высота":60},
             "ВП.161610":{'A':120, 'Б':96, "Высота":90},
             "ВП.261610":{'A':205, 'Б':89, "Высота":90},
             "ВП.262512":{'A':213, 'Б':172, "Высота":110}}


if __name__ == '__main__':
    x = 120
    y = 75
    dict_with_diametrs = ['ВЗ-Н12', 'ВЗ-Н12']
    all_name_inputs = {'': None, 'ВЗ-Н12': 31.9, 'ВЗ-Н16': 36.2, 'ВЗ-Н20': 39.6, 'ВЗ-Н25': 47.3, 'ВЗ-Н25/Р': 47.3,
                       'ВЗ-Н32': 53.6, 'ВЗ-Н32/Р': 53.6, 'ВЗ-Н40': 64.9, 'ВЗ-Н50': 72.8, 'ВЗ-Н63': 84.3, 'ВЗ-Н75': 97.6,
                       'ВЗ-Н75А': 99.6, 'ВЗ-Н90': 112.6, 'ВЗ-Н90А': 119.6, 'ВЗ-Н90В': 119.6, 'ВЗ-Н100': 132.6,
                       'ВЗ-Н100А': 132.6, 'ВЗ-Н100В': 132.6, 'ВЗ-Н16-МР12': 36.2, 'ВЗ-Н20-МР15': 39.6,
                       'ВЗ-Н20-МР16': 40.6, 'ВЗ-Н20-МР18': 41.6, 'ВЗ-Н20-МР20': 42.6, 'ВЗ-Н20-МР22': 43.6,
                       'ВЗ-Н20-МР25': 44.6, 'ВЗ-Н25-МР18': 49.3, 'ВЗ-Н25-МР20': 50.3, 'ВЗ-Н25-МР22': 51.3,
                       'ВЗ-Н25-МР25': 52.3, 'ВЗ-Н25-МР32': 53.3, 'ВЗ-Н32-МР25': 53.6, 'ВЗ-Н32-МР32': 54.6,
                       'ВЗ-Н32-МР38': 55.6, 'ВЗ-Н40-МР38': 64.9, 'ВЗ-16Н-Т3/8G(B)': 36.2, 'ВЗ-16Н-Т1/2G(B)': 36.2,
                       'ВЗ-20Н-Т1/2G(B)': 39.6, 'ВЗ-20Н-Т3/4G(B)': 39.6, 'ВЗ-25Н-Т3/4G(B)': 47.3, 'ВЗ-25Н-Т1G(B)': 47.3,
                       'ВЗ-32Н-Т1G(B)': 53.6, 'ВЗ-32Н-Т1.1/4G(B)': 53.6, 'ВЗ-40Н-Т1.1/4G(B)': 64.9,
                       'ВЗ-40Н-Т1.1/2G(B)': 64.9, 'ВЗ-50Н-Т1.1/2G(B)': 72.8, 'ВЗ-50Н-Т2G(B)': 72.8, 'ВЗ-Б16': 36.2,
                       'ВЗ-Б20': 39.6, 'ВЗ-МБ20': 39.6, 'ВЗ-Б25': 47.3, 'ВЗ-МБ25': 47.3, 'ВЗ-МБ25/Р': 47.3,
                       'ВЗ-Б32': 53.6, 'ВЗ-МБ32': 53.6, 'ВЗ-МБ32/Р': 53.6, 'ВЗ-Б40': 64.9, 'ВЗ-МБ40': 64.9,
                       'ВЗ-Б50': 72.8, 'ВЗ-Б63': 84.3, 'ВЗ-Б75': 97.6, 'ВЗ-Б75А': 99.6, 'ВЗ-Б90': 112.6,
                       'ВЗ-Б90В': 112.6, 'ВЗ-П20': 39.6, 'ВЗ-П20А': 39.6, 'ВЗ-П20В': 39.6, 'ВЗ-П32': 53.6,
                       'ВЗ-П32А': 53.6, 'ВЗ-П32В': 53.6, 'ВЗ-К20': 42.6, 'ВЗ-К25': 49.6, 'ВЗ-К32': 59.2, 'ВЗ-К40': 75.8}
    a = calculate_coordinates_for_inputs_in_one_row(x = x,
                                                    y = y,
                                                    dict_with_diametrs = dict_with_diametrs,
                                                    all_name_inputs = all_name_inputs)
    list_with_diametrs = [all_name_inputs[i] for i in dict_with_diametrs]
    b = create_levels(x = x,
                      y = y,
                      list_with_diametrs = list_with_diametrs)
    list_name_diametr = [[i,all_name_inputs[i]] for i in dict_with_diametrs]
    c = second_type_of_creating_circle(x=x,
                                   y=y,
                                   list_with_diametrs=[['ВЗ-Н32',31.9], ['ВЗ-Н32',31.7],['ВЗ-Н32',31.5],['ВЗ-Н32',31.1],
                                                       ['ВЗ-Н32',31.0],['ВЗ-Н32',32.3]])
    d = set_one_of_the_top(x = x,
                       y = y,
                    dict_after_second_type_of_creating = c)

    print(d)

