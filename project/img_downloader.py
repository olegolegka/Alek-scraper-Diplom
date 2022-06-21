import requests
from bs4 import BeautifulSoup
import os
from random import randint
from time import sleep
def img_Downloader(url,sep = ''):
    name_folder = "images"
    isExist = os.path.exists (name_folder)
    if not isExist:
        os.mkdir(name_folder)
    try:
        for i in range(0,int(sep),1):
            print("я запустился")
            URL = url + str(i)
            print(url)
            out = randint(2, 6)
            page = requests.get(URL.strip(), timeout=out)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all('img')
            count = 0
            for result in results:
                link = result['src']
                if result['alt']:
                    name = result['alt']
                else:
                    name = count
                if link.startswith("http"):
                    img_data = requests.get(link)
                    print(img_data.status_code)
                else:
                    continue
                try:
                    with open(name_folder + "/" + name + ".jpg", "wb") as handler:
                        handler.write(img_data.content)
                    count += 1
                except:
                    print("ошибка записи")
                    continue
    except:
        print("что то пошло не так")