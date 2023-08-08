import ezdxf

def create_border_A3(doc,y_min_upside,x_min_rightside):
    '''
    Создает рамку А3 формата с аттрибутами сразу
    :param doc:
    :param y_min_upside:
    :param x_min_rightside:
    :return:
    '''
    block_border = doc.blocks['Border_A3']
    values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
    if doc.blocks.get('Border_A3'):
        border_insert = doc.modelspace().add_blockref(name='Border_A3',
                                                      insert=(x_min_rightside,y_min_upside))
        border_insert.add_auto_attribs(values)

        return border_insert

def write_RUTITLE_attrib(attrib_rutitle, rutitle_text:str):
    '''
    Заполнение аттрибута rutitle
    :param attrib_rutitle: В цикле проверки аттрибутов передается аттрибут
    :param rutitle_text: Значение str от rutitleLineEdit
    :return:
    '''
    if attrib_rutitle.dxf.tag == 'RUTITLE':
        if rutitle_text != None:
            if len(rutitle_text) <= 36:
                attrib_rutitle.dxf.text = rutitle_text
            else:
                attrib_rutitle.dxf.text = rutitle_text[:36]

def write_project_attrib(attrib_projecttitle, projecttitle_text:str):
    '''
    Заполнение аттрибута projecttitle 1 2 3
    :param attrib_projecttitle: В цикле проверки аттрибутов передается аттрибут
    :param rutitle_text: Значение str от projecttitleLineEdit
    :return:
    '''
    if len(projecttitle_text) <= 25:
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_2':
            attrib_projecttitle.dxf.text = projecttitle_text

    elif 26 <= len(projecttitle_text) <= 50:
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_2':
            attrib_projecttitle.dxf.text = projecttitle_text[:25]
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_3':
            attrib_projecttitle.dxf.text = projecttitle_text[25:]

    elif 51 <= len(projecttitle_text) <= 75:
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_1':
            attrib_projecttitle.dxf.text = projecttitle_text[:25]
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_2':
            attrib_projecttitle.dxf.text = projecttitle_text[25:50]
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_3':
            attrib_projecttitle.dxf.text = projecttitle_text[50:]

def write_company_attrib(attrib_company, companylineedit_text:str):
    '''
    Заполнение аттрибута Company
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_company.dxf.tag == 'COMPANY':
        if companylineedit_text != None:
            if len(companylineedit_text) <= 27:
                attrib_company.dxf.text = companylineedit_text
            else:
                attrib_company.dxf.text = companylineedit_text[:27]

def write_scale(attrib_scale, scale:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_scale.dxf.tag == 'SCALE':
        if scale != None:
                attrib_scale.dxf.text = scale

def write_rudes(attrib_rudes, rudes:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rudes.dxf.tag == 'RUDES':
        if rudes != None:
                attrib_rudes.dxf.text = rudes

def write_rudesdata(attrib_rudesdata, rudesdata:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rudesdata.dxf.tag == 'RUDESDATA':
        if rudesdata != None:
                attrib_rudesdata.dxf.text = rudesdata

def write_rudesdata(attrib_rudesdata, rudesdata:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rudesdata.dxf.tag == 'RUDESDATA':
        if rudesdata != None:
                attrib_rudesdata.dxf.text = rudesdata

def write_scale(attrib_SCALE, SCALE:float):
    '''
    Заполнение
    :param attrib_SCALE: В цикле проверки аттрибутов передается аттрибут
    :param SCALE: 2,2.5,4,....
    :return:
    '''
    if attrib_SCALE.dxf.tag == 'SCALE':
        if SCALE != None:
                attrib_SCALE.dxf.text = f'1:{SCALE}'

def write_page_number(attrib_RUSHEET, sheet_number = 1):
    '''Пишет номер страницы'''
    if attrib_RUSHEET.dxf.tag == 'RUSHEET':
        if sheet_number != None:
                attrib_RUSHEET.dxf.text = str(sheet_number)

def write_page_numbers(attrib_RUSHTS, sheet_count = 2):
    '''Пишет номер страницы'''
    if attrib_RUSHTS.dxf.tag == 'RUSHTS':
        if sheet_count != None:
                attrib_RUSHTS.dxf.text = str(sheet_count)
