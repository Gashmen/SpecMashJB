import ezdxf
import CONST

def add_attrib_in_block(block,blocks_attribs_insert):
    '''
    Вставка аттрибутов в блоки на нужные координаты
    :param block: class ezdxf.entities.Insert
    :param number: int
    :return: None
    '''
    for padd in blocks_attribs[block.dxf.name]:
        padd_attrib = block.add_attrib(padd.dxf.tag, f' ',
                                       insert=(block.dxf.insert[0] + blocks_attribs_insert[block.dxf.name][padd.dxf.tag][0],
                                       block.dxf.insert[1]+blocks_attribs_insert[block.dxf.name][padd.dxf.tag][1], 0),
                                       dxfattribs={'align_point': (block.dxf.insert[0] + blocks_attribs_insert[block.dxf.name][padd.dxf.tag][0],
                                        block.dxf.insert[1]+blocks_attribs_insert[block.dxf.name][padd.dxf.tag][1], 0)})
        for check in padd.dxfattribs().keys():
            if check != 'insert' and check != 'text' and check != 'tag' and check != 'owner' and check != 'handle' and check != 'align_point':
                padd_attrib.dxf.__dict__[check] = padd.dxf.__dict__[check]


if __name__ == '__main__':

        doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf')

        msp = doc.modelspace()
        msp.delete_all_entities()

        block_border = doc.blocks['Border_A3']
        border_attdef = [attdef for attdef in block_border.query('ATTDEF')]
        values = {attdef.dxf.tag:'07.2023' for attdef in border_attdef}

        insert_border = msp.add_blockref(name = 'Border_A3', insert=(100, -100))
        insert_border.add_auto_attribs(values)
        # for new_attrib in border_attdef:
        #     attrib_dxfattibs = {property_tag:property_value for property_tag,property_value in new_attrib.dxfattribs().items()
        #                            if property_tag != 'insert' and property_tag != 'text'
        #                                    and property_tag != 'tag' and property_tag != 'owner'
        #                                    and property_tag != 'handle' and property_tag != 'prompt'}
        #     tag = new_attrib.dxf.tag
        #     insert_attrib = new_attrib.dxf.insert
        #     align_attrib = new_attrib.dxf.align_point
        #     attrib_after_add = insert_border.add_attrib(tag=tag,
        #                                                  insert=(insert_border.dxf.insert[0] + insert_attrib[0],
        #                                                          insert_border.dxf.insert[1] + insert_attrib[1]),
        #                                                  dxfattribs=attrib_dxfattibs,
        #                                                  text ='07.202323232323')
        #     if align_attrib:
        #         attrib_after_add.dxf.align_point = (insert_border.dxf.insert[0] + align_attrib[0],
        #                                             insert_border.dxf.insert[1] + align_attrib[1])
        #     attrib_after_add.dxf.halign = 4
        #     attrib_after_add.dxf.valign = 2


        for attdef in block_border.query('ATTDEF'):
            print(attdef.dxfattribs())

        # print(block_border.query('ATTDEF')[0].dxf.insert)

        doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\xx_dimesion_test.dxf')

