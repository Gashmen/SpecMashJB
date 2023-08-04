import ezdxf
from src.dxf_creating import shell_create
def add_label_cut_on_topside(doc,shell_name:str,max_len_input:float,scale):
    '''
    Добавление обозначения сверху и снизу A->
    :param doc: документ self.doc_new
    :param shell_name: имя оболочки VP.161610
    :return:
    '''

    insert_topside = doc.modelspace().query(f'INSERT[name == "{shell_name}_topside"]')[0]
    topside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_topside)

    a = doc.modelspace().add_blockref(name='cut_name_top',
                                      insert=(insert_topside.dxf.insert[0],
                                              topside_extreme_lines['y_max'] + max_len_input))
    a.scale_uniform(1 / scale)
    a.dxf.insert = (insert_topside.dxf.insert[0],topside_extreme_lines['y_max'] + max_len_input)

    b = doc.modelspace().add_blockref(name='cut_name_bottom',
                                      insert=(insert_topside.dxf.insert[0],
                                              topside_extreme_lines['y_min'] - max_len_input))
    b.scale_uniform(1 / scale)
    b.dxf.insert = (insert_topside.dxf.insert[0], topside_extreme_lines['y_min'] - max_len_input)

def add_label_cut_on_cutside(doc,shell_name:str,max_len_input:float,scale):
    '''
    Добавление обозначения сверху A-A
    :param doc: документ self.doc_new
    :param shell_name: имя оболочки VP.161610
    :return:
    '''

    insert_cutside = doc.modelspace().query(f'INSERT[name == "{shell_name}_cutside"]')[0]
    cutside_extreme_lines = shell_create.define_extreme_lines_in_insert(insert_cutside)

    a = doc.modelspace().add_blockref(name='cut_name_main',
                                  insert=(cutside_extreme_lines['x_min'] + (cutside_extreme_lines['x_max'] - cutside_extreme_lines['x_min'])/2,
                                          cutside_extreme_lines['y_max'] + max_len_input))
    a.scale_uniform(1/scale)
    a.dxf.insert = (cutside_extreme_lines['x_min'] + (cutside_extreme_lines['x_max'] - cutside_extreme_lines['x_min'])/2,
                    cutside_extreme_lines['y_max'] + max_len_input)


def add_label_cut(doc,shell_name:str,max_len_input:float,scale):
    add_label_cut_on_topside(doc=doc,
                                 shell_name=shell_name,
                                 max_len_input=max_len_input,
                                 scale=scale)
    add_label_cut_on_cutside(doc=doc,
                             shell_name=shell_name,
                             max_len_input=max_len_input,
                             scale=scale)


