import ezdxf
'''Заменить в случае отсутствия файла'''

PATH_TO_DIN_REYKA_BLOCK = 'C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Оболочка\ContainerVer02.dxf'

PATH_TO_TERMINAL = 'C:\\Users\g.zubkov\PycharmProjects\marshallingboxes\Клеммы\checkcheck.dxf'

LIST_WITH_TERMINALS_NAME = ['SUPU_SCREW_GREEN_16','SUPU_SCREW_WHITE_6']

def create_dict_with_horizontal_lines(block):
    ''' Сначала создаем словарь в котором находится координата y горизантольных линий(ключ) и
        линии на этой координате(значения) в списке. '''
    dict_with_horizontal_lines = dict()
    for entity in block.entity_space:
        if entity.dxftype() == 'LINE':
            if round(entity.dxf.start[1], 2) == round(entity.dxf.end[1],2):
                if round(entity.dxf.start[1], 2) not in dict_with_horizontal_lines:
                    dict_with_horizontal_lines[round(entity.dxf.start[1], 2)] = [entity]
                else:
                    dict_with_horizontal_lines[round(entity.dxf.start[1], 2)].append(entity)
    return dict_with_horizontal_lines

def calculate_terminal_len(block):
    '''
    :param dict_with_horizontal_lines: словарь с линиями полученные после create_dict_with_horizontal
    :return:
    '''
    dict_with_horizontal_lines = create_dict_with_horizontal_lines(block)
    max_sum = []
    for y_coordinate in dict_with_horizontal_lines:
        sum_of_all_lines_in_this_y = 0

        min_x_coord_on_this_horizontal_level_iteration = None
        max_x_coord_on_this_horizontal_level_iteration = None
        '''Найдем самую минимальную координату на этих отрезках и самую максимальную'''

        for line in dict_with_horizontal_lines[y_coordinate]:

            sum_of_all_lines_in_this_y += abs(round(line.dxf.end[0] - line.dxf.start[0], 2))
            if min_x_coord_on_this_horizontal_level_iteration == None and \
                    max_x_coord_on_this_horizontal_level_iteration == None:
                min_x_coord_on_this_horizontal_level_iteration = min(round(line.dxf.end[0], 2),
                                                                     round(line.dxf.start[0], 2))
                max_x_coord_on_this_horizontal_level_iteration = max(round(line.dxf.end[0], 2),
                                                                     round(line.dxf.start[0], 2))

            else:
                min_x_coord_on_this_horizontal_level_iteration = \
                    min(min_x_coord_on_this_horizontal_level_iteration,
                        min(round(line.dxf.end[0], 2), round(line.dxf.start[0], 2)))
                max_x_coord_on_this_horizontal_level_iteration = \
                    max(max_x_coord_on_this_horizontal_level_iteration,
                        max(round(line.dxf.end[0], 2), round(line.dxf.start[0], 2)))

        max_sum.append(max_x_coord_on_this_horizontal_level_iteration - min_x_coord_on_this_horizontal_level_iteration)
    return round(max(max_sum),2)

if __name__ == '__main__':
    doc_din = ezdxf.readfile(PATH_TO_DIN_REYKA_BLOCK)
    doc_terminal = ezdxf.readfile(PATH_TO_TERMINAL)
    DIN_REYKA_LEN = None
    SUMMARY_LEN_TERMINALS = None
    for block in doc_din.blocks:
        if 'din' in block.dxf.name.lower() and 'mainpart' in block.dxf.name.lower():
            DIN_REYKA_LEN = calculate_terminal_len(block = block)
    for terminal_name in LIST_WITH_TERMINALS_NAME:
        terminal_block = doc_terminal.blocks[terminal_name]
        terminal_len = calculate_terminal_len(block = terminal_block)
        if SUMMARY_LEN_TERMINALS is None:
            SUMMARY_LEN_TERMINALS = terminal_len
        else:
            SUMMARY_LEN_TERMINALS += terminal_len









