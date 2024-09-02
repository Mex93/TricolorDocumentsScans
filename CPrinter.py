import clr
import sys


class CPrinter:
    def __init__(self, printer_name: str):
        self.__printer_name = printer_name
        # Добавьте путь к вашей DLL
        sys.path.append(r'LabelPrinterLibrary.dll')
        # Загрузите вашу DLL:
        clr.AddReference('LabelPrinterLibrary')

    def __print_label(self, barcode_text):
        from LabelPrinterLibrary import LabelPrinter
        result = LabelPrinter.PrintBarcode(self.__printer_name, barcode_text)
        return result

    def send_print_label(self, tricolor_key: str):
        if len(tricolor_key) > 0:
            with open('barcode_template.txt', 'r') as file:
                ezpl_data = file.read()
                ezpl_data = ezpl_data.replace("THIS_TEST", tricolor_key)

            # нельзя впереди этикетки что бы были пробелы!!!!!!
            # в документе должен быть пробел в самом конце после E

            self.__print_label(ezpl_data)
