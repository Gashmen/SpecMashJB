import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from transliterate import translit


import start_ui as designer_ui
import src.csv_reader.csv_reader as csv_reader
from src.dxf_creating import shell_create,main_shell_create

class ShellPageSetup(designer_ui.Mainver):

    def __init__(self,save_path = None, path_to_csv = None, path_to_dxf = None, path_to_terminal_dxf = None):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__(save_path=save_path,
                         path_to_csv=path_to_csv,
                         path_to_terminal_dxf=path_to_terminal_dxf)

        #path_to_dxf задаем None заранее
        self.path_to_dxf = path_to_dxf

        #создание self.path_to_dxf
        self.check_path_to_dxf()

        #Определение переменной ключа
        self.shell_key = None
        self.shell_name = None

        #Создание словаря наименования
        self.dict_full_name_shell_page = {'Tag': None, 'Маркировка взрывозащиты': None}
        #Создание словаря с полными размерами
        self.full_size_shell = {'Внутренние размеры AB': None,
                                'Внутренние размеры БГ': None,
                                "Внутренняя высота коробки": None}

        '''ФУНКЦИИ ЗАПОЛНЕНИЯ COMBOBOX WIDGETS'''

        # получение типа взрывозащиты оболочек по производителю
        self.manufactureComboboxWidget_shellpage.currentTextChanged.connect(self.give_ex_type_and_dict_with_this_ex)

        # получение cерии оболочек, относительно типа взрывозащиты
        self.safefactortypeCombobox_shellpage.currentTextChanged.connect(self.give_serial_type)

        # получение размеров оболочек
        self.serialCombobox_shellpage.currentTextChanged.connect(self.give_size)
        self.serialCombobox_shellpage.currentTextChanged.connect(self.write_serialtype_in_general_dict_with_all_info)

        # Получение маркировки начальной по взрывозащите, без Т класса
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.set_ex_marking)
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.write_size_in_general_dict_with_all_info)

        self.gas_mark_RadioButton_shellpage.toggled.connect(self.set_ex_marking)
        self.dust_mark_RadioButton_shellpage.toggled.connect(self.set_ex_marking)
        self.ore_mark_RadioButton_shellpage.toggled.connect(self.set_ex_marking)

        #Получение полного Tag оболочки
        self.temperature_class_comboBox_shellpage.currentTextChanged.connect(self.write_t_class_in_general_dict)
        self.maxtempLineedit_shellpage.editingFinished.connect(self.write_t_class_in_general_dict)
        self.mintempLineEdit_shellpage.editingFinished.connect(self.write_t_class_in_general_dict)

        # Добавление температурного класса
        self.gas_mark_RadioButton_shellpage.toggled.connect(self.give_T_class_and_maxT)
        self.dust_mark_RadioButton_shellpage.toggled.connect(self.give_T_class_and_maxT)
        self.ore_mark_RadioButton_shellpage.toggled.connect(self.give_T_class_and_maxT)
        self.maxtempLineedit_shellpage.editingFinished.connect(self.give_T_class_and_maxT)


        '''ФУНКЦИИ ПОЛУЧЕНИЯ НОВЫХ ВАЖНЫХ ПЕРЕМЕННЫХ'''
        #ПОЛУЧЕНИЯ КЛЮЧА ПО КОТОРОМУ УЖЕ ВСЕ ПОНЯТНО И МОЖНО СТРОИТЬ
        self.sizeCombobox_shellpage.currentTextChanged.connect(self.give_key)


        '''СОХРАНЕНИЕ DXF'''


    def check_path_to_dxf(self):
        '''Проверяет, указан ли путь до Контейнера оболочек
        Если нет, то должен открыть filedialog для выбора файла'''

        if self.path_to_dxf is None:
            filename,_ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                 caption='Выбрать файл Контейнера dxf',
                                                 directory= '\\'.join(os.getcwd().split('\\')[0:-1]),
                                                 filter="DXF files (*.dxf)")
            self.path_to_dxf = filename


    def add_manufacturer_items_combobox(self):
        '''Добавляет производителей при появление csv файла'''
        if self.main_dict is not {}:
            self.manufactureComboboxWidget_shellpage.clear()
            list_manufacturer_for_shell = csv_reader.define_list_manufacturer_for_shell(main_dict=self.main_dict)
            self.manufactureComboboxWidget_shellpage.addItems(list_manufacturer_for_shell)
        else:
            self.error_window.add_error('Не создан main_dict в ShellPage')

    def give_ex_type_and_dict_with_this_ex(self):
        '''Добавляет в Вид взрывозащиты Combobox имеющиеся типы
        self.type_of_ex_dict : {'Exe оболочки': {'Серия': {0: 'ВА', 1: 'ВА', 2: 'ВА'....
        self.list_with_ex_for_combobox : ['Exd оболочки', 'Exe оболочки']
        '''
        self.safefactortypeCombobox_shellpage.clear()
        if self.manufactureComboboxWidget_shellpage.currentText() != '' and \
            self.manufactureComboboxWidget_shellpage.currentText() != None:
            self.type_of_ex_dict, self.list_with_ex_for_combobox = csv_reader.define_type_of_ex(
                manufacturer=self.manufactureComboboxWidget_shellpage.currentText(),
                main_dict=self.main_dict,
                page_type=self.stackedWidget.currentIndex())
            self.list_with_ex_for_combobox.insert(0, '')
            if self.list_with_ex_for_combobox:
                self.safefactortypeCombobox_shellpage.addItems(self.list_with_ex_for_combobox)
        else:
            self.error_window.add_error('self.manufactureComboboxWidget_shellpage является None или ''')

    def give_serial_type(self):
        '''
        Добавляет виды оболочек
        '''
        self.serialCombobox_shellpage.clear()
        if self.safefactortypeCombobox_shellpage.currentText() is not None and \
           self.safefactortypeCombobox_shellpage.currentText() != '':
                self.serial_ex_type = csv_reader.define_serial_of_shell(
                    type_ex=self.safefactortypeCombobox_shellpage.currentText(),
                    dicts_with_type_ex =self.main_dict[self.manufactureComboboxWidget_shellpage.currentText()][
                                                            self.safefactortypeCombobox_shellpage.currentText()])
                self.serial_ex_type.insert(0, '')
                self.serial_ex_type.sort()
                self.serialCombobox_shellpage.addItems(self.serial_ex_type)
        else:
            self.error_window.add_error('self.safefactortypeCombobox_shellpage является None или ''')


    def write_serialtype_in_general_dict_with_all_info(self):
        ''' Заполнение dict после изменения Серии в ComboBox виджете '''
        if (self.serialCombobox_shellpage.count() != 0 and self.serialCombobox_shellpage.currentText() != ''):
            self.dict_full_name_shell_page['Tag'] = f'К{self.serialCombobox_shellpage.currentText()}'

    def give_size(self):
        """
        Выдает размеры оболочек только те, которые есть в dxf базе
        update : Не выдает!
        :return:
        """
        self.sizeCombobox_shellpage.clear()
        if self.serialCombobox_shellpage.currentText() is not None and\
           self.serialCombobox_shellpage.currentText() != '':
                self.shell_size = csv_reader.define_shell_size(
                    type_shell=self.serialCombobox_shellpage.currentText(),
                    dicts_with_type_ex=self.main_dict[self.manufactureComboboxWidget_shellpage.currentText()][self.safefactortypeCombobox_shellpage.currentText()])
                # self.shell_size = list(set(self.shell_size) &
                #                        set(dxf_creator.return_shells_and_inputs_in_dxf(self.path_to_dxf)['Shell'][translit(self.serialCombobox_shellpage.currentText(),
                #                                                                                                            language_code='ru',
                #                                                                                                             reversed=True)]))
                self.shell_size.insert(0, '')
                self.shell_size.sort()
                self.sizeCombobox_shellpage.addItems(self.shell_size)

    def write_size_in_general_dict_with_all_info(self):
        ''' Заполнение dict после изменения Серии в ComboBox виджете '''
        if (self.sizeCombobox_shellpage.count() != 0 and self.sizeCombobox_shellpage.currentText() != ''):
            self.dict_full_name_shell_page['Tag'] = \
                f'К{self.serialCombobox_shellpage.currentText()}.{self.sizeCombobox_shellpage.currentText()}'
            print(self.dict_full_name_shell_page['Tag'])
        else:
            self.error_window.add_error('self.sizeCombobox_shellpage является None или ''')

    '''ПОСЛЕ ПОЛУЧЕНИЯ КЛЮЧА МОЖНО НАЧАТЬ СТРОИТЬ ОБОЛОЧКУ И СОБИРАТЬ ДЛЯ НЕЕ ДАННЫЕ'''
    def give_key(self):
        '''Получение ключа строки в csv файле оболочек
        После этого можно строить и получать данные
        '''
        if self.sizeCombobox_shellpage.currentText() is not None and\
           self.sizeCombobox_shellpage.currentText() != '':
                self.shell_key = csv_reader.define_key_of_shell(
                    type_shell = self.serialCombobox_shellpage.currentText(),
                    type_shell_size = self.sizeCombobox_shellpage.currentText(),
                    dicts_with_type_ex = self.main_dict[self.manufactureComboboxWidget_shellpage.currentText()]
                                                                [self.safefactortypeCombobox_shellpage.currentText()])
        else:
            self.shell_key = None
            self.error_window.add_error('give key не создан')

        self.create_shell_name_for_dxf_creating()
        self.get_full_sizes_shell()
        self.define_blocks_name_shell_before_draw()



    def set_ex_marking(self):
        '''
        :return:
        '''
        self.gasdustoreComboBox_shellpage.clear()
        if self.shell_key != None:
            if self.shell_key != [] and self.shell_key != ['nan']:
                self.dict_with_ex_marking = csv_reader.marking_of_ex_defence(
                    key=self.shell_key,
                    dicts_with_type_ex = self.main_dict[self.manufactureComboboxWidget_shellpage.currentText()][
                                                        self.safefactortypeCombobox_shellpage.currentText()])
                if self.gas_mark_RadioButton_shellpage.isChecked():
                    for _ in self.dict_with_ex_marking['shell']:
                        self.gasdustoreComboBox_shellpage.addItem(_)
                elif self.dust_mark_RadioButton_shellpage.isChecked():
                    for _ in self.dict_with_ex_marking['dust']:
                        self.gasdustoreComboBox_shellpage.addItem(_)
                elif self.ore_mark_RadioButton_shellpage.isChecked():
                    for _ in self.dict_with_ex_marking['ore']:
                        self.gasdustoreComboBox_shellpage.addItem(_)
        else:
            self.error_window.add_error('give key не создан')

    def give_T_class_and_maxT(self):
        '''Определяет Т класс в зависимости от указанного температурного диапазона'''
        self.temperature_class_comboBox_shellpage.clear()
        T_class = ['', 'T3', 'T4', 'T5', 'T6']

        def define_deleted_Tclass(max_T: int) -> list:
            if max_T <= 40:
                return ['', 'T3', 'T4', 'T5', 'T6']
            elif max_T <= 55 and max_T > 40:
                return ['', 'T3', 'T4', 'T5']
            elif max_T <= 100 and max_T > 55:
                return ['', 'T3', 'T4']
            elif max_T <= 130 and max_T > 100:
                return ['', 'T3']
            else:
                return ['Не проходит по Т классу']

        if self.gas_mark_RadioButton_shellpage.isChecked():
            self.t_class_widget_shellpage.setEnabled(True)
            self.using_temperatureWidget_shellpage.setEnabled(True)
            self.mintempLabel_shellpage.setEnabled(True)
            self.mintempLineEdit_shellpage.setEnabled(True)
            self.maxtempLabel_shellpage.setEnabled(True)
            self.maxtempLineedit_shellpage.setEnabled(True)
            self.t_class_widget_shellpage.setEnabled(True)
            self.using_temperatureLabel_shellpage.setText('Температура окружающей среды')
            self.temperature_class_comboBox_shellpage.addItems(
                define_deleted_Tclass(int(self.maxtempLineedit_shellpage.text())))
        elif self.dust_mark_RadioButton_shellpage.isChecked():
            self.using_temperatureWidget_shellpage.setEnabled(True)
            self.mintempLabel_shellpage.setEnabled(False)
            self.mintempLineEdit_shellpage.setEnabled(False)
            self.t_class_widget_shellpage.setEnabled(False)
            self.maxtempLabel_shellpage.setEnabled(True)
            self.maxtempLineedit_shellpage.setEnabled(True)
            self.using_temperatureLabel_shellpage.setText('Максимальная температура поверхности')
        elif self.ore_mark_RadioButton_shellpage.isChecked():
            self.t_class_widget_shellpage.setEnabled(False)
            self.using_temperatureWidget_shellpage.setEnabled(False)
            self.using_temperatureLabel_shellpage.setText(' ')

    def write_t_class_in_general_dict(self):
        '''Записываем в словарь данные по Т классу оболочки( в ее наименование 'Tag')'''
        if (self.maxtempLineedit_shellpage.isEnabled() and self.mintempLineEdit_shellpage.isEnabled()) and \
           (self.serialCombobox_shellpage.count() != 0 and self.serialCombobox_shellpage.currentText() != ''):
                if self.maxtempLineedit_shellpage.isEnabled() and self.mintempLineEdit_shellpage.isEnabled():
                    self.dict_full_name_shell_page['Tag'] = \
                        f'К{self.serialCombobox_shellpage.currentText()}.{self.sizeCombobox_shellpage.currentText()}'+\
                        f'({self.mintempLineEdit_shellpage.text()}...+{self.maxtempLineedit_shellpage.text()})'



    def create_shell_name_for_dxf_creating(self):
        '''Создание имени для построения после заполнения self.shell_key'''
        if self.shell_key != None:
            if self.shell_key != [] and self.shell_key != ['nan']:
                shell_name = translit(value = self.serialCombobox_shellpage.currentText(),
                                      language_code='ru',
                                      reversed=True) +\
                    '.' + \
                    self.sizeCombobox_shellpage.currentText()
                self.shell_name = shell_name

    def define_blocks_name_shell_before_draw(self):
        '''Добавление в словарь self.list_for_save_blocks_before_draw информации '''
        if self.shell_key != None:
            self.dict_for_save_blocks_before_draw['shell'] = \
                shell_create.get_list_for_draw_shell(shell_name=self.shell_name)

    def get_full_sizes_shell(self):
        '''Составление полного именни оболочки как например КВП.161610(-60...+60)'''
        if self.shell_key != None:
            maindict_manufacturer_extype = self.main_dict[
                                              self.manufactureComboboxWidget_shellpage.currentText()][
                                                   self.safefactortypeCombobox_shellpage.currentText()]
            for type_size in self.full_size_shell.keys():
                self.full_size_shell[type_size] = maindict_manufacturer_extype[type_size][self.shell_key]


if __name__ == "__main__":
    path_to_csv = os.getcwd() + '\Общая база'
    path_to_dxf = '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\Оболочка\\ContainerVer02.dxf'
    # path_to_dxf = None
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = ShellPageSetup(path_to_csv=path_to_csv,
                                    path_to_dxf = path_to_dxf)
    welcome_window.show()
    sys.exit(app.exec_())