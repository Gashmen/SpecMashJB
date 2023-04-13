import ezdxf

def create_border_A3(doc,y_min_upside,x_min_rightside):
    block_border = doc.blocks['Border_A3']
    values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
    if doc.blocks.get('Border_A3'):
        border_insert = doc.modelspace().add_blockref(name='Border_A3',
                                                      insert=(x_min_rightside,y_min_upside))
        border_insert.add_auto_attribs(values)

        return border_insert





