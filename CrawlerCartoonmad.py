import requests
from bs4 import BeautifulSoup
import datetime
import os
from requests.models import Response
import time
# 要爬的漫畫網 Domain 
domainUrl = 'https://www.cartoonmad.com'
# 作品頁 Ex: https://www.cartoonmad.com/comic/4982.html
url = f'{domainUrl}/comic/4982.html'
# 設定Request Header
myheader= { 'cookie' : 'ASPSESSIONIDAGRRQCQB=KDKBFDBDEKNFJHJPCBEFPMKA; ASPSESSIONIDAEQSTCRB=CONBNONDACGFIMNDIAICGNLI;'
           ,'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
           ,'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
           ,'Connection' : 'keep-alive'
           ,'dnt' : '1'
           ,'Referer': 'https://www.cartoonmad.com/'
          }
# 傳送Get Request          
worksResponse = requests.get(url, headers=myheader)
worksResponse.encoding = "big5" 
# 解析
worksSoup = BeautifulSoup(worksResponse.text, 'html.parser')
worksName = worksSoup.findAll('input', {'name': 'name'})[0]['value'] # 作品名稱
fieldset = worksSoup.find_all('fieldset')
# fieldset第二筆為作品集的所有話數連結
aset = fieldset[1].find_all('a')
if not os.path.exists(f'{worksName}')  : # 建立作品資料夾
   os.mkdir(f"{worksName}")

# 爬每一話
for link in aset: 
    isNotEnd = True # 是否結束此話的下載
    href = link["href"] # 取得此話連結
    setName = link.text.replace(" ", "") # 取的此話名稱
    pageUrl = f"{domainUrl}{href}" # 設定此話要爬的URL
    pageDomainUrl = f"https://www.cartoonmad.cc/comic/" #每一頁指向下一頁的Domain Name
    setPath = os.path.join(worksName,setName) # 第X話路徑
    if not os.path.exists(setPath)  : # 建立第X話資料夾
        os.mkdir(setPath)
        # 爬此話裡的每一頁
        while isNotEnd : 
            setResponse = requests.get(pageUrl, headers=myheader)
            setResponse.encoding = "big5" 
            setSoup = BeautifulSoup(setResponse.text, 'html.parser')
            thisPageNumber = setSoup.find_all("a", {'class':'onpage'})[0] #這一話頁數
            thisPage = setSoup.find_all("img", {'oncontextmenu': "return false"})[0] #這一話圖片連結
            nextPage = setSoup.find_all("img", {'oncontextmenu': "return false"})[0].findPrevious("a") #下一頁連結
            img = requests.get(thisPage['src'], headers=myheader) # 取得圖片內容
            imgPath = os.path.join(setPath, thisPageNumber.text) # 取得圖片路徑
            with open(f"{imgPath}.jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
                file.write(img.content)
            pageUrl = f"{pageDomainUrl}{nextPage['href']}" #改成下一頁連結重爬一次
            # 判斷下一頁是否為最後一頁
            if nextPage['href'].find("http://www.comicmad.fun8.us/comic/thend.asp") != -1 :
                # 最後一頁跳出迴圈，找下一話
                isNotEnd = False
            time.sleep(1)

