import ezdxf

def create_border_A3(doc,y_min_upside,x_min_rightside):
    if doc.blocks.get('Border_A3'):
        border_insert = doc.modelspace().add_blockref(name='Border_A3',
                                                      insert=(x_min_rightside,y_min_upside))
        return border_insert






