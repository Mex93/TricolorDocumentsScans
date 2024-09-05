import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QFontDatabase

import logging
import threading

from ui.untitled import Ui_MainWindow
from config_parser.CConfig import CConfig
from common import (send_message_box, SMBOX_ICON_TYPE, get_current_unix_time,
                    is_pattern_match, get_about_text, get_rules_text,
                    is_tricolor_text_valid, convert_date_from_sql_format_ex,
                    is_tv_sn_text_valid)
from enuuuums import INPUT_TYPE
from CPrinter import CPrinter

from sql.CSQLQuerys import CSQLQuerys, SQL_TV_MODELS_DATA
from sql.enums import CONNECT_DB_TYPE


# pyside6-uic .\ui\untitled.ui -o .\ui\untitled.py
# pyside6-rcc .\ui\res.qrc -o .\ui\res_rc.py
# Press the green button in the gutter to run the script.


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__base_program_version = "0.1"  # Менять при каждом обновлении любой из подпрограмм

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("designs/Iosevka Bold.ttf")
        self.setWindowTitle(f'Сканировка Tricolor 2024 v0.1b [Режим: привязка]')

        logging.basicConfig(level=logging.INFO, filename="key_logging.log", filemode="a",
                            format="%(asctime)s %(levelname)s %(message)s")

        self.cconfig = CConfig()
        self.anti_flood_print: int = 0
        self.tv_sn_template: str = ""

        # ---------------------------------------
        try:
            if self.cconfig.load_data() is False:
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text="Ошибка в файле конфигурации!\n"
                                      "Один или несколько параметров ошибочны!\n\n"
                                      "Позовите технолога!",
                                 title="Внимание!",
                                 variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
                return

            self.printer_name = self.cconfig.get_printer_name()
            self.assembled_line = self.cconfig.get_assembled_line()
            self.tricolor_template = self.cconfig.get_tricolor_template()
            self.info_mode = self.cconfig.get_info_mode()

        except Exception as err:
            send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                             text="Ошибка в файле конфигурации!\n"
                                  "Один или несколько параметров ошибочны!\n\n"
                                  "Позовите технолога!\n\n"
                                  f"Ошибка: '{err}'",
                             title="Внимание!",
                             variant_yes="Закрыть", variant_no="", callback=lambda: self.set_close())
            return
        if self.info_mode == 1:
            self.setWindowTitle(f'Сканировка Tricolor 2024 v0.1b [Режим: информация]')

        self.cframe = FlickerInterface(self)
        self.clabel = TextLabel(self)
        self.cinput = InputField(self)
        self.cprinter = CPrinter(self.printer_name)
        self.cmodel = TVmodels(self)

        self.set_default_program_data()

        self.ui.pushButton_print.clicked.connect(self.on_user_presed_on_print_btn)
        self.ui.pushButton_cancel.clicked.connect(self.on_user_presed_on_cancel_btn)
        self.ui.lineEdit_input.returnPressed.connect(self.on_user_text_input_field)
        self.ui.action_info.triggered.connect(self.on_user_pressed_info)
        self.ui.comboBox_model_name.activated.connect(self.on_user_clicked_on_model_change)

        self.set_block_interface()
        self.ui.lineEdit_input.setEnabled(False)
        self.load_models()

    def load_models(self):
        csql = CSQLQuerys()
        try:
            result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
            if result_connect is True:
                result = csql.load_tricolor_models()
                count = 0
                if result is not False:
                    for tv in result:
                        tv_name = tv.get(SQL_TV_MODELS_DATA.fd_tv_name, None)
                        tv_fk = tv.get(SQL_TV_MODELS_DATA.fd_tv_id, None)
                        tv_template = tv.get(SQL_TV_MODELS_DATA.fd_tv_serial_number_template, None)
                        if None in (tv_name, tv_fk, tv_template):
                            continue

                        self.cmodel.add_item_on_change(tv_fk, tv_name, tv_template)
                        count += 1

                if not count:
                    self.send_error_message(
                        "Во время выполнения программы произошла ошибка #3.\n"
                        "Обратитесь к системному администратору!\n\n"
                        f"Код ошибки: 'load_models -> [No Data]'")
                    return
                else:
                    self.ui.comboBox_model_name.setCurrentIndex(-1)

                    self.set_unblock_interface()
                    self.clabel.set_text("Программа успешно загружена!\nВыберите модель устройства:", "green", 4.0)

            else:
                raise ValueError("Нет подключения к БД!")

        except Exception as err:
            print(err)
            logging.critical(err)
            self.send_error_message(
                "Во время выполнения программы произошла ошибка #2.\n"
                "Обратитесь к системному администратору!\n\n"
                f"Код ошибки: 'load_models -> [{err}]'")
            return False
        finally:
            csql.disconnect_from_db()

    def on_user_clicked_on_model_change(self):
        text = self.ui.comboBox_model_name.currentText()
        if text:
            tv_fk = self.cmodel.get_item_from_tv_name(text)
            if tv_fk != -1:
                self.cmodel.set_changed_model(tv_fk)
                self.set_unblock_interface()
                self.ui.comboBox_model_name.setEnabled(False)
                self.ui.lineEdit_input.setEnabled(True)
                return

        self.send_error_message(
            "Во время выполнения программы произошла ошибка #4.\n"
            "Обратитесь к системному администратору!\n\n"
            f"Код ошибки: 'on_user_clicked_on_model_change -> [Not find changed models]'")

    @staticmethod
    def on_user_pressed_info():
        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_INFO,
                         text=f"{get_about_text()}"
                              f"\n"
                              f"\n"
                              f"{get_rules_text()}",
                         title="О программе",
                         variant_yes="Закрыть", variant_no="")

    def on_clear_input_callback(self):
        self.cinput.clear_field()

    def set_update_models(self):
        csql = CSQLQuerys()
        try:
            result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
            if result_connect is True:
                tv_fk = self.cmodel.get_model_fk_changed()
                result = csql.update_current_tricolor_models(tv_fk)
                if result is not False:
                    tv_fk, tv_name, tv_template = result
                    tv_fk = self.cmodel.get_item_from_tv_name(tv_name)
                    if tv_fk != -1:
                        if (tv_name == self.cmodel.get_model_name_changed() and
                                tv_template == self.cmodel.get_model_template()):
                            return True
                        else:
                            raise ValueError("Модель не найдена!")
                    else:
                        raise ValueError("Модель не найдена!")
                else:
                    raise ValueError("Модель не найдена!")
            else:
                raise ValueError("Нет подключения к БД!")

        except Exception as err:
            print(err)
            logging.critical(err)
            self.send_error_message(
                "Во время выполнения программы произошла ошибка #666.\n"
                "Обратитесь к системному администратору!\n\n"
                f"Код ошибки: 'set_update_models -> [{err}]'")
            return False
        finally:
            csql.disconnect_from_db()

    def on_user_text_input_field(self):

        if not self.cmodel.is_model_changed():
            return

        input_text = self.cinput.get_current_value()
        self.cinput.clear_field()
        input_text = input_text.upper().replace(" ", "")

        self.clabel.clear_text()
        self.clabel.clear_device_text()
        self.clabel.clear_tricolor_text()
        self.clabel.clear_model_text()
        self.cframe.stop_flick()

        if len(input_text) > 5:
            if not is_tv_sn_text_valid(input_text) and not is_tricolor_text_valid(input_text):
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_WARNING,
                                 text=f"В вводимой информации обнаружены недопустимые символы!",
                                 title="Внимание!",
                                 variant_yes="Закрыть", variant_no="", callback=None)
                return
            if not self.set_update_models():
                return

            tv_tempate = self.cmodel.get_model_template()
            # Пикнут и подошло по шаблону триколора

            input_type = INPUT_TYPE.NONE
            if is_pattern_match(self.tricolor_template, input_text):
                input_type = INPUT_TYPE.TRICOLOR_ID
            elif is_pattern_match(tv_tempate, input_text):  # если телевизор
                input_type = INPUT_TYPE.TV_SN

            if input_type == INPUT_TYPE.NONE:
                send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                                 text=f"Указанные данные '{input_text}' не подходят ни к одному шаблону!\n\n"
                                      f"Возможно модель выбрана неверно!!!",
                                 title="Ошибка ввода данных",
                                 variant_yes="Ок", variant_no="", callback=None)
                return
            pmodel_id = self.cmodel.get_model_fk_changed()
            csql = CSQLQuerys()
            try:
                # Этот код полностью проверит есть ли в какой либо таблице этот ключ
                result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
                if result_connect is True:
                    csql = CSQLQuerys()
                    try:

                        # Этот код полностью проверит есть ли в какой либо таблице этот ключ
                        result_connect = csql.connect_to_db(CONNECT_DB_TYPE.LINE)
                        if result_connect is True:

                            result = csql.get_assembled_tv_from_tricolor_key(input_type, input_text)
                            if result is not False:
                                tv_sn, tv_fk, tricolor_key, date = result

                                if tricolor_key is not None:
                                    tricolor_key = tricolor_key.upper()
                                if tv_sn is not None:
                                    tv_sn = tv_sn.upper()

                                is_find = False
                                if input_type == INPUT_TYPE.TRICOLOR_ID:
                                    is_find = True
                                elif input_type == INPUT_TYPE.TV_SN:
                                    if tricolor_key is not None:
                                        is_find = True
                                if is_find:
                                    tv_name = self.get_current_tv_name_from_tv_model(tv_fk, csql)

                                    if input_type == INPUT_TYPE.TRICOLOR_ID:
                                        self.clabel.set_text(f"Указанный ключ Tricolor ID '{tricolor_key}' найден\n"
                                                             f"в устройстве под SN '{tv_sn}''{tv_name}'[{tv_fk}]\n"
                                                             f"Date: {convert_date_from_sql_format_ex(str(date))}",
                                                             "red", 30.0)
                                    elif input_type == INPUT_TYPE.TV_SN:
                                        self.clabel.set_text(f"Ключ Tricolor ID '{tricolor_key}' найден\n"
                                                             f"в устройстве под SN '{tv_sn}''{tv_name}'[{tv_fk}]\n"
                                                             f"Date: {convert_date_from_sql_format_ex(str(date))}",
                                                             "red", 30.0)

                                    self.clabel.set_tricolor_text(tricolor_key)
                                    self.clabel.set_model_text(f"{tv_name}[{tv_fk}]")
                                    self.clabel.set_device_sn(tv_sn)
                                    self.cframe.set_flick(5)
                                    return

                            result = csql.get_tricolor_key_data_in_history_base(input_type, input_text)
                            if result is not False:  # дубляж assembled table, так как ещё таблица хистори
                                tv_sn, tv_fk, tricolor_id, assembled_line, attached_date, create_date = result

                                if tricolor_id is not None:
                                    tricolor_id = tricolor_id.upper()
                                if tv_sn is not None:
                                    tv_sn = tv_sn.upper()

                                is_find = False
                                if input_type == INPUT_TYPE.TRICOLOR_ID:
                                    is_find = True
                                elif input_type == INPUT_TYPE.TV_SN:
                                    if tricolor_id is not None:
                                        is_find = True
                                if is_find is True:
                                    tv_name = self.get_current_tv_name_from_tv_model(tv_fk, csql)

                                    if input_type == INPUT_TYPE.TRICOLOR_ID:
                                        self.clabel.set_text(
                                            f"Указанный ключ Tricolor ID '{tricolor_id}' уже был привязан\n"
                                            f"к устройству: '{tv_name}[{tv_fk}] {tv_sn}'\n"
                                            f"[Линия: {assembled_line}, A:{convert_date_from_sql_format_ex(str(attached_date))}-C:{convert_date_from_sql_format_ex(str(create_date))}]!"
                                            , "red", 10.0)
                                    elif input_type == INPUT_TYPE.TV_SN:
                                        self.clabel.set_text(
                                            f"Ключ Tricolor ID '{tricolor_id}' уже был привязан\n"
                                            f"к устройству: '{tv_name}[{tv_fk}] {tv_sn}'\n"
                                            f"[Линия: {assembled_line}, A:{convert_date_from_sql_format_ex(str(attached_date))}-C:{convert_date_from_sql_format_ex(str(create_date))}]!"
                                            , "red", 10.0)

                                    self.clabel.set_model_text(f"{tv_name}[{tv_fk}]")
                                    self.clabel.set_tricolor_text(tricolor_id)
                                    self.clabel.set_device_sn(tv_sn)
                                    self.cframe.set_flick(5)

                                    return

                            result = csql.get_tricolor_key_data_in_process_base(input_type, input_text)
                            if result is not False:
                                tv_sn, tv_fk, tricolor_id, assembled_line, attached_date, create_date = result

                                if tricolor_id is not None:
                                    tricolor_id = tricolor_id.upper()
                                if tv_sn is not None:
                                    tv_sn = tv_sn.upper()

                                is_find = False
                                if input_type == INPUT_TYPE.TRICOLOR_ID:
                                    is_find = True
                                elif input_type == INPUT_TYPE.TV_SN:
                                    if tricolor_id is not None:
                                        is_find = True
                                if is_find is True:
                                    tv_name = self.get_current_tv_name_from_tv_model(tv_fk, csql)

                                    if input_type == INPUT_TYPE.TRICOLOR_ID:
                                        self.clabel.set_text(f"Указанный ключ Tricolor ID '{tricolor_id}' в процессе\n"
                                                             f"привязки к устройству: '{tv_name}[{tv_fk}] {tv_sn}'\n"
                                                             f"[Линия: {assembled_line}, A:{convert_date_from_sql_format_ex(str(attached_date))}-C:{convert_date_from_sql_format_ex(str(create_date))}]!"
                                                             , "blue", 10.0)
                                    elif input_type == INPUT_TYPE.TV_SN:
                                        self.clabel.set_text(f"Ключ Tricolor ID '{tricolor_id}' в процессе\n"
                                                             f"привязки к устройству: '{tv_name}[{tv_fk}] {tv_sn}'\n"
                                                             f"[Линия: {assembled_line}, A:{convert_date_from_sql_format_ex(str(attached_date))}-C:{convert_date_from_sql_format_ex(str(create_date))}]!"
                                                             , "blue", 10.0)

                                    self.clabel.set_model_text(f"{tv_name}[{tv_fk}]")
                                    self.clabel.set_tricolor_text(tricolor_id)
                                    self.clabel.set_device_sn(tv_sn)
                                    self.cframe.set_flick(5)
                                    return

                            if input_type == INPUT_TYPE.TRICOLOR_ID:
                                result = csql.get_tricolor_key_data_in_key_base(input_text)
                                if result is not False:
                                    self.clabel.set_text(f"Указанный ключ Tricolor ID '{input_text}' свободен!"
                                                         , "green", 10.0)

                                    return
                                else:
                                    self.clabel.set_text(
                                        f"Указанный ключ Tricolor ID '{input_text}' не обнаружен в базе ключей!\n"
                                        f"Он не привязан ни к устройству, ни к базе истории ключей!"
                                        , "red", 10.0)

                                    return
                            elif input_type == INPUT_TYPE.TV_SN:

                                if self.info_mode == 1:
                                    self.clabel.set_text(
                                        f"Для указанного SN: '{input_text}' не обнажен ключ!\n"
                                        f"Ключ не привязан ни к устройству, ни к базе истории ключей!"
                                        , "red", 10.0)
                                    return

                                result = self.check_correct_data_in_models_table(pmodel_id, csql)
                                if result[0] == 0:  # ошибок нет
                                    result = csql.get_tricolor_empty_key_from_key_base(pmodel_id)
                                    if result is not False:  # свободный ключ найден
                                        tv_fk, tricolor_key, load_date = result

                                        if tricolor_key is not None:
                                            tricolor_key = tricolor_key.upper()

                                        handle = csql.get_sql_handle()
                                        result_s = False
                                        try:
                                            is_success_insert_in_key_process = (
                                                csql.insert_key_in_attached_base(tv_fk,
                                                                                 input_text,
                                                                                 tricolor_key,
                                                                                 self.assembled_line,
                                                                                 load_date))
                                            is_success_delete_from_key_base = csql.delete_key_from_key_base(
                                                tv_fk,
                                                tricolor_key)

                                            if is_success_delete_from_key_base and is_success_insert_in_key_process:
                                                result_s = True

                                            else:
                                                raise ValueError("Error in create table")
                                        except:
                                            handle.rollback()
                                        else:
                                            handle.commit()

                                        if result_s is False:
                                            self.send_error_message(
                                                "Во время выполнения программы произошла ошибка #7.\n"
                                                "Обратитесь к системному администратору!\n\n"
                                                f"Код ошибки: 'Привязка ключа в process key base -> [{tv_fk,
                                                input_text,
                                                tricolor_key,
                                                self.assembled_line,
                                                convert_date_from_sql_format_ex(str(load_date))}]'")
                                            return
                                        # привязка
                                        tv_name = self.cmodel.get_model_name_changed()

                                        self.clabel.set_text(
                                            f"Ключ Tricolor ID '{tricolor_key}' успешно привязан к устройству\n"
                                            f"'{tv_name}[{tv_fk}] {input_text}' Линия: {self.assembled_line}!"
                                            , "green", 10.0)

                                        self.clabel.set_model_text(f"{tv_name}[{tv_fk}]")
                                        self.clabel.set_tricolor_text(tricolor_key)
                                        self.clabel.set_device_sn(input_text)
                                        self.cprinter.send_print_label(tricolor_key)
                                        self.cframe.set_flick(3, "green")

                                        logging.info(f"Ключ Tricolor ID '{tricolor_key}' успешно привязан к устройству "
                                                     f"'{tv_name}[{tv_fk}] {input_text}' [Линия: {self.assembled_line}]\n"
                                                     f"P[{self.printer_name}][{self.tricolor_template}]")
                                        return

                                    else:
                                        tv_name = self.cmodel.get_model_name_changed()

                                        self.clabel.set_text(f"Для указанной модели\n"
                                                             f"'{tv_name}'[{pmodel_id}]'\n"
                                                             f"нет свободных ключей в базе данных!\n"
                                                             , "red", 10.0)

                                        self.cframe.set_flick(4)
                                        return

                                else:
                                    _, error_text = result
                                    self.clabel.set_text(error_text, "red", 400.0)

                                    return False
                        else:
                            raise ValueError("Нет подключения к БД!")

                    except Exception as err:
                        print(err)
                        logging.critical(err)
                        self.send_error_message(
                            "Во время выполнения программы произошла ошибка #1.\n"
                            "Обратитесь к системному администратору!\n\n"
                            f"Код ошибки: 'on_user_text_input_field -> [{err}]'")
                        return
                    finally:
                        csql.disconnect_from_db()
                else:
                    raise ValueError("Нет подключения к БД!")

            except Exception as err:
                print(err)
                logging.critical(err)
                self.send_error_message(
                    "Во время выполнения программы произошла ошибка #1.\n"
                    "Обратитесь к системному администратору!\n\n"
                    f"Код ошибки: 'on_user_text_input_field -> [{err}]'")
                return
            finally:
                csql.disconnect_from_db()
        else:
            self.clabel.set_text("SN должен быть более 5 символов!", "red", 2.0)

    @staticmethod
    def get_current_tv_name_from_tv_model(tv_fk: int, sql_unit: CSQLQuerys) -> str:
        tv_name = "-"
        result = sql_unit.get_tv_model_data(tv_fk)
        if result is not False:
            _, tv_name, _ = result
        return tv_name

    @staticmethod
    def check_correct_data_in_models_table(tv_fk: int, sql_unit: CSQLQuerys) -> tuple:

        result = sql_unit.get_tv_model_data(tv_fk)
        error_id = 0
        error_text = ""
        if not result:
            error_id = 3
            error_text = "Отсутствует указанная модель в таблице с моделямии устройств!"
        template, name, tricolor = result
        if not error_id:
            if not tricolor:
                error_id = 4
                error_text = "Указанный номер модели не является Tricolor TV!"

        if not error_id:
            if not len(name) or not len(template):
                error_id = 5
                error_text = "Указанный номер модели ошибочно внесён в таблицу моделей(Шаблон или название пусты)!"

        if error_id > 0:
            mess_text = (f"Во время выполнения проверки конфигурации возникла ошибка #{error_id}.\n"
                         f"{error_text}\n"
                         f"Код ошибки: 'check_device_model_data -> [Error Data]'")

            rtuple = (error_id, mess_text)
            return rtuple
        rtuple = (error_id, template, name, tricolor)
        return rtuple

    def on_user_presed_on_print_btn(self):
        tricolor_text = self.clabel.get_tricolor_text()
        tvsn_text = self.clabel.get_device_sn_text()
        if len(tricolor_text) > 0 and len(tvsn_text) > 0:
            utime = get_current_unix_time()
            if self.anti_flood_print < utime:
                new_tricolor_text = tricolor_text.replace("Tricolor ID: ", "")
                self.cprinter.send_print_label(new_tricolor_text)

                tv_name = self.cmodel.get_model_name_changed()
                tv_fk = self.cmodel.get_model_fk_changed()
                tv_sn = tvsn_text.replace("Model Name: ", "")

                logging.info(f"Оператор распечатал ключ Tricolor ID '{new_tricolor_text}' "
                             f"'{tv_name}[{tv_fk}] {tv_sn}'\n"
                             f"P[{self.printer_name}][{self.assembled_line}][{self.tricolor_template}]")

                self.clabel.set_text(f"Этикетка '{tricolor_text}' для '{tvsn_text}' распечатана!", "green", 5.0)
                self.anti_flood_print = utime + 2
            else:
                self.clabel.set_text("Не флудите печатью!", "red", 2.0)
        else:
            self.clabel.set_text("Печатать нечего!", "red", 2.0)

    def on_user_presed_on_cancel_btn(self):
        self.set_default_program_data()
        self.clabel.set_text("Меню обнулено", "none", 2.0)

    def set_default_program_data(self):
        self.cframe.stop_flick()
        self.clabel.clear_text()
        self.clabel.clear_device_text()
        self.clabel.clear_tricolor_text()
        self.clabel.clear_model_text()
        self.cinput.clear_field()

        # self.cprinter.send_print_label("irewhgrwihjg")

    def closeEvent(self, event):
        # с таймерами
        self.cframe.stop_flick()
        self.clabel.clear_text()

    def set_close(self):
        self.cframe.stop_flick()
        self.clabel.clear_text()
        sys.exit()

    def send_error_message(self, text: str):
        self.set_block_interface()

        send_message_box(icon_style=SMBOX_ICON_TYPE.ICON_ERROR,
                         text=text,
                         title="Фатальная ошибка",
                         variant_yes="Закрыть программу", variant_no="", callback=lambda: self.set_close())

    def set_block_interface(self):
        self.ui.frame_main.setEnabled(False)

    def set_unblock_interface(self):
        self.ui.frame_main.setEnabled(True)


class InputField:
    def __init__(self, main_window: MainWindow):
        self.__main_window = main_window

    def get_current_value(self) -> str:
        return self.__main_window.ui.lineEdit_input.text()

    def set_current_value(self, text: str) -> None:
        self.__main_window.ui.lineEdit_input.setText(text)

    def clear_field(self):
        self.set_current_value("")


class TextLabel:
    def __init__(self, main_window: MainWindow):
        self.__main_window = main_window
        self.__timer_id: threading.Timer | int = -1
        self.__tricolor_field_used = False
        self.__tvsn_field_used = False
        self.__tvmodel_field_used = False

    def set_tricolor_text(self, text: str):
        self.__main_window.ui.label_tricolor_id.setText(f"Tricolor ID: {text}")
        self.__tricolor_field_used = True

    def clear_tricolor_text(self):
        self.set_tricolor_text("")
        self.__tricolor_field_used = False

    def set_model_text(self, text: str):
        self.__main_window.ui.label_tv_model.setText(f"Model Name: {text}")
        self.__tvmodel_field_used = True

    def clear_model_text(self):
        self.set_model_text("")
        self.__tvmodel_field_used = False

    def set_device_sn(self, text: str):
        self.__main_window.ui.label_tv_sn.setText(f"TV SN: {text}")
        self.__tvsn_field_used = True

    def clear_device_text(self):
        self.set_device_sn("")
        self.__tvsn_field_used = False

    def get_device_sn_text(self) -> str:
        if not self.__tvsn_field_used:
            return ""
        return self.__main_window.ui.label_tv_sn.text()

    def get_model_name_text(self) -> str:
        if not self.__tvmodel_field_used:
            return ""
        return self.__main_window.ui.label_tv_model.text()

    def get_tricolor_text(self) -> str:
        if not self.__tricolor_field_used:
            return ""
        return self.__main_window.ui.label_tricolor_id.text()

    def set_text(self, text: str, color: str, timer: float):
        if self.__timer_id != -1:
            if threading.Timer.is_alive(self.__timer_id):
                self.__timer_id.cancel()
        # green
        # red
        self.__main_window.ui.label_message.setText(text)
        if color == "green":
            self.__main_window.ui.label_message.setStyleSheet(u"color:green")
        elif color == "red":
            self.__main_window.ui.label_message.setStyleSheet(u"color:red")
        elif color == "yellow":
            self.__main_window.ui.label_message.setStyleSheet(u"color:yellow")
        elif color == "blue":
            self.__main_window.ui.label_message.setStyleSheet(u"color:blue")
        else:
            self.__main_window.ui.label_message.setStyleSheet(u"color:none")
        self.__timer_id = threading.Timer(timer, self.__on_stop_timer)
        self.__timer_id.start()

    def clear_text(self):
        if self.__timer_id != -1:
            if threading.Timer.is_alive(self.__timer_id):
                self.__timer_id.cancel()
            self.__on_stop_timer()
        self.__main_window.ui.label_message.setText("")
        self.__main_window.ui.label_message.setStyleSheet(u"background-color:none")

    def __on_stop_timer(self):
        self.__timer_id = -1
        self.__main_window.ui.label_message.setText("")
        self.__main_window.ui.label_message.setStyleSheet(u"background-color:none")


class FlickerInterface:
    def __init__(self, main_window: MainWindow):
        self.__main_window = main_window
        self.__timer_id: threading.Timer | int = -1
        self.__flick_state = False
        self.__flick_start = False
        self.__color: str = ""
        self.__flick_timer_count = 0

    def stop_flick(self):
        if self.__flick_start:
            if self.__timer_id != -1:
                if threading.Timer.is_alive(self.__timer_id):
                    self.__timer_id.cancel()
        self.__set_default()

    def __set_default(self):
        self.__flick_start = False
        self.__timer_id = -1
        self.__flick_state = False
        self.__color = ""
        self.__flick_timer_count = 0
        self.__main_window.ui.frame_main.setStyleSheet(u"background-color:none")

    def is_flick(self) -> bool:
        if self.__flick_start:
            return True

    def set_flick(self, timer: int, color: str = "red"):
        if self.__timer_id != -1:
            if threading.Timer.is_alive(self.__timer_id):
                self.__timer_id.cancel()
            self.__set_default()

        self.__color = color
        self.__flick_start = True
        self.__flick_state = False
        self.__flick_timer_count = timer
        self.__start_timer()

    def __on_change_new_state(self):
        if self.__flick_start:
            self.__flick_state = not self.__flick_state
            if self.__flick_state:
                self.__main_window.ui.frame_main.setStyleSheet(f"background-color:{self.__color}")
            else:
                self.__main_window.ui.frame_main.setStyleSheet(f"background-color:none")
            self.__flick_timer_count -= 1

            if self.__flick_timer_count <= 0:
                self.stop_flick()
            else:
                self.__start_timer()

    def __start_timer(self):
        self.__timer_id = threading.Timer(1.0, self.__on_change_new_state)
        self.__timer_id.start()


class TVmodels:
    def __init__(self, main_menu: MainWindow):
        self.__main_menu = main_menu
        self.__tv_list = list()
        self.__current_model_fk = 0
        self.__current_model_name = ""
        self.__current_model_template = ""
        self.__list_max_index = 0
        self.__reset_changed_model()

    def add_item_on_change(self, tv_fk: int, tv_name: str, tv_template: str):

        mm = self.__main_menu.ui
        mm.comboBox_model_name.addItem(tv_name)
        mm.comboBox_model_name.setItemText(self.__list_max_index, tv_name)

        self.__list_max_index += 1
        self.__tv_list.append([tv_fk, tv_name, tv_template])

    def get_item_index_from_tv_fk(self, tv_fk: int) -> int:
        for index, item in enumerate(self.__tv_list):
            if item[0] == tv_fk:
                return index
        return -1

    def get_item_from_tv_name(self, tv_name: str) -> int:
        for index, item in enumerate(self.__tv_list):
            if item[1] == tv_name:
                return item[0]
        return 0

    def set_changed_model(self, tv_fk: int) -> bool:
        index = self.get_item_index_from_tv_fk(tv_fk)
        if index != -1:
            model_name = self.__tv_list[index][1]
            self.set_changed_model_ex(index, tv_fk, model_name, self.__tv_list[index][2])

            return True

    def set_changed_model_ex(self, index: int, tv_fk: int, tv_name: str, tv_template: str) -> bool:
        self.__tv_list[index][0] = tv_fk
        self.__tv_list[index][1] = tv_name
        self.__tv_list[index][2] = tv_template
        self.__current_model_fk = tv_fk
        model_name = tv_name
        self.__current_model_name = model_name
        self.__current_model_template = tv_template
        return True

    def __reset_changed_model(self) -> None:
        self.__current_model_fk = 0
        self.__current_model_name = ""
        self.__current_model_template = ""

    def is_model_changed(self) -> bool:
        if self.__current_model_fk == 0:
            return False
        else:
            return True

    def get_model_template(self) -> str:
        return self.__current_model_template

    def get_model_fk_changed(self) -> int:
        return self.__current_model_fk

    def get_model_name_changed(self) -> str:
        return self.__current_model_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
