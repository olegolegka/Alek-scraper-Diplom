import re
import requests
from bs4 import BeautifulSoup
import os
def img_Downloader(url,sep = ''):
    name_folder = "images"
    isExist = os.path.exists (name_folder)
    if not isExist:
        os.mkdir(name_folder)
    try:
        for i in range(0,int(sep),1):
            URL = url + str(i)
            page = requests.get(URL.strip(), timeout=5,)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all('img')
            count = 0

            for result in results:
                link = result['src']
                print(link)
                name = result['<img alt']
                print(name)
                img_data = requests.get(link)
                print(img_data.content)

                with open(name_folder + "/" + str(count) + ".jpg", "wb") as handler:
                    handler.write(img_data.content)
                count += 1
    except:
        print("что то пошло не так")