import itertools

import ezdxf
'''Концепция заполнения имени оболочки: VP.110806_topside, где VP - ВП(пластиковая); 110806 - размеры; topside - сторона которая показывается'''
doc = ezdxf.readfile('ContainerVer02.dxf')

def create_tree_blocks(doc):
    tree_with_all_blocks = dict()
    for someblock in doc.blocks:
        if '*' not in someblock.dxf.name:
            inserts_in_someblock = dict() #{Имя инсерта: координаты его в блоке}
            for insert in someblock:
                if insert.dxftype() == 'INSERT':
                    inserts_in_someblock[insert.dxf.name] = insert.dxf.insert
            tree_with_all_blocks[someblock.dxf.name] = inserts_in_someblock
    '''itertools.chain разворачивает цепь полностью'''

    return tree_with_all_blocks


def check_insert_in_block(doc,dict_oldname_key_new_name_value:dict, dict_with_block_in_block_and_insert:dict):
    dict_oldname_key_new_name_value_copy = dict_oldname_key_new_name_value.copy()
    dict_with_block_in_block_and_insert_copy = dict_with_block_in_block_and_insert.copy()
    a = []
    b ={}
    while any(list(dict_with_block_in_block_and_insert_copy.values())):
        for old_name, new_name in dict_oldname_key_new_name_value_copy.items():
            if dict_with_block_in_block_and_insert_copy[old_name] != {}:
                for i in dict_with_block_in_block_and_insert_copy[old_name]:
                    dict_oldname_key_new_name_value_copy[i] = new_name + '' + i

def search_block_that_without_insert_and_rename(doc):
    oldname_newname = dict()
    dict_with_newname_old_coordinate = dict()
    list_checker = []
    for someblock in doc.blocks:
        if '*' not in someblock.dxf.name:
            list_checker.append(someblock.dxf.name)
    for block_name in list_checker:
        for insert in doc.blocks[block_name]:
            if insert.dxftype() == 'INSERT':
                if insert.dxf.name not in oldname_newname:
                    if 'U' == insert.dxf.name[0]:
                        oldname_newname[insert.dxf.name] = block_name + '_' + insert.dxf.name
                        dict_with_newname_old_coordinate[block_name + '_' + insert.dxf.name] = [block_name,insert.dxf.insert]

    for oldname in oldname_newname:
        doc.blocks.rename_block(oldname, oldname_newname[oldname])
        doc.blocks[dict_with_newname_old_coordinate[oldname_newname[oldname]][0]].add_blockref(oldname_newname[oldname],
                                                                                               insert=dict_with_newname_old_coordinate[oldname_newname[oldname]][1])


if __name__ == '__main__':
    tree_dict = create_tree_blocks(doc)
    print(search_block_that_without_insert_and_rename(doc))
    doc.saveas('checkcheck.dxf')