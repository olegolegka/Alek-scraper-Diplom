#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from scriptGenerator import ScriptGenerator
import scraper, syntax

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
        # self.savebutton.clicked.connect (self.modifyUI)
        grid.addWidget(self.urlLabel,0,0)
        grid.addWidget(self.urlInput,0,1)
        grid.addWidget (self.sepInput, 0, 2)
        grid.addWidget(self.selectorLabel,1,0)
        grid.addWidget(self.selectorInput,1,1)
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
        info = "Visit the <a href=\"https://github.com/olegolegka\">Мой репозиторий</a>"
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
        <p>Также можно использовать другой путь для разделения вложенных CSS селекторов используя ">". </p>
        <p>Для примера, если вы хотите собрать текст span элемента с классом "text" который лежит внутри элемента div с классом "details", используйте что-то вроде этого:</p>
        <p><i>div.details > span.text</i></p>
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
        url = self.urlInput.text()
        sep = self.sepInput.text()
        selectors = self.selectorInput.text()
        self.web.load(QUrl(url))
        self.scraper_ = scraper.Scraper (str (url), str (selectors),str(sep))
        self.script = ScriptGenerator(url,selectors).generate()
        self.scraper_.threadChange.connect(self.addScriptAndData)
        self.scraper_.start()

    def addScriptAndData(self):
        """ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Method which adds the script and scraped data to respective tabs.

            Syntax highlighter instance is created and functionality added to script Tab.
        """
        self.dataBrowser.setText(self.scraper_.data.encode('utf-8').decode('utf-8'))
        self.highlight = syntax.PythonHighlighter(self.scriptBrowser.document())
        self.scriptBrowser.setText(self.script)

    def saveSCV(self):
        self.data  = self.scraper_.data.encode('utf-8').decode('utf-8')
        print(self.data)
        with open ('test.csv', 'w') as file:
            file.write (self.data)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
