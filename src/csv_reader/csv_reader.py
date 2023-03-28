import pandas as pd
import os
main_path = os.getcwd() + '\\Общая база'
def get_main_dict(main_path:str) ->dict:

    '''
    :param main_path: main_path = os.getcwd() + '\Общая база'
    :return: {'ВЗОР':{'Exe оболочки':{Серия:{0:'ВА',1:'ВА'...}}
    '''

    main_dict = dict()
    for dirs,folder,files in os.walk(main_path):
        #Заполнение компаний,наличие папок(оборудования) и вставка csv словарем
        #ЗАПУСТИТЬ ЭТУ ФУНКЦИЮ В МОМЕНТ НАЖАТИЯ КНОПКИ КЛЕМНЫЕ КОРОБКИ ДЛЯ ПОЛУЧЕНИЯ ВСЕЙ ИНФЫ ЗАРАНЕЕ
        if files != [] and folder == []:
            for filename in files:
                if filename.endswith('.csv'):
                    if filename.partition('_')[0] not in main_dict:
                        main_dict[filename.partition('_')[0]] = \
                            {dirs.split('\\')[-1]:pd.read_csv(main_path+'\\'+dirs.split('\\')[-1]+'\\'+filename,
                                                              delimiter=';').to_dict()}
                    else:
                        main_dict[filename.partition('_')[0]][dirs.split('\\')[-1]] = \
                            pd.read_csv(main_path+'\\'+dirs.split('\\')[-1]+'\\'+filename,
                                                              delimiter=';').to_dict()
    return main_dict


'''SHELL PAGE'''
def define_list_manufacturer_for_shell(main_dict:dict)->list:
    #список для выбора производителей оболочек
    manufacturer_shell = list(set([manufacturer for manufacturer in main_dict for types_obj in list(main_dict[manufacturer].keys())
                              if 'оболочк' in types_obj.lower()]))
    manufacturer_shell.insert(0,'')
    return manufacturer_shell


def define_list_manufacturer_for_input(main_dict: dict) -> set:
    #список для выбора производителей вводов
    manufacturer_input = list(
        set([manufacturer for manufacturer in main_dict for types_obj in list(main_dict[manufacturer].keys())
             if 'вводы' in types_obj.lower()]))
    manufacturer_input.insert(0, '')
    return manufacturer_input

def define_type_of_ex(manufacturer:str, main_dict,page_type:int) -> dict:
    #Передать в ComboBox список со значениями Exd,Exe, путем перебора по оборудованию с наличием слова "оболочка"
    #и убрать строку оболочка
    if 0 == page_type and manufacturer != '':
        return main_dict[manufacturer],[type_ex for type_ex in main_dict[manufacturer] if 'оболочк' in type_ex.lower()]
    elif 0 == page_type and manufacturer == '':
        return {}, []
    # Использовать этот ретерн для дальнейшего определения словаря

def define_serial_of_shell(type_ex: str, dicts_with_type_ex: dict) -> list:
    #Определить серию оболочек по Exd,Exe
    #На выходе выдать список оболочек
    if type_ex != '' and type_ex != None:
        list_with_serial_of_type_ex = list(set([str(check_type)
                                      for check_type in dicts_with_type_ex['Серия'].values()]))

        return list_with_serial_of_type_ex
    elif type_ex == '':
        return []

def define_shell_size(type_shell:str, dicts_with_type_ex:dict) -> list:
    #Определить типоразмер оболочек
    #На выходе выдать список размеров по данной оболочке
    if type_shell != '' and type_shell != None and type_shell != 'nan':
        shell_size = [str(dicts_with_type_ex['Типоразмер'][shell_keys]) for shell_keys in dicts_with_type_ex['Серия']
                           if type_shell in dicts_with_type_ex['Серия'][shell_keys]]
        return shell_size
    elif type_shell == '':
        return []
    elif type_shell == 'nan':
        return ['nan']
def define_key_of_shell(type_shell:str,type_shell_size:str,dicts_with_type_ex:dict)-> int:
    #Определение ключа соответствия для дальнейшего заполнения
    if type_shell_size != '' and type_shell_size != None and type_shell != 'nan':
        key_with_shell = [shell_keys for shell_keys in dicts_with_type_ex['Серия'] if type_shell in dicts_with_type_ex['Серия'][shell_keys]]
        key = int([size_key for size_key in dicts_with_type_ex['Типоразмер']
                   if int(type_shell_size) == int(dicts_with_type_ex['Типоразмер'][size_key]) and size_key in key_with_shell][0])
        return key
    elif type_shell_size == '':
        return []
    elif type_shell_size == 'nan':
        return ['nan']

# print(main_dict['ВЗОР']['Exe оболочки']['Маркировка взрывозащиты'][0].split('--')[0].split(';'))
def marking_of_ex_defence(key:int,dicts_with_type_ex:dict)->dict:
    markind_dict = {'shell':[],'dust':[],'ore':[]}
    for count_marking,value_marking in enumerate(dicts_with_type_ex['Маркировка взрывозащиты'][key].split('--')):
        if count_marking == 0:
            markind_dict['shell'].insert(0, '')
            for _ in value_marking.split(';'):
                if _ !='':
                    markind_dict['shell'].append(_)
        elif count_marking == 1:
            markind_dict['dust'].append('')
            for _ in value_marking.split(';'):
                if _ != '':
                    markind_dict['dust'].append(_)
        elif count_marking == 2:
            markind_dict['ore'].append('')
            for _ in value_marking.split(';'):
                if _ != '':
                    markind_dict['ore'].append(_)
    return markind_dict

def determining_the_minimum_temperature(key:int,min_temp:str,dict_with_type_ex:dict):
    #Проверка на температуру эксплуатации минимальную
    if int(dict_with_type_ex['Температура минимальная'][key]) <= int(min_temp):
        return True
    #Если True то ничего не делаем, все хорошо
    else:
        return False
    #Если False необходимо красным подсветить температуру

def determining_the_maximum_temperature(key:int,max_temp:str,dict_with_type_ex:dict):
    #Проверка на температуру эксплуатации минимальную
    if int(dict_with_type_ex['Температура минимальная'][key]) >= int(max_temp):
        return True
    # Если True то ничего не делаем, все хорошо
    else:
        return False
    # Если False необходимо красным подсветить температуру

def define_ip(key:int, dict_with_type_ex:dict)->tuple:
    #Определение IP оболочки по ключу
    list_ip = tuple([dict_with_type_ex['IP'][key].split(';')])
    return list_ip

'''INPUTS PAGE'''
def define_input_type(manufacturer:str, dict_with_manufacturer:dict) -> list:
    # Определить серию оболочек по Exd,Exe
    # На выходе выдать список оболочек
    if manufacturer != '' and manufacturer != None:
        list_with_input_type = sorted(list(set([str(check_type) for check_type in dict_with_manufacturer['Кабельные вводы']['Серия'].values()])))
        return list_with_input_type
    elif manufacturer == '' or manufacturer == None:
        return []

def create_list_with_fullnameinputs(dict_with_manufacturer:dict) ->dict:
    list_full_name = {'':None}
    for number,check_type in enumerate(dict_with_manufacturer['Кабельные вводы']['Серия'].values()):
        if 'ВЗ-Н' == check_type or 'ВЗ-Б' == check_type or 'ВЗ-МБ' == check_type or 'ВЗ-П' == check_type or 'ВЗ-К' == check_type:
            if dict_with_manufacturer['Кабельные вводы']['Доп маркировка'][number] == '-':
                if ',' in dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number]:
                    list_full_name[check_type + str(dict_with_manufacturer['Кабельные вводы']['Резьба'][number])] =\
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number].replace(',','.'))+10
                else:
                    list_full_name[check_type + str(dict_with_manufacturer['Кабельные вводы']['Резьба'][number])] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number])+10
            elif dict_with_manufacturer['Кабельные вводы']['Доп маркировка'][number] == 'Р':
                if ',' in dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number]:
                    list_full_name[f'{check_type}{str(dict_with_manufacturer["Кабельные вводы"]["Резьба"][number])}/{dict_with_manufacturer["Кабельные вводы"]["Доп маркировка"][number]}'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number].replace(',', '.'))+10
                else:
                    list_full_name[f'{check_type}{str(dict_with_manufacturer["Кабельные вводы"]["Резьба"][number])}/{dict_with_manufacturer["Кабельные вводы"]["Доп маркировка"][number]}'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number])+10
            else:
                if ',' in dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number]:
                    list_full_name[f'{check_type}{str(dict_with_manufacturer["Кабельные вводы"]["Резьба"][number])}{dict_with_manufacturer["Кабельные вводы"]["Доп маркировка"][number]}'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number].replace(',', '.'))+10
                else:
                    list_full_name[f'{check_type}{str(dict_with_manufacturer["Кабельные вводы"]["Резьба"][number])}{dict_with_manufacturer["Кабельные вводы"]["Доп маркировка"][number]}'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number])+10
        if 'ВЗ-Н-МР' == check_type:
            if ',' in dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number]:
                list_full_name[check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[0] +
                               check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[1]] = \
                    float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number].replace(',', '.'))+10
            else:
                list_full_name[
                    check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[0] +
                    check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[1]] = \
                    float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number])+10

        if 'ВЗ-Н-Т' == check_type:
            if ' ' not in dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[1]:
                if ',' in dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number]:
                    list_full_name[
                        check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[0]
                        + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[1]+'G(B)'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number].replace(',', '.'))+10
                else:
                    list_full_name[
                        check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[0]
                        + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[1]+'G(B)'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number])+10
            else:
                if ',' in dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number]:
                    list_full_name[
                        check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[0]
                        + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[1].replace(' ','.') + 'G(B)'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number].replace(',', '.'))+10
                else:
                    list_full_name[
                        check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[0]
                        + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][number].split(';')[
                            1].replace(' ', '.') + 'G(B)'] = \
                        float(dict_with_manufacturer['Кабельные вводы']['Размер под ключ D'][number])+10
    return list_full_name

def give_full_name_and_dict_for_input(dict_with_manufacturer:dict, key_input:int) -> str :
    list_full_name =[]
    check_type = dict_with_manufacturer['Кабельные вводы']['Серия'][key_input]
    if 'ВЗ-Н' == check_type or 'ВЗ-Б' == check_type or 'ВЗ-МБ' == check_type or 'ВЗ-П' == check_type or 'ВЗ-К' == check_type:
        if dict_with_manufacturer['Кабельные вводы']['Доп маркировка'][key_input] == '-':
            list_full_name.append(check_type + str(dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input]))
        elif dict_with_manufacturer['Кабельные вводы']['Доп маркировка'][key_input] == 'Р':
            list_full_name.append(f'{check_type}{str(dict_with_manufacturer["Кабельные вводы"]["Резьба"][key_input])}/'
                                  f'{dict_with_manufacturer["Кабельные вводы"]["Доп маркировка"][key_input]}')
        else:
            list_full_name.append(
                f'{check_type}{str(dict_with_manufacturer["Кабельные вводы"]["Резьба"][key_input])}'
                f'{dict_with_manufacturer["Кабельные вводы"]["Доп маркировка"][key_input]}')
    if 'ВЗ-Н-МР' == check_type:
        list_full_name.append(check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[0]
                                                    + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[1])
    if 'ВЗ-Н-Т' == check_type:
        if ' ' not in dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[1]:
            list_full_name.append(
                check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[0]
                + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[1]+'G(B)')
        else:
            list_full_name.append(
                check_type[:-3] + dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[0]
                + check_type[-3:] + dict_with_manufacturer['Кабельные вводы']['Резьба'][key_input].split(';')[1].replace(' ','.') + 'G(B)')
    return list_full_name[0]

