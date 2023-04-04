'''ЧАСТЬ ПОИСКА КРАЙНИХ ЛИНИЙ В БЛОКАХ И ИНСЕРТАХ'''
def define_extreme_lines_in_insert(insert):
    '''Поиск координат крайних точек по линиям на Modelspace
    :insert: Insert в моделспейсе
    :return:  {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    x = list()
    y = list()
    x_0 = tuple(insert.dxf.insert)[0:2]
    for line in insert.virtual_entities():
        if line.dxftype() == 'LINE':
            x.append(line.dxf.start[0])
            x.append(line.dxf.end[0])
            y.append(line.dxf.start[1])
            y.append(line.dxf.end[1])
    return {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}

def define_extreme_lines_in_block(block):
    '''Поиск координат крайних точек по линиям в блоке
    :block: Блок из doc.blocks
    :return:  {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}
    '''
    x = list()
    y = list()
    for line in block:
        if line.dxftype() == 'LINE':
            x.append(line.dxf.start[0])
            x.append(line.dxf.end[0])
            y.append(line.dxf.start[1])
            y.append(line.dxf.end[1])
    if x and y: #если есть коробка
        return {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}

def define_extreme_lines_in_all_blocks(doc):
    '''Определяем координаты крайние по всем блокам
    вид словаря : {имя блока: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}
    '''
    return_dict = dict()
    for block in doc.blocks:
        if '*' not in block.dxf.name and not block.dxf.name.startswith('U'):
            return_dict[block.dxf.name] = define_extreme_lines_in_block(block)
    return return_dict

'''Получаю список блоков, которые остануться после удаление из контейнера'''
def get_list_for_draw_shell(shell_name:str)->list[str]:
    '''
    Создает импорт лист для оболочки
    :param shell_name: VP.161610
    :return: return_list : [VP.161610_topside,...]
    '''

    sides = ('_downside','_upside','_leftside','_rightside','_topside','_cutside',
             '_withoutcapside',
             '_installation_dimensions')
    shell_name_sides = [shell_name + side for side in sides]
    shell_name_sides.append(f'DIN_{shell_name}')
    return shell_name_sides


'''ВИДЖЕТ СОЗДАНИЕ ОБОЛОЧЕК'''
def create_topside(doc,shell_name:str):
    '''
    Создает shell_topside в координатах 0,0
    :param doc: пустой лист со вставленными импортами блоками
    :param shell_name: VP.161610
    :return: topside_insert вставленный на моделспейс
    '''
    if f'{shell_name}_topside' in [block.name for block in doc.blocks]:
        topside_insert = doc.modelspace().add_blockref(name=f'{shell_name}_topside',
                                                       insert=(0,0))
        return topside_insert
    else:
        raise ValueError(f'Не был добавлен блок с именем {shell_name}_topside')

def calculate_extreme_lines_in_topside_insert(topside_insert):
    '''
    Расчет extreme_line insert у топсайд инсерт
    :param topside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''

    topside_insert_extreme_lines = define_extreme_lines_in_insert(topside_insert)
    return topside_insert_extreme_lines

def create_downside(doc,shell_name:str,extreme_line_all_blocks:dict,topside_extreme_lines:dict):
    '''
    Создает shell_downside в координатах
    (topside_extreme_lines['x_min'] - extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'],
    topside_extreme_lines['y_max'] - extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'])
    :param doc: лист со вставленным topside
    :param topside: VP.161610
    :return: downside_insert вставленный на моделспейс
    '''
    downside_insert_coordinate = (topside_extreme_lines['x_min'] -
                                  extreme_line_all_blocks[f'{shell_name}_downside']['x_min'],
                                  topside_extreme_lines['y_max'] -
                                  extreme_line_all_blocks[f'{shell_name}_downside']['y_min'])
    downside_insert = doc.modelspace().add_blockref(name=f'{shell_name}_downside',
                                                    insert=downside_insert_coordinate)
    downside_insert.dxf.rotation = 0
    return downside_insert

def calculate_extreme_lines_in_downside_insert(downside_insert):
    '''
    Расчет extreme_line insert у топсайд инсерт
    :param topside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    downside_insert_extreme_lines = define_extreme_lines_in_insert(downside_insert)
    return downside_insert_extreme_lines

def create_upside(doc,shell_name:str,extreme_line_all_blocks:dict,topside_extreme_lines:dict):
    '''
    Создает shell_downside в координатах
    (topside_extreme_lines['x_max'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'],
    topside_extreme_lines['y_min'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'])
    :param doc: лист со вставленным topside
    :param topside: VP.161610
    :return: downside_insert вставленный на моделспейс
    '''
    upside_insert_coordinate = (topside_extreme_lines['x_max'] +
                                extreme_line_all_blocks[f'{shell_name}_upside']['x_min'],
                                topside_extreme_lines['y_min'] +
                                extreme_line_all_blocks[f'{shell_name}_upside']['y_min'])
    upside_insert = doc.modelspace().add_blockref(name=f'{shell_name}_upside',
                                                    insert=upside_insert_coordinate)
    upside_insert.dxf.rotation = 180
    return upside_insert

def calculate_extreme_lines_in_upside_insert(upside_insert):
    '''
    Расчет extreme_line insert у upside инсерт
    :param upside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    upside_insert_extreme_lines = define_extreme_lines_in_insert(upside_insert)
    return upside_insert_extreme_lines

def create_leftside(doc,shell_name:str,extreme_line_all_blocks:dict,topside_extreme_lines:dict):
    '''
    Создает shell_downside в координатах
    (topside_extreme_lines['x_max'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'],
    topside_extreme_lines['y_min'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'])
    :param doc: лист со вставленным topside
    :param topside: VP.161610
    :return: downside_insert вставленный на моделспейс
    '''
    leftside_insert_coordinate = (topside_extreme_lines['x_max'] -
                                  extreme_line_all_blocks[f'{shell_name}_leftside']['y_min'],
                                  topside_extreme_lines['y_max'] +
                                  extreme_line_all_blocks[f'{shell_name}_leftside']['x_min'])
    leftside_insert = doc.modelspace().add_blockref(name=f'{shell_name}_leftside',
                                                    insert=leftside_insert_coordinate)
    leftside_insert.dxf.rotation = 270
    return leftside_insert

def calculate_extreme_lines_in_leftside_insert(leftside_insert):
    '''
    Расчет extreme_line insert у upside инсерт
    :param upside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    leftside_insert_extreme_lines = define_extreme_lines_in_insert(leftside_insert)
    return leftside_insert_extreme_lines

def create_rightside(doc,shell_name:str,extreme_line_all_blocks:dict,topside_extreme_lines:dict):
    '''
    Создает shell_downside в координатах
    (topside_extreme_lines['x_max'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'],
    topside_extreme_lines['y_min'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'])
    :param doc: лист со вставленным topside
    :param topside: VP.161610
    :return: downside_insert вставленный на моделспейс
    '''
    rightside_insert_coordinate = ((topside_extreme_lines['x_min'] +
                                   extreme_line_all_blocks[f'{shell_name}_rightside']['y_min'],
                                   topside_extreme_lines['y_min'] -
                                   extreme_line_all_blocks[f'{shell_name}_rightside']['x_min'])
)
    rightside_insert = doc.modelspace().add_blockref(name=f'{shell_name}_rightside',
                                                    insert=rightside_insert_coordinate)
    rightside_insert.dxf.rotation = 90
    return rightside_insert

def calculate_extreme_lines_in_rightside_insert(rightside_insert):
    '''
    Расчет extreme_line insert у upside инсерт
    :param upside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    rightside_insert_extreme_lines = define_extreme_lines_in_insert(rightside_insert)
    return rightside_insert_extreme_lines

def create_cutside_shell(doc,shell_name:str,extreme_line_all_blocks:dict,leftside_extreme_lines:dict):
    '''Создает разрез справа'''
    insert_x_coordinate_cutside = leftside_extreme_lines['x_max'] - \
                                   extreme_line_all_blocks[f'{shell_name}_cutside']['y_min']
    insert_y_coordinate_cutside = leftside_extreme_lines['y_max'] + \
                                   extreme_line_all_blocks[f'{shell_name}_cutside']['x_min']

    insert_cutside = doc.modelspace().add_blockref(name = f'{shell_name}_cutside',
                                                   insert = (insert_x_coordinate_cutside,insert_y_coordinate_cutside))
    insert_cutside.dxf.rotation = 270
    return insert_cutside

def calculate_extreme_lines_in_cutside_insert(cutside_insert):
    '''
    Расчет extreme_line insert у upside инсерт
    :param upside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    cutside_insert_extreme_lines = define_extreme_lines_in_insert(cutside_insert)
    return cutside_insert_extreme_lines

def create_withoutcapside_shell(doc,shell_name:str,extreme_line_in_all_blocks:dict,cutside_extreme_lines:dict):
    '''
    :param doc:
    :param shell_name: VP.161609
    :param extreme_lines_in_all_blocks: {VP.161609_topside:{'y_min' : 133, ...}}
    :param cutside_insert: create_cutside_shell(doc, shell_name,extreme_lines_in_all_blocks)
    :return: withoutcapside_insert
    '''
    x_coordinate_insert = cutside_extreme_lines['x_max'] - \
                          extreme_line_in_all_blocks[f'{shell_name}_withoutcapside']['x_min']
    y_coordinate_insert = cutside_extreme_lines['y_max'] - \
                          extreme_line_in_all_blocks[f'{shell_name}_withoutcapside']['y_max']

    withoutcapside_insert = doc.modelspace().add_blockref(name = f'{shell_name}_withoutcapside',
                                                          insert = (x_coordinate_insert,y_coordinate_insert))
    return withoutcapside_insert

def calculate_extreme_lines_in_withoutcapside_insert(withoutcapside_insert):
    '''
    Расчет extreme_line insert у upside инсерт
    :param upside_insert: shell_name_topside
    :return: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y), 'xy_0': x_0}
    '''
    withoutcapside_insert_extreme_lines = define_extreme_lines_in_insert(withoutcapside_insert)
    return withoutcapside_insert_extreme_lines

def create_installation_dimensions(doc,shell_name:str,extreme_lines_in_all_blocks:dict):
    '''
    :param doc:
    :param shell_name: VP.161609
    :param extreme_lines_in_all_blocks: {VP.161609_topside:{'y_min' : 133, ...}}
    :param cutside_insert: create_withoutcapside_shell(doc,shell_name:str,extreme_lines_in_all_blocks:dict,cutside_insert)
    :return: installation_dimensions_insert
    '''
    withoutcapside_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_withoutcapside"]')[0]
    extreme_lines_in_withoutcapside_insert = define_extreme_lines_in_insert(withoutcapside_insert)
    x_coordinate_insert = withoutcapside_insert.dxf.insert[0]

    min_dimension_line_coordinate = 0
    for entity in doc.blocks[f'{shell_name}_installation_dimensions']:
        if entity.dxftype() == 'DIMENSION':
            for virtual_entity in entity.virtual_entities():
                if virtual_entity.dxftype() == 'LINE':
                    min_dimension_line_coordinate = min(min_dimension_line_coordinate,
                                                        virtual_entity.dxf.start[1],
                                                        virtual_entity.dxf.end[1])

    '''Если размеры сверху, то точка вставки по y = крайная точка without_capside и высота нижней линии'''
    if min_dimension_line_coordinate > 0 :
        y_coordinate_insert = extreme_lines_in_withoutcapside_insert['y_max'] - \
                              extreme_lines_in_all_blocks[f'{shell_name}_installation_dimensions']['y_min']
    else:
        y_coordinate_insert = extreme_lines_in_withoutcapside_insert['y_max'] - \
                              min_dimension_line_coordinate

    installation_dimensions = doc.modelspace().add_blockref(name=f'{shell_name}_installation_dimensions',
                                                          insert=(x_coordinate_insert, y_coordinate_insert))
    return installation_dimensions

def create_din_reyka(doc,shell_name:str):
    '''
    :param doc: doc после добавления всех видов и их передвижения
    :param shell_name: VP.161609
    :return:
    '''
    withoutcapside_insert = doc.modelspace().query(f'INSERT[name == "{shell_name}_withoutcapside"]')[0]
    din_reyka = doc.modelspace().add_blockref(name=f'DIN_{shell_name}',
                                              insert= withoutcapside_insert.dxf.insert)
    din_reyka.set_scale(1)
    return din_reyka










