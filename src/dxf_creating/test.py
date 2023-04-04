import ezdxf



from PyPDF2 import PdfFileReader


# Открываем PDF файл в режиме чтения байтов
with open('C:\\Users\\g.zubkov\\Downloads\\Telegram Desktop\\Ex_ia_2.pdf', 'rb') as pdf_file:
    # Создаем объект PDFReader, чтобы читать PDF
    pdf_reader = PdfFileReader(pdf_file)

    # Получаем количество страниц в документе
    num_pages = pdf_reader.numPages

    # Цикл по страницам
    for page in range(num_pages):
        # Получаем объект страницы
        pdf_page = pdf_reader.getPage(page)

        # Получаем текст на странице и выводим его
        print(pdf_page.extractText())

# Закрываем файл
pdf_file.close()


