import clr
import sys
import os


class CPrinter:
    def __init__(self, printer_name: str):
        self.__printer_name = printer_name
        # Добавьте путь к вашей DLL
        sys.path.append(r'LabelPrinterLibrary.dll')
        # Загрузите вашу DLL:
        clr.AddReference('LabelPrinterLibrary')
        self.standart_ezpl = (""
                         "^Q8,3\n"
                         "^W48\n"
                         "^H10\n"
                         "^P1\n"
                         "^S2\n"
                         "^AT\n"
                         "^C1\n"
                         "^R0\n"
                         "~Q+0\n"
                         "^O0\n"
                         "^D0\n"
                         "^E18\n"
                         "~R255\n"
                         "^XSET,ROTATION,0\n"
                         "^L\n"
                         "Dy2-me-dd\n"
                         "Th:m:s\n"
                         "Y37,153,Image3-84\n"
                         "Y37,153,Image2-87\n"
                         "Y25,6,WindowText1-32\n"
                         "BQ,92,6,2,5,20,0,3,THIS_TEST\n"
                         "E\n")

    def __print_label(self, barcode_text):
        from LabelPrinterLibrary import LabelPrinter
        result = LabelPrinter.PrintBarcode(self.__printer_name, barcode_text)
        return result

    def send_print_label(self, tricolor_key: str):
        if len(tricolor_key) > 0:

            with open('barcode_template.txt', 'w+') as file:
                ezpl_data = file.read()
                if not len(ezpl_data):
                    file.write(self.standart_ezpl)
                    ezpl_data = self.standart_ezpl
                ezpl_data = ezpl_data.replace("THIS_TEST", tricolor_key)

            # нельзя впереди этикетки что бы были пробелы!!!!!!
            # в документе должен быть пробел в самом конце после E

            self.__print_label(ezpl_data)
