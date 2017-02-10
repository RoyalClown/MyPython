import os
from PyPDF2.pdf import PdfFileReader, PdfFileWriter


class FileSave:
    def __init__(self, contents):
        self.contents = contents

    def txt_save(self, path='./test.txt'):
        with open(path, 'w') as f:
            f.write(self.contents)

    # 复制pdf，除去最后一页
    def createNewBooks(self, pdf_file, output_file, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        input_stream = open(pdf_file, 'rb')

        pdf_input = PdfFileReader(input_stream)
        pdf_output = PdfFileWriter()

        page = 0
        pages = pdf_input.getNumPages() - 1

        while page < pages:
            pdf_output.addPage(pdf_input.getPage(page))
            page += 1

        outputfilename = output_dir + '/' + output_file
        output_stream = open(outputfilename, 'wb')
        pdf_output.write(output_stream)
        output_stream.close()
        input_stream.close()


if __name__ == '__main__':
    createNewBooks("C:\\Users\\RoyalClown\\Downloads\\1.pdf", "1_copy.pdf", "C:\\Users\\RoyalClown\\Downloads")

if __name__ == "__main__":
    filesave = FileSave('yerw')
    filesave.txt_save()
