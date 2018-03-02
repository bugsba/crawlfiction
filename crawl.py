import requests
import re
import queue

def getgbktext(url):
    r = requests.get(url)
    r.encoding = 'GB18030'
    return r.text

def savetolocal(content,filename):
    file_object = open(filename,'w',encoding='utf-8')
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
#    print(tempcontent)
    tempregex = r'h2>(.*)</h2'
    match = re.search(tempregex,tempcontent)
    title = match.group(1)
    tempregex = r'cgSize\);\}</script>\s*(.*?)<{1,2}script'
    match = re.search(tempregex,tempcontent,re.S)

    if(match):
        temp = match.group(1).replace('&nbsp;',' ')
        temp = temp.replace('<br /><br />','\n')
        temp = temp.replace('</div>','')
        temp = re.sub(r'<.*?>','',temp)
#        print(title+'\n'+temp)
        return(title+'\n'+temp)
    else:
        return(title+'\n'+temp)

indexurl = 'http://www.xinshuzx.cn/wodedabaojian/'
regexstr = r'li><a href="(/w\S+?)"'
qurl=extracttab(regexstr,getgbktext(indexurl))
preurl = "http://www.xinshuzx.cn"
temparticle = ''
'''
urlitem = qurl.get()
urlitem = '/wodedabaojian/13147.html'
temparticle = temparticle+getarticle(preurl+urlitem)
savetolocal(temparticle,'我的大宝剑.txt')
'''
while not qurl.empty():
    urlitem = qurl.get()
    print(preurl+urlitem)
    temparticle = temparticle+getarticle(preurl+urlitem)+'\n'
 #   temparticle.encode(encoding='utf-8',errors= 'backslashreplace')
savetolocal(temparticle,'我的大宝剑.txt')
