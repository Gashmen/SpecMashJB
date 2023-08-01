'''ДАННЫЙ МОДУЛЬ НАПРАВЛЕН ТОЛЬКО НА ПЕРЕМЕЩЕНИЕ БЛОКОВ ПОСЛЕ ИХ ПОСТРОЕНИЯ НА МОДЕЛСПЕЙСЕ'''
import math

from src.dxf_creating import search_len_block,shell_create,CONST

def move_shells_after_inputs(doc,shell_name:str):
    '''Перемещение оболочек после вставки вводов на оболочки, но еще не поставили инпутс на топсайд
    doc: doc после вставки inputs
    shell_name: VP.161610
    '''
    sides = ['_upside','_downside','_rightside','_leftside']
    #Сначала получаем все имена инпутс
    names_inputs_with_ex = list() #Т.к. имена в блоках VZ-N25_exe, а нужно _withoutcapside

    for shell_side in sides:
        for block_entities in doc.blocks[shell_name + shell_side]:
            if block_entities.dxftype() == 'INSERT':
                if '_exe' or '_exd' in block_entities.dxf.name:
                    names_inputs_with_ex.append(block_entities.dxf.name.split('_')[0])
    #Ищем максимальную длину кабельного ввода
    inputs_max_len = search_len_block.define_max_length_input(
                                                     doc = doc,
                                                     list_inputs_name_after_translit= list(set(names_inputs_with_ex)))
    #Отодвигаем все сайды оболочки на длину максимального кабельного ввода
    for insert in doc.modelspace().query('INSERT'):
        if '_rightside' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] - 2*inputs_max_len, insert.dxf.insert[1])
        if '_leftside' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] + inputs_max_len, insert.dxf.insert[1])
        if '_downside' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] , insert.dxf.insert[1] + inputs_max_len)
        if '_upside' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0], insert.dxf.insert[1] - 2*inputs_max_len)
        if '_cutside' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] + 2 * inputs_max_len, insert.dxf.insert[1])
        if '_withoutcapside' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] + 3 * inputs_max_len, insert.dxf.insert[1])
        if '_installation' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] + 3 * inputs_max_len, insert.dxf.insert[1]+inputs_max_len)
        if 'DIN' in insert.dxf.name:
            insert.dxf.insert = (insert.dxf.insert[0] + 3 * inputs_max_len, insert.dxf.insert[1])
    return inputs_max_len


def get_boundaries_drawing(doc, shell_name:str, input_max_len:round):
    '''
    Выдает координаты границ чертежа (x_max,x_min,y_max,y_min)
    :param doc:doc после передвижения всех блоков
    :param shell_name: VP.161610
    :param input_max_len: 35.865
    :return:{'x_left':x_min,....)
    '''
    rightside_insert = [insert for insert in doc.modelspace().query(f'INSERT[name == "{shell_name}_rightside"]')][0]
    upside_insert = [insert for insert in doc.modelspace().query(f'INSERT[name == "{shell_name}_upside"]')][0]
    withoutcapside_insert = [insert for insert in doc.modelspace().query(f'INSERT[name == "{shell_name}_withoutcapside"]')][0]

    x_min = shell_create.define_extreme_lines_in_insert(rightside_insert)['x_min']
    y_min = shell_create.define_extreme_lines_in_insert(upside_insert)['y_min']

    x_max = shell_create.define_extreme_lines_in_insert(withoutcapside_insert)['x_max'] + input_max_len
    y_max = None

    for insert_installation in doc.modelspace().query(f'INSERT[name=="{shell_name}_installation_dimensions"]'):
        for mtext in insert_installation.virtual_entities():
            if mtext.dxftype() == 'MTEXT':
                y_max = mtext.dxf.insert[1]

    return {'x_left':x_min,'x_right':x_max,'y_down':y_min,'y_up':y_max}


def define_scale(doc,shell_name:str,input_max_len:round, boundaries:dict = CONST.A3_BOUNDARIES):
    '''
    Определяем масштаб, который необходим для вписывания оболочек в рамку, по дефолту в рамку А3.
    Условия для проверки прописаны в NOTION,
    ВСЕ ОНИ ДОЛЖНЫ СОБЛЮДАТЬСЯ:
    [len1 + len3 + 2 * len2 <= boundaries['LEN_X_НИЖНЯЯ_ГРАНИЦА'],
                          len4 + len2 >= boundaries['LEN_Y_НИЖНЯЯ_ГРАНИЦА'] - boundaries['LEN_Y_ВЕРХНЯЯ_ГРАНИЦА'],
                          len2 + len5 + len2 + len_mtext <= boundaries['LEN_Y_ВЕРХНЯЯ_ГРАНИЦА'],
                          len1 + len2 + len3 + len2 + len1 + len2 + len1 + len2 + len3 + len2 <= boundaries[
                              'LEN_X_ВЕРХНЯЯ_ГРАНИЦА']]
    :param doc: doc, после того как все подвинули
    :param shell_name: VP.161610
    :param input_max_len: 35.865
    :param boundaries: {'LEN_X_НИЖНЯЯ_ГРАНИЦА': 210,'LEN_Y_НИЖНЯЯ_ГРАНИЦА': 287,'LEN_X_ВЕРХНЯЯ_ГРАНИЦА': 395,
                        'LEN_Y_ВЕРХНЯЯ_ГРАНИЦА': 232}
    :return: 2.5
    '''

    rightside_insert = [insert for insert in doc.modelspace().query(f'INSERT[name == "{shell_name}_rightside"]')][0]

    len1= shell_create.define_extreme_lines_in_insert(rightside_insert)['x_max'] - \
          shell_create.define_extreme_lines_in_insert(rightside_insert)['x_min']

    len2 = input_max_len

    topside_insert = [insert for insert in doc.modelspace().query(f'INSERT[name == "{shell_name}_topside"]')][0]

    len3 = shell_create.define_extreme_lines_in_insert(topside_insert)['x_max'] - \
          shell_create.define_extreme_lines_in_insert(topside_insert)['x_min']

    len4 = len1

    len5 = shell_create.define_extreme_lines_in_insert(topside_insert)['y_max'] - \
          shell_create.define_extreme_lines_in_insert(topside_insert)['y_min']

    installation_insert = [insert for insert in doc.modelspace().query(f'INSERT[name == "{shell_name}_installation_dimensions"]')][0]

    len_mtext = [mtext.dxf.insert for mtext in installation_insert.virtual_entities() if mtext.dxftype() == 'MTEXT'][0][1] -\
                shell_create.define_extreme_lines_in_insert(installation_insert)['y_min']

    conditions = all([math.floor(len1 + len3 + 2*len2) <= boundaries['LEN_X_НИЖНЯЯ_ГРАНИЦА'],
                      math.floor(len4 + len2) <= boundaries['LEN_Y_НИЖНЯЯ_ГРАНИЦА'] - boundaries['LEN_Y_ВЕРХНЯЯ_ГРАНИЦА'],
                      math.floor(len2 + len5 + len2 +len_mtext) <= boundaries['LEN_Y_ВЕРХНЯЯ_ГРАНИЦА'],
                      math.floor(len1+len2+len3+len2+len1+len2+len1+len2+len3+len2) <= boundaries['LEN_X_ВЕРХНЯЯ_ГРАНИЦА']])
    i = -1
    while conditions == False:
        i += 1

        conditions = \
            all([math.floor(len1/(CONST.SCALE_GOST[i]) + len3/(CONST.SCALE_GOST[i]) + 2 * len2/(CONST.SCALE_GOST[i]))
                 <= boundaries['LEN_X_НИЖНЯЯ_ГРАНИЦА'],

                 math.floor(len4/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i]))
                 <= boundaries['LEN_Y_НИЖНЯЯ_ГРАНИЦА'] - boundaries['LEN_Y_ВЕРХНЯЯ_ГРАНИЦА'],

                 math.floor(len2/(CONST.SCALE_GOST[i]) + len5/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i]) + len_mtext/(CONST.SCALE_GOST[i]))
                 <= boundaries['LEN_Y_ВЕРХНЯЯ_ГРАНИЦА'],

                 math.floor(len1/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i]) + len3/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i])
                 + len1/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i]) + len1/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i])
                 + len3/(CONST.SCALE_GOST[i]) + len2/(CONST.SCALE_GOST[i]))
                 <= boundaries['LEN_X_ВЕРХНЯЯ_ГРАНИЦА']])
    if i == -1:
        return 1
    else:
        return CONST.SCALE_GOST[i]

def scale_all_insert(doc, scale):
    '''
    Устанавливаем расчитаный масштаб
    :param doc: Док после вставки всех insertov!!!!
    :param scale: 2.5
    :return: doc
    '''
    for entity_insert in doc.modelspace().query('INSERT'):
        entity_insert.scale_uniform(1/scale)
    return doc

def move_all_blocks_vertical_after_add_border(doc,shell_name:str,border_name='Border_A3',input_max_len = 0.0):
    '''Перемещение блоков вдоль координаты y после вставки рамки
    doc: doc после вставки border и уже все нанесено
    shell_name: VP.161610
    border_name: Border_A3
    '''

    #Определение блоков перемещения
    border_insert = doc.modelspace().query(f'INSERT[name=="{border_name}"]')[0]

    upside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_upside"]')[0]
    upside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert=upside_insert)

    topside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_topside"]')[0]
    rightside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_rightside"]')[0]
    leftside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_leftside"]')[0]
    cutside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_cutside"]')[0]
    instalation_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_installation_dimensions"]')[0]
    din_insert = [insert for insert in doc.modelspace().query(f'INSERT') if 'DIN' in insert.dxf.name][0]

    withoutside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_withoutcapside"]')[0]
    withoutside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert = withoutside_insert)

    downside_insert = doc.modelspace().query(f'INSERT[name=="{shell_name}_downside"]')[0]
    downside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert = downside_insert)

    withoutcap_insert_topside = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withoutcap')
                                 if (rightside_insert.dxf.insert[0] < insert.dxf.insert[0]< leftside_insert.dxf.insert[0]) and
                                    (upside_insert.dxf.insert[1] < insert.dxf.insert[1]< downside_insert.dxf.insert[1])]

    withoutcap_insert_rightside = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withoutcap')
                                 if (insert.dxf.insert[0] < rightside_insert.dxf.insert[0]) and
                                 (upside_insert.dxf.insert[1] < insert.dxf.insert[1] < downside_insert.dxf.insert[1])]

    withoutcap_insert_leftside = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withoutcap')
                                   if (leftside_insert.dxf.insert[0] < insert.dxf.insert[0]< cutside_insert.dxf.insert[0]) and
                                   (upside_insert.dxf.insert[1] < insert.dxf.insert[1] <downside_insert.dxf.insert[1])]

    withoutcap_insert_cutside = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withoutcap')
                                  if (cutside_insert.dxf.insert[0] < insert.dxf.insert[0] < withoutside_insert.dxf.insert[0]) and
                                  (upside_insert.dxf.insert[1] < insert.dxf.insert[1] <downside_insert.dxf.insert[1])]

    withoutcap_insert_upside = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withoutcap')
                                 if (rightside_insert.dxf.insert[0] < insert.dxf.insert[0]< leftside_insert.dxf.insert[0]) and
                                    (insert.dxf.insert[1]< upside_insert.dxf.insert[1])]

    withoutcap_insert_downside = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withoutcap')
                                 if (rightside_insert.dxf.insert[0] < insert.dxf.insert[0]< leftside_insert.dxf.insert[0]) and
                                    (insert.dxf.insert[1] > downside_insert.dxf.insert[1])]


    withcap_insert = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('withcap')]

    viewsides_insert = [insert for insert in doc.modelspace().query('INSERT') if insert.dxf.name.endswith('viewside')]

    CONST_Y_SHELL = None
    if border_name == 'Border_A3':
        #Движение по y
        CONST_Y_SHELL = CONST.A3_BOUNDARIES['LEN_Y_НИЖНЯЯ_ГРАНИЦА'] - CONST.A3_BOUNDARIES['LEN_TOP_HEADER']

    CONST_X_SHELL = None
    if border_name == 'Border_A3':
        #Движение по х
        CONST_X_SHELL = CONST.A3_BOUNDARIES['LEN_X_ВЕРХНЯЯ_ГРАНИЦА']

    delta_x_length_max = CONST_X_SHELL + border_insert.dxf.insert[0] - withoutside_extreme_lines['x_max'] - input_max_len
    delta_y_length_max = CONST_Y_SHELL + border_insert.dxf.insert[1] - downside_extreme_lines['y_max']

    downside_new_insert_x = downside_insert.dxf.insert[0] + delta_x_length_max * (2/6)
    downside_new_insert_y = downside_insert.dxf.insert[1] + delta_y_length_max * (3/4)
    downside_insert.dxf.insert = (downside_new_insert_x,downside_new_insert_y)

    instalation_new_insert_x = instalation_insert.dxf.insert[0] + delta_x_length_max * (5 / 6)
    instalation_new_insert_y = instalation_insert.dxf.insert[1] + delta_y_length_max * (3 / 4)
    instalation_insert.dxf.insert = (instalation_new_insert_x,instalation_new_insert_y)

    topside_new_insert_x = topside_insert.dxf.insert[0] + delta_x_length_max*(2/6)
    topside_new_insert_y = topside_insert.dxf.insert[1] + delta_y_length_max*(2/4)
    topside_insert.dxf.insert = (topside_new_insert_x,topside_new_insert_y)

    rightside_new_insert_x = rightside_insert.dxf.insert[0] + delta_x_length_max*(1/6)
    rightside_new_insert_y = rightside_insert.dxf.insert[1] + delta_y_length_max*(2/4)
    rightside_insert.dxf.insert = (rightside_new_insert_x,rightside_new_insert_y)

    leftside_new_insert_x = leftside_insert.dxf.insert[0] + delta_x_length_max*(3/6)
    leftside_new_insert_y = leftside_insert.dxf.insert[1]+delta_y_length_max*(2/4)
    leftside_insert.dxf.insert = (leftside_new_insert_x,leftside_new_insert_y)

    cutside_new_insert_x = cutside_insert.dxf.insert[0] + delta_x_length_max * (4 / 6)
    cutside_new_insert_y = cutside_insert.dxf.insert[1] + delta_y_length_max * (2 / 4)
    cutside_insert.dxf.insert = (cutside_new_insert_x,cutside_new_insert_y)

    withoutside_new_insert_x = withoutside_insert.dxf.insert[0] + delta_x_length_max * (5 / 6)
    withoutside_new_insert_y = withoutside_insert.dxf.insert[1] + delta_y_length_max * (2 / 4)
    withoutside_insert.dxf.insert = (withoutside_new_insert_x,withoutside_new_insert_y)

    for input_insert_without_rightside in withoutcap_insert_rightside:
        input_insert_without_new_insert_x = input_insert_without_rightside.dxf.insert[0] + delta_x_length_max * (1 / 6)
        input_insert_without_new_insert_y = input_insert_without_rightside.dxf.insert[1] + delta_y_length_max * (2 / 4)
        input_insert_without_rightside.dxf.insert = (input_insert_without_new_insert_x, input_insert_without_new_insert_y)

    for input_insert_without_topside in withoutcap_insert_topside:
        input_insert_without_new_insert_x = input_insert_without_topside.dxf.insert[0] + delta_x_length_max*(2/6)
        input_insert_without_new_insert_y = input_insert_without_topside.dxf.insert[1] + delta_y_length_max*(2/4)
        input_insert_without_topside.dxf.insert = (input_insert_without_new_insert_x,input_insert_without_new_insert_y)

    for input_insert_without_leftside in withoutcap_insert_leftside:
        input_insert_without_new_insert_x = input_insert_without_leftside.dxf.insert[0] + delta_x_length_max * (3 / 6)
        input_insert_without_new_insert_y = input_insert_without_leftside.dxf.insert[1] + delta_y_length_max * (2 / 4)
        input_insert_without_leftside.dxf.insert = (input_insert_without_new_insert_x, input_insert_without_new_insert_y)

    for input_insert_without_cutside in withoutcap_insert_cutside:
        input_insert_without_new_insert_x = input_insert_without_cutside.dxf.insert[0] + delta_x_length_max * (4 / 6)
        input_insert_without_new_insert_y = input_insert_without_cutside.dxf.insert[1] + delta_y_length_max * (2 / 4)
        input_insert_without_cutside.dxf.insert = (input_insert_without_new_insert_x, input_insert_without_new_insert_y)

    for input_insert_without_upside in withoutcap_insert_upside:
        input_insert_without_new_insert_x = input_insert_without_upside.dxf.insert[0] + delta_x_length_max*(2/6)
        input_insert_without_new_insert_y = input_insert_without_upside.dxf.insert[1] + delta_y_length_max*(1/4)
        input_insert_without_upside.dxf.insert = (input_insert_without_new_insert_x,input_insert_without_new_insert_y)

    for input_insert_without_downside in withoutcap_insert_downside:
        input_insert_without_new_insert_x = input_insert_without_downside.dxf.insert[0] + delta_x_length_max*(2/6)
        input_insert_without_new_insert_y = input_insert_without_downside.dxf.insert[1] + delta_y_length_max*(3/4)
        input_insert_without_downside.dxf.insert = (input_insert_without_new_insert_x,input_insert_without_new_insert_y)


    for input_insert_with in withcap_insert:
        input_insert_with_new_insert_x = input_insert_with.dxf.insert[0] + delta_x_length_max * (5 / 6)
        input_insert_with_new_insert_y = input_insert_with.dxf.insert[1] + delta_y_length_max * (2 / 4)
        input_insert_with.dxf.insert = (input_insert_with_new_insert_x,input_insert_with_new_insert_y)

    for terminal in [insert for insert in doc.modelspace().query('INSERT')
                     if insert!=din_insert and insert.dxf.insert[1] == din_insert.dxf.insert[1]]:
        terminal_new_insert_x = terminal.dxf.insert[0] + delta_x_length_max * (5/6)
        terminal_new_insert_y = terminal.dxf.insert[1] + delta_y_length_max * (2/4)
        terminal.dxf.insert = (terminal_new_insert_x,terminal_new_insert_y)

    for viewside in viewsides_insert:
        viewside_new_insert_x = viewside.dxf.insert[0] + delta_x_length_max * (4 / 6)
        viewside_new_insert_y = viewside.dxf.insert[1] +delta_y_length_max*(2/4)
        viewside.dxf.insert = (viewside_new_insert_x,viewside_new_insert_y)

    din_new_insert_x = din_insert.dxf.insert[0] + delta_x_length_max * (5 / 6)
    din_new_insert_y = din_insert.dxf.insert[1]+delta_y_length_max*(2/4)
    din_insert.dxf.insert = (din_new_insert_x,din_new_insert_y)

    upside_new_insert_x = upside_insert.dxf.insert[0] + delta_x_length_max*(2/6)
    upside_new_insert_y = upside_insert.dxf.insert[1] + delta_y_length_max*(1/4)
    upside_insert.dxf.insert = (upside_new_insert_x, upside_new_insert_y)
