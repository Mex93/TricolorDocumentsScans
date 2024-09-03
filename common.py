from datetime import datetime
import re
from PySide6.QtWidgets import QMessageBox
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize

from enuuuums import SMBOX_ICON_TYPE

INFO_CURRENT_ADMIN_EMAIL = "ryazanov.n@tvkvant.ru"


def get_rules_text() -> str:
    return (
        "Приведённые правила использования программы обязательны к соблюдению всем пользователям.\n\n"
        "Перечень:\n"
        "1) Разглашение данных предоставляемых программой сторонним лицам, не имеющим отношения к 'ООО Квант', "
        "строго запрещено!\n"
        "2) Попытка декомпиляции и любое вредительство внутри рабочей директории программы строго "
        "запрещено и снимает с разработчика ответственность за возможный ущерб.\n"
        # "3) Перед использованием программы пользователь должен быть ознакомлен с инструкцией.\n"
        "3) Для корректной работы программы пользователь должен указывать корректные данные в формы для заполнения.\n"
        "4) Разработчик имеет право вносить любые изменения в программу и документацию без уведомления пользователей.\n"
        "5) Невыполнение любого из пунктов правил влечёт нарушение пользователем своих обязательств."
    )


def get_about_text() -> str:
    current_year = datetime.now().year
    return ("Программа для сканировки Tricolor ID.\n\n"
            "Все права принадлежат ООО 'Квант'.\n\n"
            "Разработчик: Рязанов Н.В.\n"
            f"По всем интересующим вопросам и пожеланиям обращайтесь на почту {INFO_CURRENT_ADMIN_EMAIL}\n\n"
            f"\t\t\t{current_year} г.")


def get_instruction_text() -> str:
    return (
        "\n\n"
    )


def send_message_box(icon_style, text: str, title: str, variant_yes: str, variant_no: str, callback=None):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    match icon_style:
        case _, SMBOX_ICON_TYPE.ICON_NONE:
            msg.setIcon(QMessageBox.Icon.NoIcon)
        case SMBOX_ICON_TYPE.ICON_ERROR:
            msg.setIcon(QMessageBox.Icon.Critical)
        case SMBOX_ICON_TYPE.ICON_WARNING:
            msg.setIcon(QMessageBox.Icon.Warning)
        case SMBOX_ICON_TYPE.ICON_INFO:
            msg.setIcon(QMessageBox.Icon.Information)
        # case SMBOX_ICON_TYPE.ICON_SUCCESS:
        #     pass

    icon = QIcon()
    icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Normal, QIcon.Off)

    msg.setWindowIcon(icon)
    if len(variant_yes) > 0:
        msg.addButton(variant_yes, QtWidgets.QMessageBox.ButtonRole.YesRole)
    if len(variant_no) > 0:
        msg.addButton(variant_no, QtWidgets.QMessageBox.ButtonRole.NoRole)
    msg.setText(text)

    font = QFont()
    font.setFamilies([u"Segoe UI Emoji"])
    font.setPointSize(12)
    msg.setFont(font)

    if callback is not None:
        msg.buttonClicked.connect(callback)

    msg.exec()
    return msg


def get_current_unix_time() -> int:
    return int(int(datetime.now().timestamp()))


def convert_date_from_sql_format_ex(date: any):
    if isinstance(date, str):
        string = date.split(".")[0]
        if string is False:
            return ""
        else:
            return string
    else:
        return "-"


def convert_date_from_sql_format(date: str):
    string = date.split(".")[0]
    if string is False:
        string = ""
    return string


def is_tv_sn_text_valid(text: str) -> bool:
    clen = len(text)
    if clen < 9 or clen >= 35:
        return False

    if re.search(r'[^A-Z0-9]', text):
        return False

    return True

def is_tricolor_text_valid(text: str) -> bool:
    clen = len(text)
    if clen < 9 or clen >= 35:
        return False

    if re.search(r'[^0-9]', text):
        return False

    return True


def is_pattern_match(pattern: str, data: str) -> bool:
    if len(pattern) == len(data):
        pattern.upper()
        data.upper()
        divided_patten = list(pattern)
        divided_data = list(data)
        for symbol in range(len(divided_patten)):
            if divided_patten[symbol] == '*':
                pass
            else:
                if divided_patten[symbol] == divided_data[symbol]:
                    pass
                else:
                    return False
        return True
    else:
        return False