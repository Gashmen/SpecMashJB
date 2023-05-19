from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import re
import ezdxf
'''

Формирование спецификации должно происходить таким образом:
Нужно понимать основные и запасные части

Поэтому главные ключи общего словаря будут начинаться с "Основная часть" и "Комплект запасных частей"
{"Основная часть":main_dict, "Комплект запасных частей":reserve_dict}

Сначала строим основную часть, далее с нового листа строим ЗИП
main_dict будет представлять из себя перечисление элементов, которые есть на чертеже
каждый элемент относится к своему типу ключа в номенклатуре.
Ключи словаря будут представлять из себя :[Сборочные единицы,Детали,Стандартные изделия,Прочие изделия,Комплекты ] 

Значения для каждого ключа будут представлять из себя наименования по столбикам каждой позиции:
0:{"Формат":"А4","Зона":"","Поз.":0+1,"Обозначение":"ВРПТ.301172.024-11","Наименование":"Оболочка ВП.161610", "Кол.":1, "Примечание": производитель}
1:{"Формат":"А4","Зона":"","Поз.":0+1,"Обозначение":"ВРПТ.301172.024-11","Наименование":"Оболочка ВП.161610", "Кол.":1, "Примечание": производитель}

и тд. 
Ключи 0 1 и тд должны продолжаться по всем ключам словаря, т.е. ключ на сборочных единицах заканчивается на цифре 4, 
в деталях нужно будет начать с 5

Далее нужно написать в каждый столбец строку
Каждый раз нужно возвращать сколько строк заняло это действие
Далее получить максимальное кол-во строк по этой позиции, чтобы начать следующую позицию с max_row + 1

'''



example_dict = {"Основная часть":{'Сборочные единицы':{1:{"Формат":"А4","Зона":"","Поз.":1,"Обозначение":"ВРПТ.301172.024-11",
                                                         "Наименование":"Оболочка ВП.161610", "Кол.":1, "Примечание": "ВЗОР"},
                                                       2:{"Формат":"А4","Зона":"","Поз.":2,"Обозначение":"ВРПТ.305311.004-08",
                                                         "Наименование":"Кабельный ввод ВЗ-Н20-МР20 для не бронированного кабеля,диаметром 6-14мм,с креплением металлорукова ДУ 20",
                                                         "Кол.":1, "Примечание": "ВЗОР"}}},
                                  'Детали': {3:{"Формат":"А3","Зона":"","Поз.":3,"Обозначение":"ВРПТ.711111.003-020",
                                                         "Наименование":"Оболочка ВП.161610", "Кол.":1, "Примечание": "ВЗОР"}},

                "Комплект запасных частей":{}}

def get_split_name_bom(name:str):
    '''
    Получаем отспличенный name с логикой сначала делим по пробелам, потом чекаем, есть ли в слове запятая и разделяем по ней
    :param name:"Кабельный ввод ВЗ-Н20-МР20 для не бронированного кабеля,диаметром 6-14мм,с креплением металлорукова ДУ 20"
    :return: list
    '''
    name = str(name)
    if name != '':
        split_with_space = name.split(' ')
        for word in split_with_space.copy():
            if ',' in word:
                before_comma = word.split(',')[0] + ','
                after_comma = word.split(',')[1]
                index_word = split_with_space.index(word)
                split_with_space.pop(split_with_space.index(word))
                split_with_space.insert(index_word,before_comma)
                split_with_space.insert(index_word+1,after_comma)
        return split_with_space
    elif ' ' not in name:
        return [name]
    else:
        return [' ']

def create_split_dict(split_list:list = None, len_word:int = 0,row_number:int = 0):
    '''
    Получение
    :param split_list: ['Кабельный', 'ввод', 'ВЗ-Н20-МР20', 'для', 'не', 'бронированного', 'кабеля,',
                        'диаметром', '6-14мм,', 'с', 'креплением', 'металлорукова', 'ДУ', '20']
    :param len_word: 27
    :return:
    '''
    row_dict = {}
    for word in split_list:
        if row_number not in row_dict:
            row_dict[row_number] = []
        len_word -= len(word)
        if len_word >= 0:
            row_dict[row_number].append(word)
            if ',' not in word:
                len_word -= 1
        else:
            len_word = 27
            row_number += 1
            row_dict[row_number] = []
            len_word -= len(word)
            if len_word > 0:
                row_dict[row_number].append(word)
                len_word -= 1
    return row_dict

def create_join_str(split_list:list):
    ''' Объединение строк
    :param split_list: ['кабеля,', 'диаметром', '6-14мм,', 'с']
    '''
    result_string = ''

    if len(split_list) == 1:
        return split_list[0]
    elif len(split_list) == 0:
        raise ValueError('В списке нет элементов')
    else:
        for word in split_list:
            if word == split_list[-1]:
                result_string+=word
            else:
                if ',' in word:
                    result_string+=word
                else:
                    result_string+=f'{word} '
        return result_string


if __name__ == '__main__':

    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf')
    msp = doc.modelspace()

    bom_insert = msp.query('INSERT[name =="BOM_FIRST"]')[0]
    dict_name_attrib = {attrib.dxf.tag: attrib for attrib in bom_insert.attribs}
    print(dict_name_attrib)

    column_names_dict = {'Формат': "A", "Зона":"B","Поз.":"C","Обозначение":"D","Наименование":"E","Кол.":"F", "Примечание":'G'}

    column_len_dict = {'Формат': 2, "Зона":2,"Поз.":3,"Обозначение":30,"Наименование":30,"Кол.":4, "Примечание":9}

    example_dict = {"Основная часть": {
                        'Сборочные единицы': {1: {"Формат": "А4", "Зона": "", "Поз.": 1, "Обозначение": "ВРПТ.301172.024-11",
                                                    "Наименование": "Оболочка ВП.161610", "Кол.": 1, "Примечание": "ВЗОР"},
                                              2: {"Формат": "А4", "Зона": "", "Поз.": 2, "Обозначение": "ВРПТ.305311.004-08",
                                                    "Наименование": "Кабельный ввод ВЗ-Н20 для не бронированного кабеля,диаметром 6-14мм,с креплением металлорукова ДУ 20",
                                                    "Кол.": 1, "Примечание": "ВЗОР"}},
                        'Детали':            {3: {"Формат": "А3", "Зона": "", "Поз.": 3, "Обозначение": "ВРПТ.711111.003-020",
                                                    "Наименование": "Оболочка ВП.261610", "Кол.": 1, "Примечание": "ВЗОР"}}},

                    "Комплект запасных частей": {}}

    check_name = "Кабельный ввод ВЗ-Н20-МР20 для не бронированного кабеля,диаметром 6-14мм,с креплением металлорукова ДУ 20"

    for type_of_equipment in example_dict:
        if type_of_equipment == 'Основная часть':
            if example_dict[type_of_equipment] != {}:
                row_number = 2
                # Основная часть не пишется
                main_dict = example_dict[type_of_equipment]
                for circuit_of_equipment in main_dict:
                    # Записываем Circiut of equipment к примеру 'Сборочные единицы'
                    try:
                        dict_name_attrib[f'E{row_number}'].dxf.text = circuit_of_equipment
                    except:
                        continue
                    print(circuit_of_equipment)
                    row_number += 2

                    for count_element, writing_dict in main_dict[circuit_of_equipment].items():
                        #count_element = 1
                        #writing_dict = {'Формат': 'А4', 'Зона': '', 'Поз.': 1, 'Обозначение': 'ВРПТ.301172.024-11',
                        #                'Наименование': 'Оболочка ВП.161610', 'Кол.': 1, 'Примечание': 'ВЗОР'}
                        max_row = 0
                        for type_of_column in writing_dict:
                            split_name = get_split_name_bom(name = writing_dict[type_of_column])
                            row_dict = create_split_dict(split_list=split_name,
                                                         len_word=column_len_dict[type_of_column],
                                                         row_number=row_number
                                                         )
                            max_row = max(max_row, max(list(row_dict.keys()))-row_number+1)
                            for current_row, current_word in row_dict.items():
                                join_str = create_join_str(split_list=current_word)
                                try:
                                    dict_name_attrib[f'{column_names_dict[type_of_column]}{current_row}'].dxf.text = join_str
                                except:
                                    continue
                        row_number+=max_row
                    row_number += 1



                            # print(row_dict)
                            # print(max_row)

                    # далее записывается каждый столбец по очереди


        else:
            row_number = 1
            # Пишется комплект запасных частей на 1 строке


    doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\test.dxf')

    # check_name = get_split_name_bom(check_name)
    # len_word = 27
    # row_dict = create_split_dict(split_list=check_name, len_word= len_word)
    #
    # for i in row_dict.values():
    #     sum = 0
    #     for j in i:
    #         if j != i[-1]:
    #             sum += 1 + len(j)
    #         else:
    #             sum += len(j)
    #     print(i)
    #     print(sum)








