import openpyxl

wb = openpyxl.load_workbook('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\naming_base.xlsx')
ws = wb.active

for cell in ws['A']:
    if cell.value != None:
        if '.' in cell.value and '-' not in cell.value and '_' not in cell.value:
            cell.value = cell.value + '_topside'
        if '.' not in cell.value and '-' in cell.value and '_' not in cell.value:
            cell.value = cell.value + '_withoutcap'
wb.save('C:\\Users\\g.zubkov\\PycharmProjects\\FinalProject\\src\\dxf_base\\naming_base1.xlsx')
