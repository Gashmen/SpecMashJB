#python -m PyQt5.uic.pyuic mainver02.ui -o mainver02.py
import os

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PyQt5.QtWidgets import QMessageBox, QDialog

import src.pyui_files.mainver02_1108 as designer_ui
import src.pyui_files.error as error_ui
from src.qt_creating import help_ui
import src.csv_reader.csv_reader as csv_reader
from src.dxf_changer import TERMINAL_DB
from src.authentication import backend_auth
from src.pdf_creator import pdf_main
class ExtendedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)#Виджет принимает фокус клавиатуры за счет табуляции или по щелчку - НЕ ПОНИМАЮ ЗАЧЕМ
        self.setEditable(True)
        # add a filter model to filter matching items
        self.pFilterModel = QtCore.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)#Чувствительность к регистру в поиске - сейчас установлено, что не чувствительно
        self.pFilterModel.setSourceModel(self.model())

        # # add a completer, which uses the filter model
        self.completer = QtWidgets.QCompleter(self.pFilterModel, self)#Автозавершение, когда начинаешь вводить, показывает способы завершения слова
        # # always show all (filtered) completions
        self.completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited[str].connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)
    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))
    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)
    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

class CustomFileDialogCsv(QtWidgets.QFileDialog):
    def __init__(self):
        super().__init__()

    def closeEvent(self,event):
        reply = QtWidgets.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()

class Mainver(QtWidgets.QMainWindow, designer_ui.Ui_MainWindow):

    def __init__(self,save_path = None,path_to_csv = None,path_to_terminal_dxf = None):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)

        if not hasattr(self,'save_path'):
            self.save_path = save_path
        if not hasattr(self, 'path_to_csv'):
            self.path_to_csv = path_to_csv

        if not hasattr(self, 'path_to_terminal_dxf'):
            if path_to_terminal_dxf != None:
                self.path_to_terminal_dxf = path_to_terminal_dxf
                self.add_manufacturer_terminal_combobox()
            else:
                self.add_manufacturer_terminal_combobox()

        '''НЕОБХОДИМЫЕ ПЕРЕМЕННЫЕ ПРИ ЗАПУСКЕ'''

        self.path_to_csv = None
        self.main_information = None #Переменная, куда сохраняется все.
        self.csv_file_dialog = CustomFileDialogCsv()
        self.doc_new = None
        self.doc_nameplate = None
        self.list_added_blocks = list()

        '''Дополнительные окна при запуске'''
        self.error_window = error_ui.Ui_WidgetError()

        '''Словарь блоков, которые нужно оставить для рисования dxf {shell_name:[block_1,block_2...],...}'''
        self.dict_for_save_blocks_before_draw = {'border':['Border_A3']}

        '''Если заранее задан путь csv'''
        self.create_main_dict_and_manufacturer_combobox(path_to_csv)

        '''Если не задан путь csv'''
        self.csv_Button.clicked.connect(self.get_csv_file)


        '''Заполнение штампов'''
        self.task_number = ''
        self.position_number = ''


        '''BUTTON FUNCTIONS'''
        self.shellButton_leftMenu.clicked.connect(self.set_shell_page)

        self.inputsButton_leftMenu.clicked.connect(self.set_inputs_page)

        self.terminalButton_leftMenu.clicked.connect(self.set_terminal_page)

        self.optionsButton_leftMenu.clicked.connect(self.set_options_page)

        self.helpwindowButton.clicked.connect(self.open_help_window)

        self.pushButton_2.clicked.connect(self.call_error)

        self.welcomewindowButton.clicked.connect(self.home_window)



    '''ИЗМЕНЕНИЕ СТРАНИЦ В SHELL PAGE'''
    def set_shell_page(self):
        '''Устанавливает 0 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count():
            self.stackedWidget.setCurrentIndex(0)

    def set_inputs_page(self):
        '''Устанавливает 1 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 1:
            self.stackedWidget.setCurrentIndex(1)

    def set_terminal_page(self):
        '''Устанавливает 2 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 2:
            self.stackedWidget.setCurrentIndex(2)

    def set_options_page(self):
        '''Устанавливает 3 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 3:
            self.stackedWidget.setCurrentIndex(3)

    def open_help_window(self):
        '''Открытие окна help'''
        help_window = help_ui.ClssDialog(self)
        help_window.exec_()

    def closeEvent(self, e):
        '''Переопределяет closeEvent, чтобы перед закрытием главного окна спрашивало, закрыть или нет'''
        result = QtWidgets.QMessageBox.question(self, "Подтверждение закрытия окна",
           "Закрыть файл?",
           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
           QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()

    def save_doc_new(self):
        '''При нажатии на предпросмотр сохраняет файл'''
        if self.doc_new is not None:
            if self.save_path is not None:
                self.doc_new.saveas(self.save_path + '\\box')
            else:
                doc_filename,_ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                     directory= '\\'.join(os.getcwd().split('\\')[0:-1]),
                                                                     caption="Сохранение dxf файла",
                                                                     filter= 'DXF Files(*.dxf)')
                if doc_filename:
                    self.doc_new.saveas(doc_filename[:-3] + '_1.dxf')
                    self.doc_nameplate.saveas(doc_filename[:-3] + '_2.dxf')
                    pdf_main.save_pdf(doc_filename[:-3] + '_1.dxf')
                    pdf_main.save_pdf(doc_filename[:-3] + '_2.dxf')




    def save_doc_bom(self):
        '''При нажатии на предпросмотр сохраняет файл'''
        if self.doc_bom is not None:
            doc_bom_filename,_ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                 directory= '\\'.join(os.getcwd().split('\\')[0:-1]),
                                                                 caption="Сохранение dxf файла",
                                                                 filter= 'DXF Files(*.dxf)')
            if doc_bom_filename != '':
                self.doc_bom.saveas(doc_bom_filename)

    '''Получение main_dict и заполнение первых ComboBox Widget на каждой странице'''
    def create_csv_main_dict(self):
        '''path_to_csv - это путь до папок, где лежат куча csv файлов'''

        if self.path_to_csv is not None:
            try:
                return csv_reader.get_main_dict(self.path_to_csv)
            except:
                return {}

    def add_manufacturer_shell_combobox(self):
        '''Добавляет производителей при появление csv файла'''
        if self.main_dict is not {}:
            self.manufactureComboboxWidget_shellpage.clear()
            list_manufacturer_for_shell = csv_reader.define_list_manufacturer_for_shell(main_dict=self.main_dict)
            self.manufactureComboboxWidget_shellpage.addItems(list_manufacturer_for_shell)

    def add_manufacturer_inputs_combobox(self):
        '''Добавляет производителей при появление csv файла'''
        if self.main_dict is not {}:
            self.manufacturerInputsComboBox.clear()
            list_manufacturer_for_input = csv_reader.define_list_manufacturer_for_input(main_dict=self.main_dict)
            self.manufacturerInputsComboBox.addItems(list_manufacturer_for_input)

    def add_manufacturer_terminal_combobox(self):
        '''Добавляет производителей клемм, если есть путь до клемм'''
        self.manufacturer_terminal_combobox.clear()
        self.terminal_full_names = TERMINAL_DB.define_names_terminal(path_to_terminal_dxf = self.path_to_terminal_dxf)
        self.manufacturer_terminal_combobox.addItem('')
        list_manufacturer_for_terminal = \
            list(TERMINAL_DB.define_manufacturer(self.terminal_full_names))
        self.manufacturer_terminal_combobox.addItems(list_manufacturer_for_terminal)

    def get_inputs_manufacturer(self):
        if hasattr(self,'main_dict'):
            if not self.manufacturerInputsComboBox.count():
                self.manufactureComboboxWidget_shellpage.addItems(
                    csv_reader.define_list_manufacturer_for_shell(self.main_dict))

    def define_manufacturer_terminal(self):
        '''Определяем производетелей клемм по dxf файлу'''
        self.terminal_full_names = TERMINAL_DB.define_names_terminal()
        self.manufacturer_terminal_combobox.addItem('')
        self.manufacturer_terminal_combobox.addItems(list(TERMINAL_DB.define_manufacturer(self.terminal_full_names)))

    def create_main_dict_and_manufacturer_combobox(self,csv_path = None):
        '''Создает
        main_dict :{'АТЭКС': {'Exd оболочки': {'Серия': {0: nan, 1: nan, 2: nan...
        csv_path: 'C:/Users/g.zubkov/PycharmProjects/marshallingboxes/Общая база'
        '''
        if csv_path is not None:
            if csv_path != '':
                self.path_to_csv = csv_path
                self.main_dict = self.create_csv_main_dict()
                if self.main_dict != {}:
                    self.add_manufacturer_shell_combobox()
                    self.add_manufacturer_inputs_combobox()
                else:
                    self.manufactureComboboxWidget_shellpage.clear()
                    self.manufacturerInputsComboBox.clear()

    def get_csv_file(self):
        '''Определение пути до папки с базой CSV'''
        csv_path = self.csv_file_dialog.getExistingDirectory(self,
                                                             caption="Выбрать папку БД")
        self.create_main_dict_and_manufacturer_combobox(csv_path=csv_path)

    def call_error(self):
        '''открытие окна ошибки'''
        self.error_window.show()

        # QMessageBox.critical(self, "Ошибка ", "Тестирование QMessageBox из call_error", QMessageBox.Ok)

    def home_window(self):
        '''открытие окна дом'''
        self.home_window = backend_auth.AuthWindow()
        self.home_window.set_task_number(self.task_number)
        self.home_window.set_position_number(self.position_number)
        self.close()
        self.home_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = Mainver(path_to_terminal_dxf= '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\Клеммы\\checkcheck.dxf')
    welcome_window.show()
    sys.exit(app.exec_())

