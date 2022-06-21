#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from scriptGenerator import ScriptGenerator
import scraper, syntax, img_downloader
import pymongo
import qtmodern.styles
import qtmodern.windows
from datetime import datetime
class MainWindow(QMainWindow):
    """ The class that defines the structure of the application's GUI.

        The main GUI contains URL Input box, Selector Input box and following 3 tabs:
        1.) Script Tab : Python Script is generated here for required scraping
        2.) Webpage Tab : Displays the website of input URL
        3.) Data Tab : Displays the Scraped Data using Input URL & Selector
    """
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)
        self.menubar = self.menuBar()
        help_ = self.menubar.addMenu("Помощь")
        aboutAction = QAction("О программе",self)
        self.shortcut = QShortcut(QKeySequence("Alt+A"),self)
        self.shortcut.activated.connect(self.about)
        aboutAction.setToolTip("О Alek-Scrapper")
        aboutAction.triggered.connect(self.about)

        contributeAction = QAction("Если заметили ошибку",self)
        self.shortcut = QShortcut(QKeySequence("Alt+C"),self)
        self.shortcut.activated.connect(self.contribute)
        contributeAction.setToolTip("Данный репозиторий")
        contributeAction.triggered.connect(self.contribute)

        usageAction = QAction("Использование",self)
        self.shortcut = QShortcut(QKeySequence("Alt+U"),self)
        self.shortcut.activated.connect(self.usage)
        usageAction.setToolTip("Инструкция для пользования")
        usageAction.triggered.connect(self.usage)

        help_.addAction(aboutAction)
        help_.addAction(contributeAction)
        help_.addAction(usageAction)

        self.dialog = QDialog()

        self.statusbar = self.statusBar()

        mainlayout = QVBoxLayout()
        grid = QGridLayout()

        font = QFont("Times",13)
        self.urlLabel = QLabel("Ссылка:")
        self.urlLabel.setFont(font)
        self.urlInput = QLineEdit()
        self.urlInput.setFont(font)
        self.sepInput = QLineEdit ()
        self.sepInput.setFont (font)
        self.sepInput.setFixedSize(70,30)
        self.selectorLabel = QLabel("Тэг селектор:")
        self.selectorLabel.setFont(font)
        self.selectorInput = QLineEdit()
        self.selectorInput.setFont(font)
        self.button = QPushButton()
        self.button.setFont(font)
        self.button.setText("Начать")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.modifyUI)
        #кнопка сохранения
        self.savebutton = QPushButton ()
        self.savebutton.setFont (font)
        self.savebutton.setText ("Cохранить")
        self.savebutton.setFixedWidth (130)
        self.savebutton.clicked.connect (self.saveSCV)
        # кнопка сохранения в монго
        self.saveMongoButton = QPushButton ()
        self.saveMongoButton.setFont (font)
        self.saveMongoButton.setText ("Cохранить в БД")
        self.saveMongoButton.setFixedWidth (180)
        self.saveMongoButton.clicked.connect (self.btnClicked)
        #кнопка скачивания картинок
        self.saveIMG = QPushButton ()
        self.saveIMG.setFont (font)
        self.saveIMG.setText ("Cохранить картинки")
        self.saveIMG.setFixedWidth (220)
        self.saveIMG.clicked.connect (self.saveImg)
        grid.addWidget(self.urlLabel,0,0)
        grid.addWidget(self.urlInput,0,1)
        grid.addWidget (self.sepInput, 0, 2)
        grid.addWidget(self.selectorLabel,1,0)
        grid.addWidget(self.selectorInput,1,1)
        grid.addWidget (self.saveIMG, 0, 3)
        grid.addWidget(self.button,2,1)
        grid.addWidget (self.savebutton, 2, 2)
        grid.addWidget (self.saveMongoButton, 2, 3)

        mainlayout.addLayout(grid)

        self.tab = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab.addTab(self.tab1, "1")
        self.tab.addTab(self.tab2,"2")
        self.tab.addTab(self.tab3,"3")
        tab1layout = QVBoxLayout()
        self.scriptBrowser = QTextBrowser()
        self.scriptBrowser.append("")
        self.scriptBrowser.setFont(QFont("Courier",13))
        self.scriptBrowser.setTextColor(QColor("#C5C8C6"))
        self.scriptBrowser.setStyleSheet("background-color: #1d1f21")
        self.scriptBrowser.setText("Здесь генерируется Скрипт")
        tab1layout.addWidget(self.scriptBrowser)
        self.tab.setTabText(0,"Python Script")
        self.tab.setFont(font)
        self.tab1.setLayout(tab1layout)

        tab2layout = QVBoxLayout()
        self.web = QWebEngineView()
        tab2layout.addWidget(self.web)
        self.tab.setTabText(1,"Web-страница")
        self.tab2.setLayout(tab2layout)

        tab3layout = QVBoxLayout()
        self.dataBrowser = QTextBrowser()
        self.dataBrowser.setFont(QFont("Courier",13))
        self.dataBrowser.setTextColor(QColor("#C5C8C6"))
        self.dataBrowser.append("Собранная информация: \n\n")
        self.dataBrowser.setStyleSheet("background-color: #1d1f21")
        tab3layout.addWidget(self.dataBrowser)
        self.tab.setTabText(2,"Результат")
        self.tab3.setLayout(tab3layout)

        mainlayout.addWidget(self.tab)
        self.dialog.setLayout(mainlayout)
        self.setCentralWidget(self.dialog)
        self.setWindowTitle("Alek-Scrapper")

    def about(self):
        """ Defines the action when the about item under help menu is clicked.

            Displays the basic description of Py-Scrapper.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Alek-Scrapper - это универсальное средство сбора информации с интернет-источников."+"\n\nСозданное с помощью Python 3.5.2 и PyQt5.\n")
        info = "Зайдите на <a href=\"https://github.com/olegolegka\">Мой репозиторий</a>"
        msg.setInformativeText(info)
        msg.setWindowTitle("О программе")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def contribute(self):
        """ Defines the action when Contribute option under help menu is clicked.

            Opens the source code repository.
        """
        link = "https://github.com/olegolegka"
        QDesktopServices.openUrl(QUrl(link))

    def usage(self):
        """ Defines the action when the Usage menu item is clicked.

            Displays a message box showing the instrucions of Usage.
        """
        text = """
        <p>В окно "Ссылка" вставьте Url адрес ресурса с которого хотите собрать информацию.</p>
        <p>В окно "Тэг селектор" вставьте тэг с классом(не обязательно) той части страницы информацию которого хотите собрать. <i>(Ниже инструкция как пользоваться селекторами)</i></p>
        <h4>Как использовать селекторы</h4>
        <p>Селектор должен быть валидным CSS селектором. Для рекурсивного сбора соблюдайте иерархию тегов.
        <ul><li>&nbsp;&nbsp;Используйте '->' символ чтобы разделить разные тэги.<li>
        <li>&nbsp;&nbsp;Если вы хотите собрать элементы одного уровня заключите их в "()" и разделите запятой.</li></ul></p>
        <br/></br>
        <p><b><u>ПРИМЕРЫ:</u></b></p>
        <ol>
        <li>
        <p><i>a.category -> a.subcategory -> div.item -> (p.title, p.description)</i></p>
        <p>Данная команда соберет текст с параграфа с классами 'title' и 'description' для каждого элемента каждой категории и подкатегории.</p>
        </li>
        <li>
        <p>Также можно использовать другой путь для разделения вложенных CSS селекторов используя "->". </p>
        <p>Для примера, если вы хотите собрать текст span элемента с классом "text" который лежит внутри элемента div с классом "details", используйте что-то вроде этого:</p>
        <p><i>div.details -> span.text</i></p>
        </li>
        </ol>
        """
        details = QMessageBox()
        details.setText(text)
        details.setIcon(QMessageBox.Information)
        details.setWindowTitle("Использование")
        details.exec_()

    def modifyUI(self):
        """ Method to modify UIs for the tabs after scraping.

            First, the required web page is loaded on the webpage tab.
            Second, the python script is generated and stored in script member variable
            Third, scraper instance is created and scraping starts on a separate thread.
            As soon as scraping finishes, the method addScriptAndData() is called.
        """
        if self.urlInput.isModified() and self.sepInput.isModified() and self.selectorInput.isModified():
            url = self.urlInput.text()
            sep = self.sepInput.text()
            selectors = self.selectorInput.text()
            self.web.load(QUrl(url))
            self.scraper_ = scraper.Scraper (str (url), str (selectors),str(sep))
            self.script = ScriptGenerator(url,selectors).generate()
            self.scraper_.threadChange.connect(self.addScriptAndData)
            self.scraper_.start()
        else:
            msg1 = QMessageBox ()
            msg1.setIcon (QMessageBox.Information)
            msg1.setText (
                "Произошла ошибка" + "\n\nПроверьте введенные данные\n")
            msg1.setWindowTitle ("Ошибка")
            msg1.setStandardButtons (QMessageBox.Ok)
            msg1.exec_ ()

    def addScriptAndData(self):
        """ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Method which adds the script and scraped data to respective tabs.

            Syntax highlighter instance is created and functionality added to script Tab.
        """
        self.dataBrowser.setText(self.scraper_.data.encode('utf-8').decode('utf-8'))
        self.highlight = syntax.PythonHighlighter(self.scriptBrowser.document())
        self.scriptBrowser.setText(self.script)

    def btnClicked(self):
        try:
            savesel = self.scraper_.savesel1
            list_of_sel = self.scraper_.list_of_selectors
            self.chile_Win = ChildWindow (savesel,list_of_sel)
            self.chile_Win.move (self.x () + self.saveMongoButton.geometry ().x () + 1,
                                 self.y () + self.saveMongoButton.geometry ().y () + self.saveMongoButton.height () + 35)
            self.chile_Win.show ()
        except:
            msg1 = QMessageBox ()
            msg1.setIcon (QMessageBox.Information)
            msg1.setText (
                "Произошла ошибка" + "\n\nПроверьте введенные данные\n")
            msg1.setWindowTitle ("Ошибка")
            msg1.setStandardButtons (QMessageBox.Ok)
            msg1.exec_ ()

    def saveSCV(self):
        try:
            self.data  = self.scraper_.data.encode('utf-8').decode('utf-8')
            date = str(datetime.now()).replace(" ","-").replace(":","-")
            print(date,type(date))
            with open ('{0}.csv'.format(date[:20]), 'w') as file:
                file.write (self.data)
        except:
            msg1 = QMessageBox ()
            msg1.setIcon (QMessageBox.Information)
            msg1.setText (
                "Произошла ошибка" + "\n\nПроверьте введенные данные\n")
            msg1.setWindowTitle ("Ошибка")
            msg1.setStandardButtons (QMessageBox.Ok)
            msg1.exec_ ()

    def saveImg(self):
        if self.urlInput.isModified () and self.sepInput.isModified ():
            url = self.urlInput.text ()
            sep = self.sepInput.text ()
            img_downloader.img_Downloader(url,sep)
        else:
            msg1 = QMessageBox ()
            msg1.setIcon (QMessageBox.Information)
            msg1.setText (
                "Произошла ошибка" + "\n\nПроверьте введенные данные\n")
            msg1.setWindowTitle ("Ошибка")
            msg1.setStandardButtons (QMessageBox.Ok)
            msg1.exec_ ()

class ChildWindow (QDialog):
    def __init__(self,savesel,list_of_sel, parent=None):
        super (ChildWindow, self).__init__ (parent)
        font = QFont ("Times", 13)
        self.savesel = savesel
        self.list_of_sel = list_of_sel
        font1 = QFont ("Times", 13)
        self.verticalLayout = QtWidgets.QVBoxLayout (self)
        self.verticalLayout.setObjectName ("verticalLayout")
        self.resize (600, 600)
        self.collectionLabel = QLabel ("Коллекция:")
        self.collectionLabel.setFont (font)
        self.collectionInput = QLineEdit ()
        self.collectionInput.setFont (font)
        self.verticalLayout.addWidget (self.collectionLabel)
        self.verticalLayout.addWidget (self.collectionInput)
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(self.savesel))
        self.row = 0
        self.col = 1
        for tup in self.savesel:
            cellinfo = QTableWidgetItem (tup)
            self.table.setItem(self.row,self.col,cellinfo)
            self.row+=1
        self.table.setHorizontalHeaderLabels (["Название", "Тэг"])
        self.verticalLayout.addWidget(self.table)

        self.acceptButton = QtWidgets.QPushButton (self)
        self.acceptButton.setObjectName ("acceptButton")
        self.acceptButton.clicked.connect (self.saveMongo)
        self.verticalLayout.addWidget (self.acceptButton)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect (self.btnClosed)
        self.verticalLayout.addWidget(self.cancelButton)

        self.cancelButton.setText("Отмена")
        self.setWindowTitle ("Сохранить в бд")
        self.acceptButton.setText ("Сохранить")
    def btnClosed(self):
        self.close ()

    def saveMongo(self):
        """
        Class for saving to MongoDB
        first need connect db
        """
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client.user_db
            collection = db[self.collectionInput.text()]
            for i in range (len (self.savesel)):
                for tup in self.list_of_sel:
                        colDict = {self.table.item(i,0).text():tup[1]}
                        collection.insert_one (colDict).inserted_id
        except:
            msg2 = QMessageBox ()
            msg2.setIcon (QMessageBox.Information)
            msg2.setText (
                "Произошла ошибка при сохранении" + "\n\nПроверьте введенные данные или связь с базой данных\n")
            msg2.setWindowTitle ("Ошибка")
            msg2.setStandardButtons (QMessageBox.Ok)
            msg2.exec_ ()
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    qtmodern.styles.dark (app)
    mw = qtmodern.windows.ModernWindow (window)
    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()
