from src.dxf_creating import shell_create


def define_inputs_on_topside(doc,shell_name:str):
    '''
    Ищем кабельные ввода вокруг topside
    :param doc: док после добавление кабельнных вводов
    :param shell_name:VP.161610
    :return:
    '''

    insert_topside = doc.modelspace().query(f'INSERT[name=="{shell_name}_topside"]')[0]
    extreme_lines_topside = shell_create.define_extreme_lines_in_insert(insert_topside)

    a_side_insert = list()
    b_side_insert = list()
    v_side_insert = list()
    g_side_insert = list()

    for insert_input in doc.modelspace().query('INSERT'):
        if list(insert_input.dxf.insert)[1] == extreme_lines_topside['y_max']:
            if extreme_lines_topside['x_min'] < list(insert_input.dxf.insert)[0] < extreme_lines_topside['x_max']:
                v_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[1] == extreme_lines_topside['y_min']:
            if extreme_lines_topside['x_min'] < list(insert_input.dxf.insert)[0] < extreme_lines_topside['x_max']:
                a_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[0] == extreme_lines_topside['x_min']:
            if extreme_lines_topside['y_min'] < list(insert_input.dxf.insert)[1] < extreme_lines_topside['y_max']:
                g_side_insert.append(insert_input)

        if list(insert_input.dxf.insert)[0] == extreme_lines_topside['x_max']:
            if extreme_lines_topside['y_min'] < list(insert_input.dxf.insert)[1] < extreme_lines_topside['y_max']:
                b_side_insert.append(insert_input)
    return {'A_SIDE': a_side_insert,'B_SIDE':b_side_insert,'V_SIDE':v_side_insert,'G_SIDE':g_side_insert}



if __name__ == '__main__':
    doc = 'C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx.dxf'
