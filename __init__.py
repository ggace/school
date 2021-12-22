from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading
import time
from flask import Flask

app = Flask(__name__)

latestId = 0
msg = ""

url = "https://sdjhs.djsch.kr/boardCnts/list.do?boardID=42359&m=0301&s=sdj"
def getNotice():
    global latestId
    tagIds = []
    tagTexts = []
    result = []

    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.select("div.cntBody.clearfix tbody tr")

    for table in tables:
        tempTag = table.select("td")[0]
        if(tempTag['class'] == []):
            tagId = tempTag.text
            tagIds.append(tagId)
        else:
            tagText = tempTag.select("a")[0]['title']
            tagTexts.append(tagText)
    
    for i in range(len(tagIds)):
        result.append({'Id' : tagIds[i], 'Text' : tagTexts[i]})
    

    if(int(result[0]['Id']) != latestId):
        latestId = int(result[0]['Id'])
        

    time.sleep(5)
    getNotice()

@app.route("/")
def mainPage():
    global latestId
    global msg
    pageHtml = {"id" : latestId}
    return pageHtml

def main():
    app.run(debug=True)

getNoticeThread = threading.Thread(target=getNotice)


getNoticeThread.start()

main()
