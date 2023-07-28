'''
Получение координат словарем self.dict_with_list_coordinates_on_side_for_dxf для построения в dxf
{'А': {0: {'ВЗ-Н25': [32.11666666666667, 37.5]}, 1: {'ВЗ-Н25': [87.88333333333333, 37.5]}},
'Б': {0: {'ВЗ-Н25': [24.783333333333335, 37.5]}, 1: {'ВЗ-Н25': [73.21666666666667, 37.5]}},
'В': {},
'Г': {},
'Крышка': {}}
'''
import signal
from typing import Optional

import ezdxf
from ezdxf.addons.drawing.qtviewer import CADGraphicsViewWithOverlay, CADWidget, CADViewer
from ezdxf.addons.xqt import QtCore as qc, QtGui as qg, QtWidgets as qw
from ezdxf.audit import Auditor
from ezdxf.document import Drawing
from ezdxf.entities import DXFGraphic


class ElementSelectorView(CADGraphicsViewWithOverlay):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = None

    def keyPressEvent(self, event: qg.QKeyEvent) -> None:
        if event.key() == qc.Qt.Key_Return:
            element = self.current_hovered_element
            if element is not None:
                self.selected = element
                self.close()


def select_element(doc: Drawing, layout: str = 'Model', show_controls: bool = False) -> Optional[DXFGraphic]:
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # handle Ctrl+C properly
    app = qw.QApplication.instance()
    if app is None:
        app = qw.QApplication([])

    view = ElementSelectorView()
    cad = CADWidget(view)
    if show_controls:
        viewer = CADViewer(cad=cad)
        view.closing.connect(viewer.close)
        viewer.set_document(doc, Auditor(doc), layout=layout)
        viewer.show()
    else:
        cad.set_document(doc, layout=layout)
        cad.show()
    app.exec()
    return view.selected


def main():
    doc = ezdxf.new()
    msp = doc.modelspace()
    doc.layers.add("MyLayer")
    doc.layers.add("OtherLayer")
    msp.add_line((0, 0), (1, 0), dxfattribs={"layer": "MyLayer"})
    msp.add_line((1, 0), (1, 1), dxfattribs={"layer": "OtherLayer"})

    selected_element = select_element(doc)
    print(f'element selected: {selected_element}')

    selected_element = select_element(doc, show_controls=True)
    print(f'element selected: {selected_element}')


if __name__ == '__main__':
    main()