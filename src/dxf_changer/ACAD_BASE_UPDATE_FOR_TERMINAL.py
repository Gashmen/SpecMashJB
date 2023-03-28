import itertools
import ezdxf
from ezdxf import zoom
'''Нейминг у клемм будет вида SUPU_SCREW(или SPRING)_WHITE(или BLUE,GREEN,ORANGE)_2.5'''

CROSS_SECTION_DIAMETR = (2.5,4,6,10,16,35,50,70,95)
MANUFACTURER = 'SUPU'
TERMINAL_TYPE = 'SCREW'

'''Вынесение Hatch у всех block наверх, !белый цвет самый верхний!'''

def set_hatch_before_entity(block):
    block.set_redraw_order(
        (solid.dxf.handle, "%X" % (1000 - solid.dxf.color))
        for solid in block.entity_space if solid.dxftype() == 'HATCH')

'''Получение центра по координате Х'''

def create_dict_with_horizontal_lines(block):
    ''' Сначала создаем словарь в котором находится координата y горизантольных линий(ключ) и
        линии на этой координате(значения) в списке. '''
    dict_with_horizontal_lines = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'LINE':
            if round(entity.dxf.start[1], 2) == round(entity.dxf.end[1],2):
                if round(entity.dxf.start[1], 2) not in dict_with_horizontal_lines:
                    dict_with_horizontal_lines[round(entity.dxf.start[1], 2)] = [entity]
                else:
                    dict_with_horizontal_lines[round(entity.dxf.start[1], 2)].append(entity)
    return dict_with_horizontal_lines


def calculate_x_coordinate(dict_with_horizontal_lines:dict) -> dict:
    '''Расчет координаты X центра клеммы'''
    max_sum = []
    min_x_coord_on_this_horizontal_level = []
    for y_coordinate in dict_with_horizontal_lines:
        sum_of_all_lines_in_this_y = 0

        min_x_coord_on_this_horizontal_level_iteration = None
        max_x_coord_on_this_horizontal_level_iteration = None
        '''Найдем самую минимальную координату на этих отрезках и самую максимальную'''

        for line in dict_with_horizontal_lines[y_coordinate]:
            
            sum_of_all_lines_in_this_y += abs(round(line.dxf.end[0] - line.dxf.start[0],2))
            if min_x_coord_on_this_horizontal_level_iteration == None and \
               max_x_coord_on_this_horizontal_level_iteration == None:
                min_x_coord_on_this_horizontal_level_iteration = min(round(line.dxf.end[0],2),
                                                                     round(line.dxf.start[0],2))
                max_x_coord_on_this_horizontal_level_iteration = max(round(line.dxf.end[0],2),
                                                                     round(line.dxf.start[0],2))
            
            else:
                min_x_coord_on_this_horizontal_level_iteration = \
                    min(min_x_coord_on_this_horizontal_level_iteration,
                        min(round(line.dxf.end[0],2),round(line.dxf.start[0],2)))
                max_x_coord_on_this_horizontal_level_iteration = \
                    max(max_x_coord_on_this_horizontal_level_iteration,
                        max(round(line.dxf.end[0],2),round(line.dxf.start[0],2)))

        max_sum.append(max_x_coord_on_this_horizontal_level_iteration - min_x_coord_on_this_horizontal_level_iteration)
        min_x_coord_on_this_horizontal_level.append(min_x_coord_on_this_horizontal_level_iteration)
    '''Выдаем словарь, ключ половина длины, значение точка x_coordinate '''
    return {(max(max_sum)):(max(max_sum)/2) + min_x_coord_on_this_horizontal_level[max_sum.index(max(max_sum))]}


def check_that_the_block_is_terminal(block,set_main_terminals = None):
    '''Проверка, является ли блок клеммой, или это блок который в клемме(номер или обозначение)'''
    if block.dxf.name in set_main_terminals:
        return True


def create_dict_with_vertical_lines(block):
    ''' Создаем словарь в котором находится координата y вертикальных линий(ключ) и
        линии на этой координате(значения) в списке. '''
    dict_with_vertical_lines = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'LINE':
            if round(entity.dxf.start[0], 1) == round(entity.dxf.end[0],1):
                if round(entity.dxf.start[0], 1) not in dict_with_vertical_lines:
                    dict_with_vertical_lines[round(entity.dxf.start[0], 1)] = [entity]
                else:
                    dict_with_vertical_lines[round(entity.dxf.start[0], 1)].append(entity)
    return dict_with_vertical_lines

def calculate_center_y_coordinate(dict_with_vertical_lines:dict):
    left_horizontals_x_coord: float = min(list(dict_with_vertical_lines.keys()))
    right_horizontals_x_coord: float = max(list(dict_with_vertical_lines.keys()))

    '''Минимальная координата по y'''
    y_min_left_or_right = None
    '''Поиск максимум и минимума координаты по левой линии'''
    top_coord_left_coord = None
    bot_coord_left_coord = None

    for line in dict_with_vertical_lines[left_horizontals_x_coord]:
        if top_coord_left_coord == None:
            top_coord_left_coord = max(line.dxf.start[1],line.dxf.end[1])
        else:
            top_coord_left_coord = max(top_coord_left_coord, max(line.dxf.start[1],line.dxf.end[1]))

        if bot_coord_left_coord == None:
            bot_coord_left_coord = min(line.dxf.start[1], line.dxf.end[1])
        else:
            bot_coord_left_coord = min(bot_coord_left_coord, min(line.dxf.start[1], line.dxf.end[1]))

    '''Поиск максимум и минимума координаты по правой линии'''
    top_coord_right_coord = None
    bot_coord_right_coord = None

    for line in dict_with_vertical_lines[right_horizontals_x_coord]:
        if top_coord_right_coord == None:
            top_coord_right_coord = max(line.dxf.start[1],line.dxf.end[1])
        else:
            top_coord_right_coord = max(top_coord_right_coord, max(line.dxf.start[1],line.dxf.end[1]))

        if bot_coord_right_coord == None:
            bot_coord_right_coord = min(line.dxf.start[1], line.dxf.end[1])
        else:
            bot_coord_right_coord = min(bot_coord_right_coord, min(line.dxf.start[1], line.dxf.end[1]))

    '''Получение длины отрезка максимального по стороне terminal'''
    summirize_len_left_x_coord = top_coord_left_coord - bot_coord_left_coord
    summirize_len_right_x_coord = top_coord_right_coord - bot_coord_right_coord

    terminal_height = round(max(summirize_len_left_x_coord,summirize_len_right_x_coord),2)
    y_center = min(bot_coord_right_coord, bot_coord_left_coord) + terminal_height/2

    return round(terminal_height,2),round(y_center,2)

'''Опредиление координаты Y, центр между двумя кругами, которые слева и справа от центра кругов'''
def create_dict_with_circles(block):
    ''' Сначала создаем словарь в котором находится координата y горизантольных линий(ключ) и
            линии на этой координате(значения) в списке.  '''
    dict_with_circles = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'CIRCLE' or entity.dxftype() == 'ARC':
            if round(entity.dxf.center[0],2) not in dict_with_circles:
                dict_with_circles[round(entity.dxf.center[0],2)] = [entity]
            else:
                dict_with_circles[round(entity.dxf.center[0],2)].append(entity)
    #Находим точку икс с самым большим количеством окружностей с центром в ней
    len_max = 0
    for i in dict_with_circles:
        if max(len_max,len(dict_with_circles[i])) > len_max:
            dict_with_circles = {i:dict_with_circles[i]}
    return dict_with_circles


def create_dict_with_arc(block):
    dict_with_arc = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'ARC':
            if round(entity.dxf.center[0], 2) not in dict_with_arc:
                dict_with_arc[round(entity.dxf.center[0], 2)] = [entity]
            else:
                dict_with_arc[round(entity.dxf.center[0], 2)].append(entity)
    len_max = 0
    for i in dict_with_arc:
        if max(len_max, len(dict_with_arc[i])) > len_max:
            dict_with_arc = {i: dict_with_arc[i]}
    return dict_with_arc


def calculate_y_coordinate(dict_with_circles,y_height_center):
    count_y_coords = set()#Поиск всех координат y по окружностям и дугам(т.е. верхняя y,нижняя и тд)
    if dict_with_circles == {}:#Если нет ни дуг, ни окружностей, скорее всего там блоками все
        return y_height_center
    else:
        for x_coordinate in dict_with_circles:
            len_dict = len(dict_with_circles[x_coordinate])
            #Поиск всех координат y по окружностям и дугам(т.е. верхняя y,нижняя и тд)
            for circle_or_arc in dict_with_circles[x_coordinate]:
                if round(circle_or_arc.dxf.center[1],1) not in count_y_coords:
                    count_y_coords.add(round(circle_or_arc.dxf.center[1],1))

            if abs(y_height_center - ((max(count_y_coords) + min(count_y_coords))/2)) <= ((max(count_y_coords) - min(count_y_coords))/4):
                return (max(count_y_coords) + min(count_y_coords))/2
            else:
                return y_height_center


def move_all_entities(block):
    '''Передвижение элементов в блоке'''
    for hatch in block.entity_space:
        if hatch.dxftype() == 'HATCH':
            print(hatch)

def check_main_color_terminal(block):
    hatch_color = 0
    for hatch in block.entity_space:
        if hatch.dxftype() == 'HATCH':
            hatch_color = max(hatch_color,hatch.dxf.color)
    return int(hatch_color)
    
def define_hatch_color(hatch_color:int) -> str:
    if hatch_color == 0:
        return 'black'
    elif hatch_color == 1 or (10<= hatch_color <= 28):
        return 'red'
    elif hatch_color == 2 or (30<= hatch_color <=55):
        return 'yellow'
    elif hatch_color == 3 or (60 <= hatch_color <=110):
        return 'green'
    elif hatch_color == 5 or (120 <= hatch_color <= 185):
        return 'blue'
    elif hatch_color == 7:
        return 'white'

def sorted_dictforrename_by_color(dict_for_rename:dict) -> dict:
    for color in dict_for_rename.copy():
        a = dict_for_rename[color]
        b = dict(sorted(a.items(),key=lambda x: x[1]))
        dict_for_rename[color] = b
    return dict_for_rename

def create_name_block(manufacturer, terminal_type, color, cross_section):
    return f'{manufacturer}_{terminal_type}_{color}_{cross_section}'

def create_tree_blocks(doc):
    tree_with_all_blocks = dict()
    for someblock in doc.blocks:
        if '*' not in someblock.dxf.name:
            inserts_in_someblock = dict() #{Имя инсерта: координаты его в блоке}
            for insert in someblock:
                if insert.dxftype() == 'INSERT':
                    inserts_in_someblock[insert.dxf.name] = insert.dxf.insert
            tree_with_all_blocks[someblock.dxf.name] = inserts_in_someblock
    '''itertools.chain разворачивает цепь полностью'''

    return tree_with_all_blocks


def create_set_name_block_in_block(tree_dict:dict)->list:
    set_values_three = set(itertools.chain(*list(tree_dict.values())))
    list_with_main_terminals = set(tree_dict.keys())

    set_with_main_terminals = sorted(list_with_main_terminals - set_values_three,key=lambda x: int(x[1:]))  # Это терминалы и у них будут основные имена
    return set_with_main_terminals

def check_insert_in_block(doc,dict_oldname_key_new_name_value:dict, dict_with_block_in_block_and_insert:dict):
    dict_oldname_key_new_name_value_copy = dict_oldname_key_new_name_value.copy()
    dict_with_block_in_block_and_insert_copy = dict_with_block_in_block_and_insert.copy()
    a = []
    b ={}
    while any(list(dict_with_block_in_block_and_insert_copy.values())):
        for old_name, new_name in dict_oldname_key_new_name_value_copy.items():
            if dict_with_block_in_block_and_insert_copy[old_name] != {}:
                for i in dict_with_block_in_block_and_insert_copy[old_name]:
                    dict_oldname_key_new_name_value_copy[i] = new_name + '' + i


def rename_dict_in_terminal(doc,tree_with_all_blocks:dict,dict_oldname_key_new_name_value:dict, manufacturer:str,terminal_type:str):
    '''Уже есть переименнованные блоки main_terminal_name'''

    circle_was_done = [] # прошедшие по итерации

    tree_with_all_blocks_deliting = tree_with_all_blocks.copy()

    old_name_new_name = dict_oldname_key_new_name_value.copy()

    names_after_change = list(dict_oldname_key_new_name_value.keys())

    while circle_was_done != list(old_name_new_name.keys()):
        for old_name in old_name_new_name.copy():
            if old_name not in circle_was_done:
                dict_name_key_coordinate_value = tree_with_all_blocks_deliting[old_name]
                for name_insert, value_vec3 in dict_name_key_coordinate_value.items():
                    old_name_new_name[name_insert] = old_name_new_name[old_name] + '_' + name_insert
                circle_was_done.append(old_name)

    for old_name,new_name in old_name_new_name.items():
        doc.blocks.rename_block(old_name,new_name)

    for old_name,new_name in old_name_new_name.items():
        for old_name_in_block, vec_3_in_block in tree_with_all_blocks_deliting[old_name].items():
            doc.blocks[new_name].add_blockref(old_name_new_name[old_name_in_block],
                                                 vec_3_in_block)


if __name__ == '__main__':
    doc = ezdxf.readfile('testSupu.dxf')
    msp = doc.modelspace()
    three_blocks:dict = create_tree_blocks(doc)
    set_with_mainterminal_block_names = create_set_name_block_in_block(three_blocks)
    dict_for_rename = dict()
    for block in doc.blocks:
        if check_that_the_block_is_terminal(block,set_main_terminals=set_with_mainterminal_block_names):
            #Вынесли заливки правильно для каждого блока
            set_hatch_before_entity(block)
            #Получили словарь с горизонтальными линиями
            dict_with_horizontal_lines = create_dict_with_horizontal_lines(block)
            #Получили словарь с вертикальными линиями
            dict_with_vertical_lines = create_dict_with_vertical_lines(block)
            #Получили максимальную высоту прямоугольника и центр по максимальной длине
            terminal_height, y_height_center = calculate_center_y_coordinate(dict_with_vertical_lines)
            #Получаем длину клеммы и координату x_coordinate
            terminal_len, x_coordinate_block = list(calculate_x_coordinate(dict_with_horizontal_lines).items())[0]
            #Получаем список центров окружностей
            dict_with_circles = create_dict_with_circles(block)
            #Получаем y_coordinate
            y_coordinate = calculate_y_coordinate(dict_with_circles,y_height_center)
            print(block.dxf.name)
            print(y_coordinate)
            #Получаем основной цвет клеммы
            number_of_main_color = check_main_color_terminal(block)
            main_color = define_hatch_color(number_of_main_color)

            #Передвигаем base_point в центр клеммы
            #ТЕ КОТОРЫЕ НЕ ПЕРЕМЕСТИЛИСЬ, НАДО ОБРАБОТАТЬ ДРУГОЙ ЛОГИКОЙ
            try:
                block.block.dxf.base_point = (x_coordinate_block,y_coordinate,0)
            except BaseException:
                print('exception')

            if main_color not in dict_for_rename:
                dict_for_rename[main_color] = {block:terminal_len}
            else:
                dict_for_rename[main_color][block] = terminal_len

    #Сортировка клемм по размерам по цветам и получение словаря dict_for_rename
    sorted_dict_for_rename = sorted_dictforrename_by_color(dict_for_rename)
    olds_names = dict()
    '''ПОДГОТОВКА В РЕНЕЙМИНГУ MANUFACTURER ВНАЧАЛЕ ОПРЕДЕЛЯЕТСЯ, ЦВЕТ ЗНАЕМ, СЕЧЕНИЕ ЗНАЕМ, ТИП КЛЕММЫ БУДЕМ ДАВАТЬ ТОГДА КОНСТАНТОЙ'''
    for color in sorted_dict_for_rename:
        for block in list(sorted_dict_for_rename[color].items()):
            msp.add_blockref(block[0].dxf.name, insert = (0,0))
            old_name = block[0].dxf.name
            block_rename = create_name_block(
                manufacturer= MANUFACTURER.upper(),
                terminal_type= TERMINAL_TYPE.upper(),
                color= color.upper(),
                cross_section= CROSS_SECTION_DIAMETR[list(sorted_dict_for_rename[color].items()).index(block)])
            olds_names[old_name] = block_rename
            # doc.blocks.rename_block(old_name, block_rename) # Я думаю надо переименовывать позже
    rename_dict_in_terminal(doc,
                            tree_with_all_blocks=three_blocks,
                            dict_oldname_key_new_name_value=olds_names,
                            manufacturer=MANUFACTURER,
                            terminal_type=TERMINAL_TYPE)

    doc.modelspace().delete_all_entities()
    # doc.modelspace().add_blockref('SUPU_SCREW_WHITE_16',insert=(0,0))
    
    zoom.window(doc.modelspace(),(-200,200),(200,-200))
    doc.saveas('checkcheck.dxf')

