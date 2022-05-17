import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyQt5 import QtCore
import pymongo
import re
class Scraper(QtCore.QThread):
    """ Class for scraping webpages

        url       : starting link for scraping
        selectors : user input of selectors
        data      : string that stores the scraped data

        It inherits from the class QThread to facilitate multithreading
    """
    threadChange = QtCore.pyqtSignal(str)
    def __init__(self,link,selectors,sep = None):
        QtCore.QThread.__init__(self)
        self.url = link
        self.sep = sep
        self.CSSSelectors = selectors

    def run(self):
        """ Overrides the run() method of QThread Class.

            It parses the website URL.
            Website content is requested, BeautifulSoup object is created and then
            scrape() function is called for required scraping.
            Emits a SIGNAL threadChange to notify exiting of thread.
        """
        self.data = ""
        self.list_of_selectors = []
        separator = int(self.sep)

        try:
            for i in range(0,separator,1):
                url = self.url
                url = url + str(i+1)
                r = requests.get(url,timeout=5)
                page = BeautifulSoup (r.content, "html.parser")
                self.modify ()
                self.scrape (url, page, 0, len (self.CSSSelectors) - 1, self.CSSSelectors)
                self.threadChange.emit ("threadChange")
                print ("Scrapping done from: "+ url)
        except Exception as e:
            self.data = "Соединение закрыто - невозжно собрать"
            print(e)

    def modify(self):
        """ Modifies the string selector and converts it into list of selectors
        """
        self.savesel1 = []
        if isinstance(self.CSSSelectors,str):
            selectors = self.CSSSelectors.split('->')
        else:
            selectors = self.CSSSelectors
        for it in range(len(selectors)):
            selectors[it] = selectors[it].lstrip().rstrip()
            if selectors[it].startswith('('):
                self.savesel1 = selectors[it]
                self.savesel1 = self.savesel1[1:len(self.savesel1)-1]
                self.savesel1 = self.savesel1.split(',')
            else:
                self.savesel1.append(selectors[it])
        self.CSSSelectors = selectors

    def scrape(self,url,soup,index,hi,selectors):
        """ Recursively scrapes the webpage as per the given input.

            url       : current url being scraped
            soup      : current BeautifulSoup object being operated on
            index     : current index of the list of selectors
            hi        : highest index of the list of selectors
            selectors : the actual list of selectors (created from user input)
        """
        if index > hi:
            self.list_of_selectors.append((selectors[hi],soup.get_text()))
            text = soup.get_text()
            text = str(text.encode('utf-8').decode('utf-8'))
            self.data += text.lstrip().rstrip()+'\n'
            return
        elif index != hi and (selectors[index].startswith('a.') or selectors[index] == 'a'):
            elements = soup.select(selectors[index])
            for ele in elements:
                href = ele.get('href')
                new_url = urljoin(url,href)
                try:
                    req = requests.get(new_url,timeout=5)
                except:
                    self.data = "Connection Refused - Could not Scrape"
                    print("Connection Refused")
                    return
                new_soup = BeautifulSoup(req.content,"html.parser")
                self.scrape(new_url,new_soup,index+1,hi,selectors)#1
        else:
            if selectors[index].startswith('('):
                lis = selectors[index]
                lis = lis[1:len(lis)-1]
                lis = lis.split(',')
                for it in range(0,len(lis)):
                    lis[it] = lis[it].lstrip().rstrip()
                for selector in lis:
                    new_soup = soup.select(selector)
                    for it in range(len(new_soup)):
                        self.list_of_selectors.append((selector,new_soup[it].get_text()))
                        self.scrape(url,new_soup[it],index+1,hi,selectors)#2
                self.data += '\n\n'
            else:
                new_soup = soup.select(selectors[index])
                for it in range(len(new_soup)):
                    self.scrape(url,new_soup[it],index+1,hi,selectors)#3
    def imgDownload(self):
        url = self.url
#Testing done on following
#inp = "a.organization-card__link -> (h3.banner__title,li.organization__tag--technology)"
#link = "https://summerofcode.withgoogle.com/archive/2016/organizations/"
#SUCCESS
