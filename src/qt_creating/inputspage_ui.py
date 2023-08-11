import os
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from transliterate import translit


import shellpage_ui
import start_ui as designer_ui
import src.algoritms.new as new
import src.csv_reader.csv_reader as csv_reader
import src.dxf_creating.inputs_create as inputs_create
import src.examples.create_inputs as input_create_examples
import src.examples.create_inputs_check as input_create_expamles_check
class InputsPageSetup(shellpage_ui.ShellPageSetup,designer_ui.Mainver):

    def __init__(self,save_path = None, path_to_csv = None, path_to_dxf = None,path_to_terminal_dxf = None):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__(save_path=save_path,
                         path_to_csv=path_to_csv,
                         path_to_dxf=path_to_dxf,
                         path_to_terminal_dxf = path_to_terminal_dxf)

        self.dict_with_inputs_on_side = {"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}
        self.dict_with_list_coordinates_on_side_for_dxf = {'А': {}, 'Б': {}, "В": {}, "Г": {}, "Крышка": {}}
        '''Заполнение Combobox'''
        #Заполнение типа ввода
        self.manufacturerInputsComboBox.currentTextChanged.connect(self.get_type_of_inputs)
        #Оставляем только те виджеты,которые необходимы для выбора данного типа ввода
        self.inputtypeComboBox.currentTextChanged.connect(self.take_widgets_for_cable_size)
        # Заполнение панели комбобокса ручного ввода, после появления производителя
        self.manufacturerInputsComboBox.currentTextChanged.connect(self.make_manualinput)
        #Заполнение поворота типов поворота коробки
        self.manufacturerInputsComboBox.currentTextChanged.connect(self.add_box_locations_type)
        '''Заполнение кабельнных вводов'''
        #Создание словаря после определения размера ввода : {4:[14,27,6]}
        self.addButton.clicked.connect(self.search_size_for_input)
        # определение имени
        self.addButton.clicked.connect(self.create_current_input_name)
        # Добавление имен в siteA
        self.addButton.clicked.connect(self.add_inputsA_to_list_widget)
        # Добавление имен в siteB
        self.addButton.clicked.connect(self.add_inputsB_to_list_widget)
        # Добавление имен в siteV
        self.addButton.clicked.connect(self.add_inputsV_to_list_widget)
        # Добавление имен в siteG
        self.addButton.clicked.connect(self.add_inputsG_to_list_widget)
        '''Работа с перемещением и удалением в ABVG'''
        # Обнуление SpinBox
        self.addButton.clicked.connect(self.clear_ABVG_spinbox_afted_add_button)

        # Удалить все
        self.deleteallButton.clicked.connect(self.clear_all_list_widget)

        # Кнопка Up
        self.sideAupButton.clicked.connect(self.click_up_button_A)
        self.sideBupButton.clicked.connect(self.click_up_button_B)
        self.sideVupButton.clicked.connect(self.click_up_button_V)
        self.sideGupButton.clicked.connect(self.click_up_button_G)
        self.ComponentupButton.clicked.connect(self.click_up_button_components)

        # Кнопка Down
        self.sideAdownButton.clicked.connect(self.click_down_button_A)
        self.sideBdownButton.clicked.connect(self.click_down_button_B)
        self.sideVdownButton.clicked.connect(self.click_down_button_V)
        self.sideGdownButton.clicked.connect(self.click_down_button_G)
        self.ComponentdownButton.clicked.connect(self.click_down_button_components)

        # Кнопка delete
        self.sideAdeleteButton.clicked.connect(self.click_delete_button_A)
        self.sideBdeleteButton.clicked.connect(self.click_delete_button_B)
        self.sideVdeleteButton.clicked.connect(self.click_delete_button_V)
        self.sideGdeleteButton.clicked.connect(self.click_delete_button_G)
        self.ComponentdeleteButton.clicked.connect(self.click_delete_button_components)

        #Получение информации


        self.sideAListWidget.model().rowsInserted.connect(self.add_input_from_A_listwidget_to_dict)
        self.sideAListWidget.model().rowsRemoved.connect(self.add_input_from_A_listwidget_to_dict)

        self.sideBListWidget.model().rowsInserted.connect(self.add_input_from_B_listwidget_to_dict)
        self.sideBListWidget.model().rowsRemoved.connect(self.add_input_from_B_listwidget_to_dict)

        self.sideVListWidget.model().rowsInserted.connect(self.add_input_from_V_listwidget_to_dict)
        self.sideVListWidget.model().rowsRemoved.connect(self.add_input_from_V_listwidget_to_dict)

        self.sideGListWidget.model().rowsInserted.connect(self.add_input_from_G_listwidget_to_dict)
        self.sideGListWidget.model().rowsRemoved.connect(self.add_input_from_G_listwidget_to_dict)

        self.ComponentsListWidget.model().rowsInserted.connect(self.add_input_from_components_listwidget_to_dict)
        self.ComponentsListWidget.model().rowsRemoved.connect(self.add_input_from_components_listwidget_to_dict)


        '''Получение устройство заземления'''
        self.ground_equipment_A.clicked.connect(self.set_checked_ground_A)
        self.ground_equipment_B.clicked.connect(self.set_checked_ground_B)
        self.ground_equipment_V.clicked.connect(self.set_checked_ground_V)
        self.ground_equipment_G.clicked.connect(self.set_checked_ground_G)



    '''ФУНКЦИИ'''
    def get_type_of_inputs(self):
        '''Добавляет типы кабельнных вводов после выбора производителя кабельных вводов'''
        self.inputtypeComboBox.clear()
        if self.manufacturerInputsComboBox.currentText() != '' and \
            self.manufacturerInputsComboBox.currentText() != None:
                self.inputtypeComboBox.addItem('')
                self.inputtypeComboBox.addItems(
                    sorted(csv_reader.define_input_type(manufacturer=self.manufacturerInputsComboBox.currentText(),
                                                dict_with_manufacturer = \
                                                self.main_dict[self.manufacturerInputsComboBox.currentText()])))

    def take_widgets_for_cable_size(self):
        '''
        Определяет необходимые параметры, чтобы выбрать кабельный ввод
        Оставляет только то, что нужно для заполнения
        '''
        if self.inputtypeComboBox.currentText() != '' and self.inputtypeComboBox.currentText() != None:
            if '-МР' not in self.inputtypeComboBox.currentText() and 'Н-Т' not in self.inputtypeComboBox.currentText():
                self.tupeandmetalhoseComboBox.clear()
                self.tupeandmetalhoseWidget.setMaximumSize(0, 0)
                '''Прописать логику по максимальному диаметру предлагать только нужные МР и G'''
            elif '-МР' in self.inputtypeComboBox.currentText() and 'Н-Т' not in self.inputtypeComboBox.currentText():
                self.tupeandmetalhoseComboBox.clear()
                self.tupeandmetalhoseWidget.setMaximumSize(16666, 16666)
                self.tupeandmetalhoseLabel.setText('Диаметр металлорукава')
                self.tupeandmetalhoseComboBox.addItems(
                    ['', 'МР12', 'МР15', 'МР16', 'МР18', 'МР20', 'МР22', 'МР25', 'МР32', 'МР38'])
            elif '-МР' not in self.inputtypeComboBox.currentText() and 'Н-Т' in self.inputtypeComboBox.currentText():
                self.tupeandmetalhoseComboBox.clear()
                self.tupeandmetalhoseWidget.setMaximumSize(16666, 16666)
                self.tupeandmetalhoseLabel.setText('Трубная резьба')
                self.tupeandmetalhoseComboBox.addItems(
                    ['', 'G 3/8', 'G 1/2', 'G 3/4', 'G 1', 'G 1 1/4', 'G 1 1/2', 'G 2'])

    def make_manualinput(self):
        '''Добавляем список всех вводов производителя'''
        if self.manufacturerInputsComboBox.currentText() != '' and self.manufacturerInputsComboBox.currentText() != None:
            self.handwrite_inputspageComboBox.setEnabled(True)
            self.handwrite_inputspageComboBox.clear()
            self.all_name_inputs = csv_reader.create_list_with_fullnameinputs(
                self.main_dict[self.manufacturerInputsComboBox.currentText()])
            self.handwrite_inputspageComboBox.addItems(list(self.all_name_inputs.keys()))

    def add_box_locations_type(self):
        '''Добавляем расположение коробки'''
        self.boxlocationComboBox.clear()
        if self.manufacturerInputsComboBox.currentText() != '' and self.manufacturerInputsComboBox.currentText() != None:
            self.boxlocationComboBox.addItems(['','Горизонтальное','Вертикальное'])


    def search_size_for_input(self):
        '''Поиск размера кабельного ввода, который нужен'''
        if self.cablemaxoutLineEdit.text() != '' and self.cableminoutLineEdit.text() != '':
            value_min = new.define_min_input(self.cableminoutLineEdit.text())
            value_max = new.define_max_input(self.cablemaxoutLineEdit.text())

            # ПОИСК ЗАПЯТЫХ, КОТОРЫЕ НЕ ДАЮТ СДЕЛАТЬ НЕ FLOAT НЕ INT
            dict_diamerts_crimp_min = \
                self.main_dict[
                    self.manufacturerInputsComboBox.currentText()]['Кабельные вводы']['Диаметр обжимаемого кабеля мин']
            dict_diamerts_crimp_max = \
                self.main_dict[
                    self.manufacturerInputsComboBox.currentText()]['Кабельные вводы']['Диаметр обжимаемого кабеля макс']
            if new.check_that_max_more_then_min(max_value=value_max,
                                                min_value=value_min):
                for key_input in dict_diamerts_crimp_min:
                    self.main_dict[
                        self.manufacturerInputsComboBox.currentText()][
                            'Кабельные вводы']['Диаметр обжимаемого кабеля мин'][key_input] = \
                        new.change_cooma_to_dot(dict_diamerts_crimp_min[key_input])
                for key_input in dict_diamerts_crimp_max:
                    self.main_dict[
                        self.manufacturerInputsComboBox.currentText()][
                            'Кабельные вводы']['Диаметр обжимаемого кабеля макс'][key_input] = \
                        new.change_cooma_to_dot(dict_diamerts_crimp_max[key_input])

            dict_with_values = dict()

            # СЛОВАРЬ DICT_WITH_VALUES БУДЕТ ИМЕТЬ ВИД: {ключ как для мэин дикт для поиска строки:[мин диаметр, макс диаметр, диапазон попадания]}
            for diametrs in range(int(value_min), int(value_max) + 1):
                for key_input, value_dim_min in dict_diamerts_crimp_min.items():
                    if self.main_dict[
                        self.manufacturerInputsComboBox.currentText()]['Кабельные вводы']['Серия'][key_input] ==\
                            self.inputtypeComboBox.currentText():
                        if ';' not in str(value_dim_min) and 'х' not in str(value_dim_min):
                            if diametrs in range(
                                    int(float(value_dim_min)),
                                    int(float(dict_diamerts_crimp_max[key_input])) + 1):
                                if key_input not in dict_with_values:
                                    dict_with_values[key_input] = [float(value_dim_min),
                                                                   float(dict_diamerts_crimp_max[key_input]), 1]
                                else:
                                    dict_with_values[key_input][2] += 1

                        if ';' in str(value_dim_min):
                            if diametrs in range(
                                    int(float(value_dim_min.split(';')[0])),
                                    int(float(dict_diamerts_crimp_max[key_input].split(';')[0])) + 1):
                                if key_input not in dict_with_values:
                                    dict_with_values[key_input] = \
                                        [float(value_dim_min.split(';')[0]),
                                         float(dict_diamerts_crimp_max[key_input].split(';')[0]), 1]
                                else:
                                    dict_with_values[key_input][2] += 1

                        if ';' not in str(value_dim_min) and 'х' in str(value_dim_min):
                            if diametrs in range(
                                    int(float(value_dim_min.split('х')[0])),
                                    int(float(dict_diamerts_crimp_max[key_input].split('х')[0])) + 1):
                                if key_input not in dict_with_values:
                                    dict_with_values[key_input] = \
                                        [float(value_dim_min.split('х')[0]),
                                         float(dict_diamerts_crimp_max[key_input].split('х')[0])]
                                else:
                                    dict_with_values[key_input][2] += 1

            if self.tupeandmetalhoseComboBox.count() != 0:
                for key in dict_with_values.copy():
                    if 'G' in self.tupeandmetalhoseComboBox.currentText():
                        if ' ' in self.tupeandmetalhoseComboBox.currentText()[2:]:
                            if self.tupeandmetalhoseComboBox.currentText()[2:].replace(' ', '.') not in \
                                    self.all_name_inputs[key + 1]:
                                dict_with_values.pop(key)
                        else:
                            if self.tupeandmetalhoseComboBox.currentText()[2:] not in self.all_name_inputs[key + 1]:
                                dict_with_values.pop(key)
                    elif 'МР' in self.tupeandmetalhoseComboBox.currentText():
                        if self.tupeandmetalhoseComboBox.currentText() not in self.all_name_inputs[key + 1]:
                            dict_with_values.pop(key)

            search_max = 0
            min_diam_in_our_case = 10000
            raznica = 10000
            # поиск максимального числа вхождений
            for i, value in dict_with_values.copy().items():
                if search_max <= dict_with_values.copy()[i][2]:
                    search_max = dict_with_values.copy()[i][2]
            # удаление из словаря значений меньше по вхождениям
            for i, value in dict_with_values.copy().items():
                if value[2] < search_max:
                    dict_with_values.pop(i)
                else:
                    if min_diam_in_our_case >= value[1]:
                        min_diam_in_our_case = value[1]
            # Удаление из словаря значений меньше по наибольшему диаметру
            for i, value in dict_with_values.copy().items():
                if value[1] > min_diam_in_our_case:
                    dict_with_values.pop(i)
                else:
                    if raznica >= value[1] - value[0]:
                        raznica = value[1] - value[0]
            key_main = None
            for i, value in dict_with_values.copy().items():
                if value[1] - value[0] != raznica:
                    dict_with_values.pop(i)
                else:
                    key_main = i
            self.dict_with_current_input_value = dict_with_values

    def create_current_input_name(self):
        if self.manufacturerInputsComboBox.currentText() != '' and \
           self.manufacturerInputsComboBox.currentText() != None:
            if self.handwrite_inputspageComboBox.currentText() != None and \
               self.handwrite_inputspageComboBox.currentText() != '':
                    self.current_input_name = self.handwrite_inputspageComboBox.currentText()
            else:
                self.current_input_name = 'nan'
                if hasattr(self,'dict_with_current_input_value'):
                    if self.dict_with_current_input_value !={}:
                    #Проверка, если не заполнено в handwriteComboBox, то имя подобрать по верху
                        if self.handwrite_inputspageComboBox.currentText() == None or \
                            self.handwrite_inputspageComboBox.currentText() == '':
                            self.current_input_name = \
                                csv_reader.give_full_name_and_dict_for_input(
                                    dict_with_manufacturer= self.main_dict[self.manufacturerInputsComboBox.currentText()],
                                    key_input=list(self.dict_with_current_input_value.keys())[0])

    def clear_ABVG_spinbox_afted_add_button(self):
        # Установка нулевых значений в spinbox
        self.siteASpinBox.setValue(0)
        self.siteBSpinBox.setValue(0)
        self.siteVSpinBox.setValue(0)
        self.siteGSpinBox.setValue(0)
        self.cableminoutLineEdit.clear()
        self.cablemaxoutLineEdit.clear()
        if hasattr(self,'dict_with_current_input_value'):
            self.dict_with_current_input_value = {}


    def add_components_inputs(self, side):
        if self.V3V3.isChecked():
            self.ComponentsListWidget.addItem(f'В3-В3({self.current_input_name})-{side}')
        if self.V3V3e.isChecked():
            self.ComponentsListWidget.addItem(f'В3-В3е({self.current_input_name})-{side}')
        if self.K3.isChecked():
            self.ComponentsListWidget.addItem(f'К({self.current_input_name})-{side}')
        if self.kontrgaika.isChecked():
            self.ComponentsListWidget.addItem(f'КГ({self.current_input_name})-{side}')
        if self.GSH.isChecked():
            self.ComponentsListWidget.addItem(f'ГШ({self.current_input_name})-{side}')
        if self.CH.isChecked():
            self.ComponentsListWidget.addItem(f'Ч({self.current_input_name})-{side}')

    def add_inputsA_to_list_widget(self):
        if self.manufacturerInputsComboBox.currentText() != '' and self.manufacturerInputsComboBox.currentText() != None:
            if self.current_input_name != 'nan':
                if self.siteASpinBox.text() != '0':
                    for _ in range(0, int(self.siteASpinBox.text())):
                        self.sideAListWidget.addItem(self.current_input_name)
                        self.add_components_inputs('A')


    def add_inputsB_to_list_widget(self):
        if self.manufacturerInputsComboBox.currentText() != '' and self.manufacturerInputsComboBox.currentText() != None:
            if self.current_input_name != 'nan':
                if self.siteBSpinBox.text() != '0':
                    for _ in range(0, int(self.siteBSpinBox.text())):
                        self.sideBListWidget.addItem(self.current_input_name)
                        self.add_components_inputs('Б')


    def add_inputsV_to_list_widget(self):
        if self.manufacturerInputsComboBox.currentText() != '' and self.manufacturerInputsComboBox.currentText() != None:
            if self.current_input_name != 'nan':
                if self.siteVSpinBox.text() != '0':
                    for _ in range(0, int(self.siteVSpinBox.text())):
                        self.sideVListWidget.addItem(self.current_input_name)
                        self.add_components_inputs('В')


    def add_inputsG_to_list_widget(self):
        if self.manufacturerInputsComboBox.currentText() != '' and self.manufacturerInputsComboBox.currentText() != None:
            if self.current_input_name != 'nan':
                if self.siteGSpinBox.text() != '0':
                    for _ in range(0, int(self.siteGSpinBox.text())):
                        self.sideGListWidget.addItem(self.current_input_name)
                        self.add_components_inputs('Г')

    def add_all_inputs(self):
        self.add_inputsA_to_list_widget()
        self.add_inputsB_to_list_widget()
        self.add_inputsV_to_list_widget()
        self.add_inputsG_to_list_widget()
        self.current_input_name = 'nan'

    def clear_all_list_widget(self):
        self.sideAListWidget.clear()
        self.sideBListWidget.clear()
        self.sideVListWidget.clear()
        self.sideGListWidget.clear()
        self.ComponentsListWidget.clear()
        self.dict_with_inputs_on_side = {"А": [], "Б": [], 'В': [], "Г": [], "Крышка": []}

    def click_up_button_A(self):
        rowIndex = self.sideAListWidget.currentRow()
        currentItem = self.sideAListWidget.takeItem(rowIndex)
        self.sideAListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideAListWidget.setCurrentRow(rowIndex - 1)

    def click_up_button_B(self):
        rowIndex = self.sideBListWidget.currentRow()
        currentItem = self.sideBListWidget.takeItem(rowIndex)
        self.sideBListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideBListWidget.setCurrentRow(rowIndex - 1)

    def click_up_button_V(self):
        rowIndex = self.sideVListWidget.currentRow()
        currentItem = self.sideVListWidget.takeItem(rowIndex)
        self.sideVListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideVListWidget.setCurrentRow(rowIndex - 1)

    def click_up_button_G(self):
        rowIndex = self.sideGListWidget.currentRow()
        currentItem = self.sideGListWidget.takeItem(rowIndex)
        self.sideGListWidget.insertItem(rowIndex - 1, currentItem)
        self.sideGListWidget.setCurrentRow(rowIndex - 1)

    def click_up_button_components(self):
        rowIndex = self.ComponentsListWidget.currentRow()
        currentItem = self.ComponentsListWidget.takeItem(rowIndex)
        self.ComponentsListWidget.insertItem(rowIndex - 1, currentItem)
        self.ComponentsListWidget.setCurrentRow(rowIndex - 1)

    def click_down_button_A(self):
        rowIndex = self.sideAListWidget.currentRow()
        currentItem = self.sideAListWidget.takeItem(rowIndex)
        self.sideAListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideAListWidget.setCurrentRow(rowIndex + 1)

    def click_down_button_B(self):
        rowIndex = self.sideBListWidget.currentRow()
        currentItem = self.sideBListWidget.takeItem(rowIndex)
        self.sideBListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideBListWidget.setCurrentRow(rowIndex + 1)

    def click_down_button_V(self):
        rowIndex = self.sideVListWidget.currentRow()
        currentItem = self.sideVListWidget.takeItem(rowIndex)
        self.sideVListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideVListWidget.setCurrentRow(rowIndex + 1)

    def click_down_button_G(self):
        rowIndex = self.sideGListWidget.currentRow()
        currentItem = self.sideGListWidget.takeItem(rowIndex)
        self.sideGListWidget.insertItem(rowIndex + 1, currentItem)
        self.sideGListWidget.setCurrentRow(rowIndex + 1)

    def click_down_button_components(self):
        rowIndex = self.ComponentsListWidget.currentRow()
        currentItem = self.ComponentsListWidget.takeItem(rowIndex)
        self.ComponentsListWidget.insertItem(rowIndex + 1, currentItem)
        self.ComponentsListWidget.setCurrentRow(rowIndex + 1)

    def click_delete_button_A(self):
        rowIndex = self.sideAListWidget.currentRow()
        currentItem = self.sideAListWidget.takeItem(rowIndex)

    def click_delete_button_B(self):
        rowIndex = self.sideBListWidget.currentRow()
        currentItem = self.sideBListWidget.takeItem(rowIndex)

    def click_delete_button_V(self):
        rowIndex = self.sideVListWidget.currentRow()
        currentItem = self.sideVListWidget.takeItem(rowIndex)

    def click_delete_button_G(self):
        rowIndex = self.sideGListWidget.currentRow()
        currentItem = self.sideGListWidget.takeItem(rowIndex)

    def click_delete_button_components(self):
        rowIndex = self.ComponentsListWidget.currentRow()
        currentItem = self.ComponentsListWidget.takeItem(rowIndex)

    def add_input_from_A_listwidget_to_dict(self):
        if self.sideAListWidget.count() != 0:
            list_from_sideAListWidget = [self.sideAListWidget.item(i).text()
                                                  for i in range(0, self.sideAListWidget.count())]
            self.dict_with_inputs_on_side["А"] = list_from_sideAListWidget
            self.dict_for_save_blocks_before_draw['inputs'] = \
                inputs_create.create_list_for_drawing_inputs(self.dict_with_inputs_on_side)
        else:
            self.dict_with_inputs_on_side["А"] = []

    def add_input_from_B_listwidget_to_dict(self):
        if self.sideBListWidget.count() != 0:
            list_from_sideBListWidget = [self.sideBListWidget.item(i).text()
                                                  for i in range(0, self.sideBListWidget.count())]
            self.dict_with_inputs_on_side["Б"] = list_from_sideBListWidget
            self.dict_for_save_blocks_before_draw['inputs'] = \
                inputs_create.create_list_for_drawing_inputs(self.dict_with_inputs_on_side)
        else:
            self.dict_with_inputs_on_side["Б"] = []

    def add_input_from_V_listwidget_to_dict(self):
        if self.sideVListWidget.count() != 0:
            list_from_sideVListWidget = [self.sideVListWidget.item(i).text()
                                                  for i in range(0, self.sideVListWidget.count())]
            self.dict_with_inputs_on_side["В"] = list_from_sideVListWidget
            self.dict_for_save_blocks_before_draw['inputs'] = \
                inputs_create.create_list_for_drawing_inputs(self.dict_with_inputs_on_side)
        else:
            self.dict_with_inputs_on_side["В"] = []

    def add_input_from_G_listwidget_to_dict(self):
        if self.sideGListWidget.count() != 0:
            list_from_sideGListWidget = [self.sideGListWidget.item(i).text()
                                                  for i in range(0, self.sideGListWidget.count())]
            self.dict_with_inputs_on_side["Г"] = list_from_sideGListWidget
            self.dict_for_save_blocks_before_draw['inputs'] = \
                inputs_create.create_list_for_drawing_inputs(self.dict_with_inputs_on_side)
        else:
            self.dict_with_inputs_on_side["Г"] = []

    def add_input_from_components_listwidget_to_dict(self):
        if self.ComponentsListWidget.count() != 0:
            list_from_ComponentsListWidget = [self.ComponentsListWidget.item(i).text()
                                                  for i in range(0, self.ComponentsListWidget.count())]
            self.dict_with_inputs_on_side["Крышка"] = list_from_ComponentsListWidget
            self.dict_for_save_blocks_before_draw['inputs'] = \
                inputs_create.create_list_for_drawing_inputs(self.dict_with_inputs_on_side)


    def calculate_coordinates_for_inputs(self, x, y, list_with_diametrs):
        '''
        :param x: длина
        :param y: ширина
        :param list_with_diametrs: Словарь, который уже передается со списком, в котором каждый диаметр меньше Min(x,y)
        и ко всем диаметрам добавлено по 10 мм
        :return:
        '''
        min_size = min(x, y)
        list_with_diametrs = sorted(list_with_diametrs, reverse=True)
        level = 0
        level_box = f'{level}_{list_with_diametrs[0]}'
        level_box_for_packing = list_with_diametrs[0]
        dict_key_level_value_alldiametrs_in_level = {[level, level_box]: [level_box_for_packing]}
        level_size = min_size * 1
        for cont, value in enumerate(list_with_diametrs):
            if cont != 0:
                if level_size - level_box_for_packing >= value:
                    level_size -= value
                    dict_key_level_value_alldiametrs_in_level[[level, level_box]].append(value)
                else:
                    level_size = min_size * 1
                    level += 1
                    level_box = f'{level}_{value}'
                    level_box_for_packing = value
                    dict_key_level_value_alldiametrs_in_level[[level, level_box]].append(value)

    def delete_R_in_russian_input_name(self):
        '''
        Удаление расширенного ввода
        {'А': ['ВЗ-Н25', 'ВЗ-Н25'], 'Б': ['ВЗ-Н25'], 'В': ['ВЗ-Н25', 'ВЗ-Н25'], 'Г': [], 'Крышка': []}
        :return:
        '''
        if self.dict_with_inputs_on_side is not None:
            for shell_side in self.dict_with_inputs_on_side.copy():
                if self.dict_with_inputs_on_side[shell_side] != []:
                    for count, russian_input_name in enumerate(self.dict_with_inputs_on_side[shell_side]):
                        if '/Р' in russian_input_name:
                            self.dict_with_inputs_on_side[shell_side][count] = russian_input_name.replace('/Р', '')
                        else:
                            continue

    def set_checked_ground_A(self):
        if self.ground_equipment_A.isChecked():
            self.ground_equipment_B.setChecked(False)
            self.ground_equipment_V.setChecked(False)
            self.ground_equipment_G.setChecked(False)

            if 'ground_exd' not in self.dict_for_save_blocks_before_draw['inputs']:
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exd')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exe')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withcap')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withoutcap')

    def set_checked_ground_B(self):
        if self.ground_equipment_B.isChecked():
            self.ground_equipment_A.setChecked(False)
            self.ground_equipment_V.setChecked(False)
            self.ground_equipment_G.setChecked(False)

            if 'ground_exd' not in self.dict_for_save_blocks_before_draw['inputs']:
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exd')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exe')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withcap')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withoutcap')

    def set_checked_ground_V(self):
        if self.ground_equipment_V.isChecked():
            self.ground_equipment_B.setChecked(False)
            self.ground_equipment_A.setChecked(False)
            self.ground_equipment_G.setChecked(False)
            if 'ground_exd' not in self.dict_for_save_blocks_before_draw['inputs']:
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exd')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exe')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withcap')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withoutcap')

    def set_checked_ground_G(self):
        if self.ground_equipment_G.isChecked():
            self.ground_equipment_B.setChecked(False)
            self.ground_equipment_V.setChecked(False)
            self.ground_equipment_A.setChecked(False)

            if 'ground_exd' not in self.dict_for_save_blocks_before_draw['inputs']:
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exd')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_exe')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withcap')
                self.dict_for_save_blocks_before_draw['inputs'].append('ground_withoutcap')



    def get_coordinates_for_side(self):
        '''
        Получение координат словарем self.dict_with_list_coordinates_on_side_for_dxf для построения в dxf
        {'А': {0: {'ВЗ-Н25': [32.11666666666667, 37.5]}, 1: {'ВЗ-Н25': [87.88333333333333, 37.5]}},
        'Б': {0: {'ВЗ-Н25': [24.783333333333335, 37.5]}, 1: {'ВЗ-Н25': [73.21666666666667, 37.5]}},
        'В': {},
        'Г': {},
        'Крышка': {}}
        '''
        self.delete_R_in_russian_input_name()#Удаляем расширенный ввод в названиях на русском
        if hasattr(self, 'polyline_xy_coordinate_side'):
            for shell_side, list_with_inputs_on_rus_language in self.dict_with_inputs_on_side.items():
                if list_with_inputs_on_rus_language != []:
                    #Получение координат области полилинии
                    shell_side_dxf = \
                        input_create_examples.define_side(side_russian_name=shell_side)
                    main_surface = \
                        input_create_examples.define_rectangle_size_for_inputs(
                            dict_with_x_y_coordinates=self.polyline_xy_coordinate_side[shell_side_dxf])
                    max_size = max(main_surface['xy1'][0] - main_surface['xy0'][0],
                                   main_surface['xy1'][1] - main_surface['xy0'][1])
                    min_size = min(main_surface['xy1'][0] - main_surface['xy0'][0],
                                   main_surface['xy1'][1] - main_surface['xy0'][1])
                    list_with_diametrs_float = [input_create_examples.return_diametr_from_name(dict_all_names_dict=self.all_name_inputs,
                                                                                        name_input= rus_input_name) for rus_input_name in list_with_inputs_on_rus_language]
                    list_on_side = [
                        [rus_input_name, list_with_diametrs_float[count]]
                        for count,rus_input_name in enumerate(list_with_inputs_on_rus_language)]

                    if self.ground_equipment_A.isChecked() and shell_side == "А":
                        list_with_diametrs_float.append(16)
                        list_on_side.append(['Устройство заземления',16])
                    if self.ground_equipment_B.isChecked() and shell_side == "Б":
                        list_with_diametrs_float.append(16)
                        list_on_side.append(['Устройство заземления',16])
                    if self.ground_equipment_V.isChecked() and shell_side == "В":
                        list_with_diametrs_float.append(16)
                        list_on_side.append(['Устройство заземления',16])
                    if self.ground_equipment_G.isChecked() and shell_side == "Г":
                        list_with_diametrs_float.append(16)
                        list_on_side.append(['Устройство заземления',16])


                    dict_on_side = {count:i for count,i in enumerate(sorted(list_on_side,key=lambda x: x[1], reverse=True))}
                    dict_on_side_copy = dict_on_side.copy()
                    keynumber_for_delete_input = 0
                    start_rectangle = 0
                    while input_create_examples.checking_clear_inputs_dict(
                            dict_with_inputs_name_and_diam=dict_on_side):
                        ###
                        #ЕСЛИ ПОМЕЩАЕТСЯ В ОДНУ ЛИНИЮ
                        ###
                        if input_create_expamles_check.check_possible_to_add_all_inputs_in_one_row(
                                free_space=max_size-start_rectangle,
                                list_with_diametrs_float=[list(i)[1] for i in dict_on_side.values()]):
                            coordinate_input_one_row = input_create_expamles_check.set_coordinate_one_row(
                                x_coordinate= input_create_expamles_check.calculate_x_one_row(
                                    start_rectangle_for_paint=start_rectangle,diametr_float=list_with_diametrs_float[keynumber_for_delete_input]
                                ),
                                y_coordinate=main_surface['xy0'][1] + min_size/2
                            )

                            self.dict_with_list_coordinates_on_side_for_dxf[shell_side][keynumber_for_delete_input] = \
                                {dict_on_side_copy[keynumber_for_delete_input][0]:coordinate_input_one_row}

                            start_rectangle = input_create_expamles_check.find_start_of_rectangle_one_row(
                                        start_rectangle=start_rectangle,
                                        diametr_float=list_with_diametrs_float[keynumber_for_delete_input]
                                    )

                        #в конце удаление ввода
                            input_create_examples.delete_input_from_dict(dict_with_inputs_name_and_diam=dict_on_side,
                                                                         keynumber_for_delete_input=keynumber_for_delete_input)
                            if dict_on_side == {}:
                                free_space = max_size - start_rectangle + 5
                                if max(list(self.dict_with_list_coordinates_on_side_for_dxf[shell_side].keys())) == 0:
                                    for number in self.dict_with_list_coordinates_on_side_for_dxf[shell_side]:
                                        for input_rus_name in self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number]:
                                            self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number][
                                                input_rus_name][0] = main_surface['xy0'][0] + max_size/2
                                else:
                                    for number in self.dict_with_list_coordinates_on_side_for_dxf[shell_side]:
                                        for input_rus_name in self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number]:
                                            self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number][input_rus_name][0]= \
                                                self.dict_with_list_coordinates_on_side_for_dxf[shell_side][number][
                                                    input_rus_name][0] + free_space * (number+1)/(max(list(self.dict_with_list_coordinates_on_side_for_dxf[shell_side].keys()))+2)
                                    # continue
                        else:
                            continue
                        keynumber_for_delete_input = keynumber_for_delete_input + 1

            return self.dict_with_list_coordinates_on_side_for_dxf


if __name__ == '__main__':
    path_to_csv = os.getcwd() + '\Общая база'
    path_to_dxf = '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\Оболочка\\ContainerVer02.dxf'
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = InputsPageSetup(path_to_csv = path_to_csv,
                                     path_to_dxf = path_to_dxf)
    welcome_window.show()
    sys.exit(app.exec_())