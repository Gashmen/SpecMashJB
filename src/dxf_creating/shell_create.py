
def create_list_for_draw_shell(shell_name:str)->list[str]:
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

def topside_insert(doc,shell_name):
    '''Поиск INSERT topside'''
    for insert_topside in doc.modelspace():
        if insert_topside.dxf.name.endswith('topside') and shell_name in insert_topside.dxf.name:
            return insert_topside

def create_shell_sides(doc, shell_name,extreme_lines_in_all_blocks):
    type_of_add_rotation = {'_downside': 0, '_upside': 180, '_leftside': 270, '_rightside': 90}
    insert_topside = topside_insert(doc,shell_name)
    topside_extreme_lines = define_extreme_lines_in_insert(insert_topside)
    for type_of_add in type_of_add_rotation:
        if type_of_add.endswith('_downside'):
            insert_downside = (topside_extreme_lines['x_min'] - extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'],
                                topside_extreme_lines['y_max'] - extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'])
            add_downside = doc.modelspace().add_blockref(f'{shell_name}{type_of_add}',
                                                         insert=insert_downside)
            add_downside.dxf.rotation = 0
        elif type_of_add.endswith('_upside'):
            insert_upside = (topside_extreme_lines['x_max'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'],
                                topside_extreme_lines['y_min'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'])
            add_upside = doc.modelspace().add_blockref(f'{shell_name}{type_of_add}',
                                                         insert=insert_upside)
            add_upside.dxf.rotation = 180
        elif type_of_add.endswith('_rightside'):
            insert_rightside = (topside_extreme_lines['x_min'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'],
                               topside_extreme_lines['y_min'] - extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'])
            add_rightside = doc.modelspace().add_blockref(f'{shell_name}{type_of_add}',
                                                        insert_rightside)
            add_rightside.dxf.rotation = 90
        elif type_of_add.endswith('_leftside'):
            insert_leftside = (
            topside_extreme_lines['x_max'] - extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['y_min'],
            topside_extreme_lines['y_max'] + extreme_lines_in_all_blocks[f'{shell_name}{type_of_add}']['x_min'])

            add_leftside = doc.modelspace().add_blockref(f'{shell_name}{type_of_add}',
                                                         insert_leftside)
            add_leftside.dxf.rotation = 270

def leftside_insert(doc,shell_name):
    '''Поиск INSERT leftside'''
    for insert_leftside in doc.modelspace():
        if insert_leftside.dxf.name.endswith('leftside') and shell_name in insert_leftside.dxf.name:
            return insert_leftside

def create_cutside_shell(doc, shell_name,extreme_lines_in_all_blocks):
    '''Создает разрез справа'''
    insert_leftside = leftside_insert(doc, shell_name)
    leftside_extreme_lines = define_extreme_lines_in_insert(insert_leftside)
    insert_x_coordinate_cutside =  leftside_extreme_lines['x_max'] - \
                                   extreme_lines_in_all_blocks[f'{shell_name}_cutside']['y_min']
    insert_y_coordinate_cutside = leftside_extreme_lines['y_max'] + \
                                   extreme_lines_in_all_blocks[f'{shell_name}_cutside']['x_min']

    insert_cutside = doc.modelspace().add_blockref(name = f'{shell_name}_cutside',
                                                   insert = (insert_x_coordinate_cutside,insert_y_coordinate_cutside))
    insert_cutside.dxf.rotation = 270
    return insert_cutside

def create_withoutcapside_shell(doc,shell_name:str,extreme_lines_in_all_blocks:dict):
    '''
    :param doc:
    :param shell_name: VP.161609
    :param extreme_lines_in_all_blocks: {VP.161609_topside:{'y_min' : 133, ...}}
    :param cutside_insert: create_cutside_shell(doc, shell_name,extreme_lines_in_all_blocks)
    :return: withoutcapside_insert
    '''
    cutside_insert = create_cutside_shell(doc,shell_name,extreme_lines_in_all_blocks)
    extreme_lines_in_cutside_insert = define_extreme_lines_in_insert(cutside_insert)
    x_coordinate_insert = extreme_lines_in_cutside_insert['x_max'] - \
                          extreme_lines_in_all_blocks[f'{shell_name}_withoutcapside']['x_min']
    y_coordinate_insert = extreme_lines_in_cutside_insert['y_max'] - \
                          extreme_lines_in_all_blocks[f'{shell_name}_withoutcapside']['y_max']

    withoutcapside_insert = doc.modelspace().add_blockref(name = f'{shell_name}_withoutcapside',
                                                          insert = (x_coordinate_insert,y_coordinate_insert))
    return withoutcapside_insert

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

def create_all_shells(doc,shell_name:str, extreme_lines:dict):
    '''
    :param doc:
    :param shell_name:
    :param extreme_lines: {имя блока: {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}
    :return:
    '''
    msp = doc.modelspace()
    msp.add_blockref(f'{shell_name}_topside',insert=(0,0))
    all_blocks_extreme_lines = define_extreme_lines_in_all_blocks(doc)
    create_shell_sides(doc, shell_name, all_blocks_extreme_lines)
    create_cutside_shell(doc,shell_name, extreme_lines)
    create_withoutcapside_shell(doc,shell_name,extreme_lines)
    create_installation_dimensions(doc,shell_name,extreme_lines)
    create_din_reyka(doc,shell_name)
    return doc








