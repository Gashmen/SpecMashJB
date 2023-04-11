import ezdxf
import CONST

doc = ezdxf.readfile('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\DXF_BASE.dxf')

coordinate_din_in_cutside = doc.blocks[f'VP.161610_cutside'].query('INSERT[name=="35_DIN_CUTSIDE"]')[0].dxf.insert

cutside_insert = doc.modelspace().add_blockref(name='VP.161610_cutside',
                              insert=(0,0))
cutside_insert.dxf.rotation = 270

doc.modelspace().add_blockref(name='SUPU_SCREW_BLUE_4_viewside',
                              insert=(
                                  cutside_insert.dxf.insert[0] + coordinate_din_in_cutside[1] + CONST.FROM_DIN_INSERT,
                                  cutside_insert.dxf.insert[1] - coordinate_din_in_cutside[0])
                              )
doc.modelspace().add_blockref(name = 'Terminal_end_stop_viewside',
                              insert=(cutside_insert.dxf.insert[0]+coordinate_din_in_cutside[1]+CONST.FROM_DIN_INSERT,
                                      cutside_insert.dxf.insert[1]-coordinate_din_in_cutside[0])
                              )


doc.saveas('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\test.dxf')
print(coordinate_din_in_cutside)