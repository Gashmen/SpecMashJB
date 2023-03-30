import os

import ezdxf
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from src.qt_creating import terminal_ui
from src.dxf_changer import TERMINAL_DB
from src.dxf_creating import import_module, shell_create, main_shell_create,terminal_create,inputs_create
from src.dxf_creating import move_inserts


class DxfCreator(terminal_ui.TerminalPage):

    def __init__(self,
                 save_path = None,
                 path_to_csv = None,
                 path_to_dxf = None,
                 path_to_terminal_dxf = None
                 ):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__(save_path=save_path,
                         path_to_csv=path_to_csv,
                         path_to_dxf=path_to_dxf,
                         path_to_terminal_dxf=path_to_terminal_dxf
                         )

        self.previewButton_leftMenu.clicked.connect(self.create_shell_dxf_after_selfkey)
        self.previewButton_leftMenu.clicked.connect(self.create_inputs_dxf_after_shell)
        self.previewButton_leftMenu.clicked.connect(self.create_terminals_dxf_after_DIN_REYKA)
        self.previewButton_leftMenu.clicked.connect(self.save_doc_new)

        '''Для планшета ставлю значения спинбоксов заранее, т.к. не видно их и нет дизайнера тут'''
        self.siteASpinBox.setValue(2)
        self.siteBSpinBox.setValue(1)
        self.siteVSpinBox.setValue(2)
        # self.test_write()

    def create_shell_dxf_after_selfkey(self):
        '''Создание dxf оболочки'''
        if self.shell_key != None:
            if 'shell' in self.dict_for_save_blocks_before_draw.keys():
                self.doc_new = import_module.clear_base_doc_for_new(
                    dxfbase_path=self.path_to_dxf,
                    dict_for_save_blocks_before_draw=self.dict_for_save_blocks_before_draw)
            shell_create.create_all_shells(doc=self.doc_new,
                                           shell_name=self.shell_name,
                                           extreme_lines=shell_create.define_extreme_lines_in_all_blocks(doc=self.doc_new))

    def create_inputs_dxf_after_shell(self):
        '''Создание вводов на сторонах оболочки'''
        if hasattr(self,'doc_new'):
            '''Проверка на тип взрывозащиты'''
            ex_protection = None
            if 'exe' in self.safefactortypeCombobox_shellpage.currentText().lower():
                ex_protection = 'exe'
            elif 'exd' in self.safefactortypeCombobox_shellpage.currentText().lower():
                ex_protection = 'exd'
            else:
                ex_protection = None

            if ex_protection != None:
                inputs_create.create_inputs_in_block(doc=self.doc_new,
                                                     dict_before_match=self.dict_with_list_coordinates_on_side_for_dxf,
                                                     full_shale_name=self.shell_name,
                                                     type_of_explosion=ex_protection)
                self.input_max_len = move_inserts.move_shells_after_inputs(doc=self.doc_new,
                                                                           shell_name=self.shell_name)
                self.boundaries_drawing = move_inserts.get_boundaries_drawing(doc=self.doc_new,
                                                                              shell_name=self.shell_name,
                                                                              input_max_len=self.input_max_len)
                self.scale_drawing = move_inserts.define_scale(doc=self.doc_new,
                                                               shell_name=self.shell_name,
                                                               input_max_len=self.input_max_len)
                inputs_create.create_inputs_on_topside_withoutcapside(doc=self.doc_new,
                                                                      shell_name=self.shell_name)

    def create_terminals_dxf_after_DIN_REYKA(self):
        '''Добавление клемм на DIN рейку'''
        if hasattr(self,'doc_new'):
            din_reyka = terminal_create.check_din_reyka(self.doc_new, self.shell_name)
            if din_reyka:
                len_din_reyka = terminal_create.define_len_terminal(self.doc_new, din_reyka.dxf.name)
                if hasattr(self,'list_with_terminals'):
                    list_with_terminals = self.list_with_terminals

                    '''Поиск длины всех клемм и самой первой'''
                    summary_terminal_len = sum([terminal_create.define_len_terminal(self.doc_new,terminal)
                                                for terminal in list_with_terminals])

                    len_first_terminal = terminal_create.define_len_terminal(self.doc_new, list_with_terminals[0])

                    if len_din_reyka > summary_terminal_len:
                        terminal_create.create_terminal_on_din(doc_after_import=self.doc_new,
                                                               list_terminal_blocks=list_with_terminals,
                                                               din_reyka_insert=din_reyka)


                    self.list_for_import_terminal = terminal_create.create_list_for_drawing_terminal(self.list_from_terminal_listwidget)

            move_inserts.scale_all_insert(doc=self.doc_new,
                                          scale=self.scale_drawing)

    def test_write(self):
        self.manufactureComboboxWidget_shellpage.setCurrentText('ВЗОР')
        self.safefactortypeCombobox_shellpage.setCurrentText('Exe оболочки')
        self.serialCombobox_shellpage.setCurrentText('ВП')
        self.sizeCombobox_shellpage.setCurrentText('161610')
        self.gas_mark_RadioButton_shellpage.setChecked(True)
        self.gasdustoreComboBox_shellpage.setCurrentText('1Ex e IIC')
        self.temperature_class_comboBox_shellpage.setCurrentText('T4')
        self.manufacturerInputsComboBox.setCurrentText('ВЗОР')
        self.inputtypeComboBox.setCurrentText('ВЗ-Н')
        self.handwrite_inputspageComboBox.setCurrentText('ВЗ-Н25')
        self.siteASpinBox.setValue(2)
        self.siteBSpinBox.setValue(1)
        self.siteVSpinBox.setValue(2)
        self.manufacturer_terminal_combobox.setCurrentText('SUPU')
        self.mounttype_terminal_combobox.setCurrentText('Винтовые')
        self.appointment_terminal_combobox.setCurrentText('L')
        self.conductorsection_terminal_combobox.setCurrentText('16')
        self.count_terminal_spinbox.setValue(3)

if __name__ == '__main__':
    path_to_csv = '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\bd'
    path_to_dxf_shell = '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\dxf_base\\DXF_BASE.dxf'
    path_to_terminal_dxf = '\\'.join(os.getcwd().split('\\')[0:-1]) + '\\dxf_base\\DXF_BASE.dxf'

    app = QtWidgets.QApplication(sys.argv)
    welcome_window = DxfCreator(path_to_csv=path_to_csv,
                                    path_to_dxf = path_to_dxf_shell,
                                  path_to_terminal_dxf=path_to_terminal_dxf)
    welcome_window.show()
    sys.exit(app.exec_())