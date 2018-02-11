import requests
import re
import queue

def getgbktext(url):
    r = requests.get(url)
    r.encoding = 'gbk'
    return r.text

def savetolocal(content,filename):
    file_object = open(filename,'w')
    file_object.write(content)
    file_object.close()

def extracttab(regex,content):
    reslinks = re.finditer(regex,content)
    qurl = queue.Queue()
    for templink in reslinks:
        qurl.put(templink.group(1))
    return qurl 

def getarticle(url):
    tempcontent = getgbktext(url)
    tempregex = r'yd_text2"">(.*?)</div'
    match = re.search(tempregex,tempcontent)
    temp = match.group(1).replace('&nbsp;',' ')
    return temp.replace('<br /><br />','\n')

indexurl = 'http://www.bichi.me/read/349697.html'
regexstr = r'td_con.+?href="(\S+)?"'
qurl=extracttab(regexstr,getgbktext(indexurl))
preurl = "http://www.bichi.me"
temparticle = ''
while not qurl.empty():
    urlitem = qurl.get()
    temparticle = temparticle+getarticle(preurl+urlitem)+'\n'
savetolocal(temparticle,'我的大宝剑.txt')