import ezdxf

import shell_create
def create_dim():
    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\marshallingboxes\\newnewnewn.dxf')
    msp = doc.modelspace()

    insert_downside = None
    for insert_entity in msp.query('INSERT'):
        if 'downside' in insert_entity.dxf.name:
            insert_downside = insert_entity

    insert_downside_coordinates = shell_create.define_extreme_lines_in_insert(insert_downside)

    dim = msp.add_linear_dim(
        base=(insert_downside_coordinates['x_0'][0],insert_downside_coordinates['y_max']+10),
        p1=(insert_downside_coordinates['x_min'],insert_downside_coordinates['y_max']),
        p2=(insert_downside_coordinates['x_max'],insert_downside_coordinates['y_max']),
        dimstyle= 'EZDXF'
    )

    dim.render()
    doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\marshallingboxes\\newnewnewn1.dxf')

import math

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



def calculate_horizontal_len_block(block):
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


def calculate_vertical_len_block(block):
    '''
    Считает вертикальную длину блока
    :param block:
    :return:
    '''
    dict_with_horizontal_lines = create_dict_with_horizontal_lines(block=block)
    vertical_len = abs(max(dict_with_horizontal_lines.keys()) - min(dict_with_horizontal_lines.keys()))
    return vertical_len


if __name__ == '__main__':
    doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx.dxf')
    msp = doc.modelspace()

    for block in doc.blocks:
        if '*' not in block.dxf.name and 'VZ-N' in block.dxf.name:
            print(block.dxf.name)
            print(calculate_horizontal_len_block(block))
            print(calculate_vertical_len_block(block=block))

