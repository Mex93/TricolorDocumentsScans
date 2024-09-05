# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import ui.res_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1012, 370)
        MainWindow.setMinimumSize(QSize(719, 297))
        icon = QIcon()
        icon.addFile(u":/res/images/logo.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(30, 30))
        self.action_info = QAction(MainWindow)
        self.action_info.setObjectName(u"action_info")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_main)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comboBox_model_name = QComboBox(self.frame_main)
        self.comboBox_model_name.setObjectName(u"comboBox_model_name")
        font = QFont()
        font.setPointSize(20)
        self.comboBox_model_name.setFont(font)
        self.comboBox_model_name.setEditable(False)

        self.verticalLayout_5.addWidget(self.comboBox_model_name)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEdit_input = QLineEdit(self.frame_main)
        self.lineEdit_input.setObjectName(u"lineEdit_input")
        self.lineEdit_input.setMinimumSize(QSize(677, 31))
        font1 = QFont()
        font1.setPointSize(14)
        self.lineEdit_input.setFont(font1)
        self.lineEdit_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.lineEdit_input)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_message = QLabel(self.frame_main)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setFont(font1)
        self.label_message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_message)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_tv_sn = QLabel(self.frame_main)
        self.label_tv_sn.setObjectName(u"label_tv_sn")
        font2 = QFont()
        font2.setPointSize(15)
        self.label_tv_sn.setFont(font2)
        self.label_tv_sn.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.label_tv_sn)

        self.label_tv_model = QLabel(self.frame_main)
        self.label_tv_model.setObjectName(u"label_tv_model")
        self.label_tv_model.setFont(font2)
        self.label_tv_model.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.label_tv_model)

        self.label_tricolor_id = QLabel(self.frame_main)
        self.label_tricolor_id.setObjectName(u"label_tricolor_id")
        self.label_tricolor_id.setFont(font2)
        self.label_tricolor_id.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.label_tricolor_id)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_print = QPushButton(self.frame_main)
        self.pushButton_print.setObjectName(u"pushButton_print")
        self.pushButton_print.setFont(font2)
        icon1 = QIcon()
        icon1.addFile(u":/res/images/print_ok.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_print.setIcon(icon1)
        self.pushButton_print.setIconSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.pushButton_print)

        self.pushButton_cancel = QPushButton(self.frame_main)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(354, 48))
        self.pushButton_cancel.setFont(font2)
        icon2 = QIcon()
        icon2.addFile(u":/res/images/disabled_by_default.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_cancel.setIcon(icon2)
        self.pushButton_cancel.setIconSize(QSize(40, 40))

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_6.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1012, 22))
        self.menu_info = QMenu(self.menubar)
        self.menu_info.setObjectName(u"menu_info")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_info.menuAction())
        self.menu_info.addAction(self.action_info)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_info.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.comboBox_model_name.setPlaceholderText("")
        self.lineEdit_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 SN \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430", None))
        self.label_message.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_tv_sn.setText(QCoreApplication.translate("MainWindow", u"TV_SN:", None))
        self.label_tv_model.setText(QCoreApplication.translate("MainWindow", u"TV_MODEL:", None))
        self.label_tricolor_id.setText(QCoreApplication.translate("MainWindow", u"TRICOLOR_ID:", None))
        self.pushButton_print.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u043f\u0435\u0447\u0430\u0442\u0430\u0442\u044c \u044d\u0442\u0438\u043a\u0435\u0442\u043a\u0443", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.menu_info.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
    # retranslateUi

