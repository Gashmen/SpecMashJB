import ezdxf

def define_names_terminal(
        path_to_terminal_dxf = 'C:\\Users\\g.zubkov\\PycharmProjects\\marshallingboxes\\Клеммы\\checkcheck.dxf'):

    doc = ezdxf.readfile(path_to_terminal_dxf)
    names_of_terminal = list()
    for block in doc.blocks:
        if block.dxf.name[0] != 'U' and block.dxf.name[1] not in '0123456789' and '*' not in block.dxf.name:
            names_of_terminal.append('_'.join(block.dxf.name.split('_')[0:4]))

    return list(set(names_of_terminal))

def define_manufacturer(names_of_terminal):
    MANUFACTURER = list(set([manufacturer.split('_')[0] for manufacturer in names_of_terminal]))
    return MANUFACTURER

def define_type_of_terminal(names_of_terminal:list, manufacturer:str):
    if manufacturer:
        TYPE_OF_TERMINAL = list()
        for terminal in names_of_terminal:
            if manufacturer == terminal.split('_')[0]:
                if terminal.split('_')[1].lower() == 'screw':
                    TYPE_OF_TERMINAL.append('Винтовые')
                elif terminal.split('_')[1].lower() == 'spring':
                    TYPE_OF_TERMINAL.append('Пружинные')
        return list(set(TYPE_OF_TERMINAL))
    else:
        return ['']

def define_appointment_of_terminal(names_of_terminal:list, manufacturer:str,type_of_terminal:str):

    if manufacturer and type_of_terminal:
        TYPEOFTERMINAL = 'SCREW' if type_of_terminal == 'Винтовые' else 'SPRING'
        appointment_of_terminal = list()
        for terminal in names_of_terminal:
            if manufacturer == terminal.split('_')[0] and terminal.split('_')[1] == TYPEOFTERMINAL:
                if terminal.split('_')[2] == 'WHITE':
                    appointment_of_terminal.append('L')
                elif terminal.split('_')[2] == 'BLUE':
                    appointment_of_terminal.append('N')
                elif terminal.split('_')[2] == 'GREEN':
                    appointment_of_terminal.append('PE')
        return list(set(appointment_of_terminal))
    else:
        return ['']

def define_conductorsection_terminal(names_of_terminal:list,manufacturer:str,type_of_terminal: str,appointment_of_terminal:str):

    if manufacturer and type_of_terminal and appointment_of_terminal:
        TYPEOFTERMINAL = 'SCREW' if type_of_terminal == 'Винтовые' else 'SPRING'
        APPOINMENT = 'WHITE' if appointment_of_terminal == 'L' else 'BLUE' if appointment_of_terminal == 'N' else 'GREEN'
        conductor_section = list()
        for terminal in names_of_terminal:
            if manufacturer == terminal.split('_')[0] and\
                    terminal.split('_')[1] == TYPEOFTERMINAL and\
                    terminal.split('_')[2] == APPOINMENT:
                conductor_section.append(terminal.split('_')[3])
        return sorted(list(set(conductor_section)),key = lambda x: float(x))
    else:
        return ['']


def define_name_of_terminal(name_from_qt:str):
    TYPEOFTERMINAL = 'SCREW' if name_from_qt.split('_')[1] == 'Винтовые' else 'SPRING'
    APPOINMENT = 'WHITE' if name_from_qt.split('_')[2] == 'L' else 'BLUE' if name_from_qt.split('_')[2] == 'N' else 'GREEN'
    return '_'.join([name_from_qt.split('_')[0],TYPEOFTERMINAL,APPOINMENT,name_from_qt.split('_')[3] ])


if __name__ == '__main__':
    print(define_type_of_terminal(names_of_terminal=define_names_terminal(),manufacturer='SUPU'))

