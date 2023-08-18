import ezdxf
import datetime
from ezdxf.entities import Attrib
def create_nameplate_doc(dxfbase_path:str):
    '''
    Удаляем все ненужное из dxf_base и возвращаем doc_nameplate
    :dxfbase_path : C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf
    '''

    doc_nameplate = ezdxf.readfile(dxfbase_path)

    doc_nameplate_for_del = ezdxf.readfile(dxfbase_path)

    doc_nameplate.modelspace().delete_all_entities()

    for block in doc_nameplate_for_del.blocks:
        try:
            if block.dxf.name != 'nameplate' and block.dxf.name != 'Border_A3' and 'Model_Space' not in block.dxf.name and 'Paper_Space' not in block.dxf.name:
                    doc_nameplate.blocks.delete_block(name=block.dxf.name)
        except:
            continue
    return doc_nameplate

def create_nameplate_insert(doc_nameplate, extreme_lines_border_insert):
    '''
    Создает insert nameplate
    :param doc_nameplate:
    :param extreme_lines_border_insert:
    :return:
    '''
    block_nameplate = doc_nameplate.blocks['nameplate']
    values = {attdef.dxf.tag: '' for attdef in block_nameplate.query('ATTDEF')}

    insert_x = extreme_lines_border_insert['x_min'] + \
               (extreme_lines_border_insert['x_max'] - extreme_lines_border_insert['x_min']) / 2

    insert_y = extreme_lines_border_insert['y_min'] + \
               (extreme_lines_border_insert['y_max'] - extreme_lines_border_insert['y_min']) / 2

    if doc_nameplate.blocks.get('nameplate'):
        nameplate_insert = doc_nameplate.modelspace().add_blockref(name='nameplate',
                                                      insert=(insert_x,insert_y))
        nameplate_insert.add_auto_attribs(values)

        return nameplate_insert

def write_attrib_box_full_name(attrib,full_name,add_numbers='.XXXX.XX'):
    '''
    Заполнение аттрибута BOX_FULL_NAME
    :param attrib: аттрибут в nameplate
    :param full_name: КВП.261610
    :param add_numbers: .{номер заявки}.{номер изделия в этой заявке}
    :return:
    '''

    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'BOX_FULL_NAME':
            attrib.dxf.text = f'{full_name}-{str(datetime.datetime.now())[2:4]}{add_numbers}'

def write_explosion_tag(attrib, gasdustore='1 Ex e IIC',temperature_class='T6', IP='66'):

    '''self.gasdustoreComboBox_shellpage.currentText() + ' ' + self.temperature_class_comboBox_shellpage.currentText() + ' Gb, IP66'''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'EXPLOSION_TAG':
            attrib.dxf.text = f'{gasdustore} {temperature_class} Gb, IP{IP}'

def write_minus_temperature(attrib, minus_temperature = '-60'):
    '''Написание минусовой температуры
    self.mintempLineEdit_shellpage.text()
    '''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'MINUS_TEMPERATURE':
            attrib.dxf.text = f'{minus_temperature}'

def write_plus_temperature(attrib, plus_temperature = '+40'):
    '''Написание плюсовой температуры
    self.maxtempLineedit_shellpage.text()
    '''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'PLUS_TEMPERATURE':
            attrib.dxf.text = f'+{plus_temperature}'

def write_voltage_current_frequency(attrib, voltage='230',current='32',frequency='50/60'):
    '''Заполнените тэга V_I_F'''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'V_I_F':
            attrib.dxf.text = f'~{voltage}В {current}А {frequency}Гц'

def write_batch_number(attrib, batch_number='XXXXXXXXX'):
    '''Заполнение тэна BATCH_NUMBER'''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'BATCH_NUMBER':
            attrib.dxf.text = f'Парт. № {batch_number}'

def write_just_attrib_1(attrib,just_attrib_1 = 'ОТКРЫВАТЬ'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_1':
            attrib.dxf.text = f'{just_attrib_1}'

def write_just_attrib_2(attrib,just_attrib_2 = 'ОТКЛЮЧИВ ОТ СЕТИ'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_2':
            attrib.dxf.text = f'{just_attrib_2}'

def write_just_attrib_3(attrib,just_attrib_3 = 'C  ≤ Ta ≤          C'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_3':
            attrib.dxf.text = f'{just_attrib_3}'

def write_just_attrib_4(attrib,just_attrib_4 = 'o'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_4':
            attrib.dxf.text = f'{just_attrib_4}'










