import ezdxf

start_dict = {'Сборочные единицы': [{'Обозначение': 'ВРПТ.301172.024-11',
                                     'Наименование': 'Оболочка ВП.161610',
                                     'Формат': 'А4', 'Кол.': None, 'Примечание': None},
                                    {'Обозначение': 'ВРПТ.305311.001-025',
                                     'Наименование': 'Кабельный ввод ВЗ-Н25#для не бронированного#кабеля, диаметром 12-18мм',
                                     'Формат': 'А4', 'Кол.': None, 'Примечание': None}],
              'Стандартные изделия': [{'Обозначение': None,
                                       'Наименование': 'Винт А2.М6-6gx10.019#ГОСТ 17473-80',
                                       'Формат': 'А4', 'Кол.': None, 'Примечание': None},
                                      {'Обозначение': None,
                                       'Наименование': 'Шайба 6 019 ГОСТ 6402-70',
                                       'Формат': 'А4', 'Кол.': None, 'Примечание': None},
                                      {'Обозначение': None,
                                       'Наименование': 'Шайба A.6.019 ГОСТ 11371-78',
                                       'Формат': 'А4', 'Кол.': None, 'Примечание': None}],
              'Детали':               [{'Обозначение': 'ВРПТ.745551.005-140',
                                        'Наименование': 'DIN-рейка NS35х7,5, L=140 мм',
                                        'Формат': 'А4', 'Кол.': None, 'Примечание': None}]}

tag_in_BOM_dxf = {'Формат':'A', 'Зона':'B', 'Поз.':'C', 'Обозначение':'D', 'Наименование':'E', 'Кол.': 'F', 'Примечание':'G'}

return_dict = dict()

'''Создание dxf, block и INSERT'''
def create_doc_BOM(dxfbase_path:str, number_BOM_page:int):
    '''Создает BOM удаляя все не нужное'''
    doc_bom = ezdxf.readfile(dxfbase_path)

    doc_dxfbase_for_del = ezdxf.readfile(dxfbase_path)

    doc_bom.modelspace().delete_all_entities()

    if number_BOM_page == 1:

        blocks_BOM = ['BOM_FIRST']

    elif number_BOM_page > 1:

        blocks_BOM = ['BOM_SECOND']

    for block in doc_dxfbase_for_del.blocks:
        try:
            if block.dxf.name not in blocks_BOM and '*' not in block.dxf.name:
                    doc_bom.blocks.delete_block(name=block.dxf.name)
        except:
            continue
    return doc_bom

def create_BOM_FIRST(doc_bom):
    '''Создает первый лист спецификации'''

    block_border = doc_bom.blocks['BOM_FIRST']
    values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
    if doc_bom.blocks.get('BOM_FIRST'):
        border_insert = doc_bom.modelspace().add_blockref(name='BOM_FIRST',
                                                          insert=(0, 0))
        border_insert.add_auto_attribs(values)

        return border_insert

def create_BOM_SECOND(doc_bom):
    '''Создает первый лист спецификации'''

    block_border = doc_bom.blocks['BOM_SECOND']
    values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
    if doc_bom.blocks.get('BOM_SECOND'):
        border_insert = doc_bom.modelspace().add_blockref(name='BOM_SECOND',
                                                          insert=(0, 0))
        border_insert.add_auto_attribs(values)

        return border_insert

def create_new_BOM_dxf(dxfbase_path:str, number_BOM_page:int):
    '''
    Создает новый BOM, при переходе в цикле на новый dict
    :param dxfbase_path: путь до dxf BASE файла
    :param number_BOM_page: число берется 1,2,3... при работе цикле в словаре {1:{'E1':'','D1':''}}
    :return:doc_bom со вставленным инсертом таблицей
    '''
    doc_bom = create_doc_BOM(dxfbase_path=dxfbase_path,
                             number_BOM_page=number_BOM_page)
    if number_BOM_page == 1:
        border_insert = create_BOM_FIRST(doc_bom=doc_bom)
        return border_insert
    elif number_BOM_page >= 2:
        border_insert = create_BOM_FIRST(doc_bom=doc_bom)
        return border_insert

def save_BOM(doc_bom,number_page:int,save_path_shell:str = None,):
    '''
    Сохранение спецификации
    :param doc_bom: doc спецификации заполненой
    :param number_page: номер страницы для сохранения имени
    :param save_path_shell: путь для сохранения чертежа оболочек
    :return:
    '''
    if save_path_shell is not None:
        doc_bom.saveas(filename=save_path_shell + f'\\BOM_{number_page}')

'''Создание главного dict'''

def create_clear_secondleveldict_with_attribs(number_BOM_page:int):
    '''
    Создает словарь в зависимости от того, какой номер страницы спецификации пошел
    :return:{'E1':'','D1':''}
    '''
    if number_BOM_page == 1:
        for i in range(1,30):
            return_dict = {f'A{i}':'',f'B{i}':'',f'C{i}':'',f'D{i}':'',f'E{i}':'',f'F{i}':'',f'G{i}':''}
            return return_dict
    elif number_BOM_page >= 2:
        for i in range(1,33):
            return_dict = {f'A{i}':'',f'B{i}':'',f'C{i}':'',f'D{i}':'',f'E{i}':'',f'F{i}':'',f'G{i}':''}
            return return_dict

def check_row_numbers(number_row_after_write:int, number_BOM_page:int):
    '''
    Проверка на превышение номера строки относительно аттрибутов, чтобы создать новый BOM
    :param number_row_after_write: 1-32 или 1 -29
    :param number_BOM_page: 1 2 3 ...
    :return:
    '''
    if number_BOM_page == 1:
        if number_row_after_write <= 29:
            return True
        else:
            return False
    elif number_BOM_page >=2:
        if number_row_after_write <= 32:
            return True
        else:
            return False


def write_first_iteration_in_dict(dict_with_BOM_tags:dict[str:str], number_row:int,
                                  name_attrib:str, number_BOM_page:int):
    '''
    Заполняет в словаре первые строки name_attrib
    :param dict_with_BOM_tags: return_dict = {f'A{i}':'',f'B{i}':'',f'C{i}':'',f'D{i}':'',f'E{i}':'',f'F{i}':'',f'G{i}':''}
    :param number_row: 1-32 or 1-29
    :param name_attrib: 'Сборочные единицы'
    :param number_BOM_page: 1 2 3 4
    ###:param dxfbase_path: путь до базы dxfbase
    ###:param doc_bom: doc данной спецификации
    ###:param path_to_save: путь для сохранения

    :return: или number_row_after_write типа false. Проверка на isinstance
    '''
    number_row_after_write = number_row + 4
    if check_row_numbers(number_row_after_write=number_row_after_write,
                         number_BOM_page=number_BOM_page):
        dict_with_BOM_tags[f'E{number_row+1}'] = str(name_attrib)
        number_row += 4
        return number_row_after_write
    else:
        return False
        # save_BOM(doc_bom=doc_bom, number_page=number_BOM_page,save_path_shell=path_to_save)
        # number_BOM_page = number_BOM_page + 1
        # new_border_insert = create_new_BOM_dxf(dxfbase_path=dxfbase_path,
        #                                        number_BOM_page=number_BOM_page)
        # number_row += 4
        # return new_border_insert

def calculate_count_row_for_one_position(dict_second_level:dict)->int:
    '''
    Расчитать количество строк, которые понадобятся для этой позиции для заполнения в BOM
    :param dict_second_level: {'Обозначение': 'ВРПТ.301172.024-11', 'Наименование': 'Кабельный ввод ВЗ-Н25#для не бронированного#кабеля, диаметром 12-18мм',
                                            'Формат': 'А4', 'Кол.': None, 'Примечание': None}
    :return: изменяет словарь на словарь другого вида
    '''
    row = 0
    for column_name, name_in_bom in dict_second_level.items():
        if name_in_bom== None:
            name_in_bom = ''
        name_in_bom = str(name_in_bom)
        if '#' not in name_in_bom:
            row = max(1, row)
        else:
            row = max(row, len(name_in_bom.split('#')))

    for column_name, name_in_bom in dict_second_level.items():
        if name_in_bom == None:
            name_in_bom = ''
        name_in_bom = str(name_in_bom)
        if '#' not in name_in_bom:
             for i in range(0, row):
                 if i == 0:
                     dict_second_level[column_name] = [name_in_bom]
                 else:
                     dict_second_level[column_name].append('')
        else:
            row_new = name_in_bom.split('#')
            for i in range(0, row):
                if len(row_new) == row:
                    dict_second_level[column_name] = row_new
                else:
                    dict_second_level[column_name] = row_new
                    for i in range(0,row - len(row_new)):
                        dict_second_level[column_name].append('')
    return row



def write_second_iteration_in_dict(dict_with_BOM_tags:dict[str:str], number_row:int,
                                  dict_names_attribs:dict, number_BOM_page:int):
    '''
    Заполняет в словаре вторые строки проходя циклом по словарю
    :param dict_with_BOM_tags: return_dict = {f'A{i}':'',f'B{i}':'',f'C{i}':'',f'D{i}':'',f'E{i}':'',f'F{i}':'',f'G{i}':''}
    :param number_row: 1-32 or 1-29
    :param name_attrib: 'Сборочные единицы'
    :param number_BOM_page: 1 2 3 4
    :param dxfbase_path: путь до базы dxfbase
    :param doc_bom: doc данной спецификации
    :param path_to_save: путь для сохранения

    :return: или number_row_after_write типа int or INSERT. Проверка на isinstance
    '''
    tag_in_BOM_dxf = {'Формат': 'A', 'Зона': 'B', 'Поз.': 'C', 'Обозначение': 'D', 'Наименование': 'E', 'Кол.': 'F',
                      'Примечание': 'G'}
    max_row = number_row + calculate_count_row_for_one_position(dict_second_level=dict_names_attribs)
    if check_row_numbers(number_row_after_write=max_row,
                         number_BOM_page=number_BOM_page):
        for column_name in dict_names_attribs:
            for count_name_attrib, name_attrib in enumerate(dict_names_attribs[column_name]):
                dict_with_BOM_tags[tag_in_BOM_dxf[column_name] + f'{number_row + count_name_attrib}'] = name_attrib
        return number_row + max_row
    else:
        return False

def create_main_properties(dict_all_attribs:dict[str:list[dict]], name_attrib:str, row:int, tag_in_BOM_dxf:dict[str:str]):
    '''
    Заполнение словаря через главный аттрибут
    :param dict_all_attribs:dict вида {0:{'E2':"Сборочная единица"}}
    :param name_attrib:
    :param row:
    :return:
    '''

    row +=1
    if f'E{row}' not in dict_all_attribs:
        dict_all_attribs[f'E{row}'] = name_attrib
    row +=2



if __name__ == '__main__':
    start_dict = {'Сборочные единицы': [{'Обозначение': 'ВРПТ.301172.024-11',
                                         'Наименование': 'Оболочка ВП.161610',
                                         'Формат': 'А4', 'Кол.': None, 'Примечание': None},
                                        {'Обозначение': 'ВРПТ.305311.001-025',
                                         'Наименование': 'Кабельный ввод ВЗ-Н25#для не бронированного#кабеля, диаметром 12-18мм',
                                         'Формат': 'А4', 'Кол.': None, 'Примечание': None}],
                  'Стандартные изделия': [{'Обозначение': None,
                                           'Наименование': 'Винт А2.М6-6gx10.019#ГОСТ 17473-80',
                                           'Формат': 'А4', 'Кол.': None, 'Примечание': None},
                                          {'Обозначение': None,
                                           'Наименование': 'Шайба 6 019 ГОСТ 6402-70',
                                           'Формат': 'А4', 'Кол.': None, 'Примечание': None},
                                          {'Обозначение': None,
                                           'Наименование': 'Шайба A.6.019 ГОСТ 11371-78',
                                           'Формат': 'А4', 'Кол.': None, 'Примечание': None}],
                  'Детали': [{'Обозначение': 'ВРПТ.745551.005-140',
                              'Наименование': 'DIN-рейка NS35х7,5, L=140 мм',
                              'Формат': 'А4', 'Кол.': None, 'Примечание': None}]}

    '''Сначала формируем словарь, который будет относится к каждому аттрибуту в BOM_FIRST и BOM_SECOND
    Создаем сначала 1 страницы и далее будем добавлять +1 к page_bom 
    '''
    main_dict = dict()
    page_bom = 1
    number_row = 1
    dict_with_all_attribs_and_values = create_clear_secondleveldict_with_attribs(number_BOM_page=page_bom)
    for first_level_name_attrib in start_dict:
        number_row = write_first_iteration_in_dict(dict_with_BOM_tags=dict_with_all_attribs_and_values,
                                                   number_row=number_row,
                                                   name_attrib=first_level_name_attrib,
                                                   number_BOM_page=page_bom)
        if isinstance(number_row, int):#проверка, если число по выходу
            for dict_second_level in start_dict[first_level_name_attrib]:
                number_row = write_second_iteration_in_dict(dict_with_BOM_tags=dict_with_all_attribs_and_values,
                                                            number_row=number_row,
                                                            dict_names_attribs=dict_second_level,
                                                            number_BOM_page=page_bom)
                # if isinstance(number_row, int):



        else:
            main_dict[page_bom] = dict_with_all_attribs_and_values
            #надо увеличить страницу на 1
            dict_with_all_attribs_and_values = create_clear_secondleveldict_with_attribs(number_BOM_page=page_bom)
            #Создать новый номер



