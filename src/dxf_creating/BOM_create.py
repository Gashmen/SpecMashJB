import math

import ezdxf
import openpyxl
from openpyxl.utils import get_column_letter


def create_doc_BOM(dxfbase_path:str):
    '''Создает BOM удаляя все не нужное'''
    doc_bom = ezdxf.readfile(dxfbase_path)

    doc_dxfbase_for_del = ezdxf.readfile(dxfbase_path)

    doc_bom.modelspace().delete_all_entities()

    blocks_BOM = ['BOM_FIRST','BOM_SECOND']


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

def check_name_len(name_string:str):
    if name_string != None:
        if math.ceil(len(name_string)/27) ==1:
            return True
        else:
            return False

def read_BOM_base(xlsx_base_path:str):
    '''
    Чтение базавой эксельки BOM и выдача словаря
    :param xlsx_base_path:
    :return:
    '''

    return_dict = dict()

    workbook = openpyxl.load_workbook(xlsx_base_path)
    worksheet = workbook.active

    column_names = list(worksheet[1])

    for column_name in column_names:
        return_dict[column_name.value] = {}
        for count,row_value in enumerate(worksheet[get_column_letter(column_name.column)][column_name.row:]):
            return_dict[column_name.value][count] = row_value.value

    return return_dict

def write_attrib(BOM_insert,dict_for_writing_attrib):
    '''
    Заполение аттрибутов в спецификации
    :param BOM_insert: BOM_FIRST или BOM_SECOND
    :param dict_for_writing_attrib:
    {'Сборочные единицы':{0:{"Формат":"А4","Зона":"","Поз.":0+1,"Обозначение":"ВРПТ.301172.024-11","Наименование":"Оболочка ВП.161610", "Кол.":1, "Примечание": производитель}}
    :return:
    '''

    row_start = 2
    dict_name_attrib = {attrib.dxf.tag: attrib for attrib in BOM_insert.attribs}
    for main_type_name in dict_for_writing_attrib:
        # [Сборочные изделия, Детали, Стандартные изделия ...]
        dict_name_attrib[f'E{row_start}'].dxf.text = main_type_name
        row_start+=2

        dict_with_pozition = dict_for_writing_attrib[main_type_name]

        for number_pozition in dict_with_pozition:
            dict_name_attrib[f'A{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Формат']
            dict_name_attrib[f'B{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Зона']
            dict_name_attrib[f'C{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Поз.']
            dict_name_attrib[f'D{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Обозначение']
            dict_name_attrib[f'F{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Кол.']
            dict_name_attrib[f'G{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Примечание']

            if math.ceil(len(dict_with_pozition[number_pozition]['Наименование']) / 27) == 1:
                dict_name_attrib[f'E{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Наименование']
            elif math.ceil(len(dict_with_pozition[number_pozition]['Наименование']) / 27) == 2:
                dict_name_attrib[f'E{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Наименование'][:27]
                row_start+=1
                dict_name_attrib[f'E{row_start}'].dxf.text = dict_with_pozition[number_pozition]['Наименование'][27:]

    row_start+=1

def add_dict(dict_with_tags:dict, count_row:int):
    '''
    Нужно добавить в этот же словарь тэг того, сколько страниц добавить в конце после прохода по данному словорю а также найти, сколько нужно добавить
    :param dict_with_tags:{'Обозначение': 'ВРПТ.305311.001-025', 'Наименование': 'Кабельный ввод ВЗ-Н25#для не бронированного#кабеля, диаметром 12-18мм', 'Свойство': 'Сборочные единицы', 'Формат': 'А4', 'Кол.': None, 'Примечание': None}
    :param count_row:1
    :return:
    '''
    row = 0
    for column_name, name_in_bom in dict_with_tags.items():
        if '#' not in name_in_bom:
            row = max(1, row)
        else:
            row = max(row, len(name_in_bom.split('#')))

    for column_name, name_in_bom in dict_with_tags.items():
        if '#' not in name_in_bom:
             for i in range(0, row):
                 if i == 0:
                     dict_with_tags[column_name] = [name_in_bom]
                 else:
                     dict_with_tags[column_name].append('')
        else:
            row_new = name_in_bom.split('#')
            for i in range(0, row):
                if len(row_new) == row:
                    dict_with_tags[column_name] = row_new
                else:






if __name__ == '__main__':

    # create_BOM_FIRST(doc_bom=doc)
    # doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\test_BOM.dxf')
    list_for_creating_BOM = list()
    data_base_bom = read_BOM_base(xlsx_base_path='C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\naming_base.xlsx')
    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx.dxf')

    tag_in_BOM_dxf = {'Формат':'A', 'Зона':'B', 'Поз.':'C', 'Обозначение':'D', 'Наименование':'E', 'Кол.': 'F', 'Примечание':'G'}

    list_with_block_names = [block.dxf.name for block in doc.blocks if '*' not in block.dxf.name]
    for block_name in list_with_block_names:
        for count_block, name_block_base in data_base_bom['Блок'].items():
            if name_block_base == block_name:
                _dict = {}
                for _ in data_base_bom:
                    if _ != 'Блок':
                        _dict[_]= data_base_bom[_][count_block]
                list_for_creating_BOM.append(_dict)

    doc_bom = create_doc_BOM(dxfbase_path='C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\src\dxf_base\\DXF_BASE.dxf')

    main_border = create_BOM_FIRST(doc_bom=doc_bom)

    end_row_in_bom = 1
    for equip in list_for_creating_BOM:
        start_row_in_bom = end_row_in_bom

        for namename in equip:
            print(equip)
            for attrib in main_border.attribs:
                try:
                    if tag_in_BOM_dxf[namename] + str(start_row_in_bom) == attrib.dxf.tag:
                        if '#' in equip[namename]:
                            for i in equip[namename].split('#'):
                                attrib.dxf.text = i
                                start_row_in_bom+=1
                        attrib.dxf.text = equip[namename]
                        print(attrib.dxf.tag)
                except:
                    continue

        # end_row_in_bom =


        # for namename in equip:
        #     print(namename)
