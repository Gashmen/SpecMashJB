import math

import ezdxf

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

def create_shell_name(dict_name):
    '''

    :param dict_name:
    :return:
    '''
    return None



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

if __name__ == '__main__':
    doc = create_doc_BOM('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf')
    create_BOM_FIRST(doc_bom=doc)
    doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\test_BOM.dxf')
    for 