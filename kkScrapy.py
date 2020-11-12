import os
from bs4 import BeautifulSoup
import requests
from lxml import etree
import re        
import urllib.request as urlReq
import pandas as pd


class kk:
    def __init__(self):
        pass

    def date_time(self):
        dt=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()) )
        return dt

    def main(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        # req = requests.get('https://i.kuaikuaikeji.com/kims/boss/tool/helpQuestion2.html?tabId=5',timeout=5,headers=headers)
        req = requests.get('https://i.kuaikuaikeji.com/kims/boss/tool/data/hn_5_3.html',timeout=5,headers=headers)
        
        ptn='(?<=\"clearfix\"\>).*(?=\<\/span\>)'
        soup = BeautifulSoup(req.content, "lxml")
        # res=re.findall(ptn,soup)
        res=soup.find_all('span',class_='clearfix')

        for txt in res:
            resss=txt.text
            print(resss)

class downKK:
    def __init__(self):
        self.xls='E:\\WXWork\\1688852895928129\\WeDrive\\大智小超科学实验室\\我的文件\\我的文档\\快快app真实地址.xlsx'

    def read_excel(self):
        self.df=pd.read_excel(self.xls)
        lst=self.df['地址'].values.tolist()
        return lst

    def down(self): 
        def getHtml(url):
            html = urlReq.urlopen(url).read()
            return html
        
        def saveHtml(file_name, file_content):
            #    注意windows文件命名的禁用符，比如 /
            with open(os.path.join('e:/temp/kk',file_name) + ".html", "wb") as f:
                #   写文件用bytes而不是str，所以要转码
                f.write(file_content)     

        for addr in self.read_excel():
            aurl = addr
            if aurl!='-':
                savename=aurl.split('/')[-1][0:-5]
                # print(savename)
                html = getHtml(aurl)
                saveHtml(savename,html)

        

 


if __name__=='__main__':
    # q=kk()
    # q.main()

    q=downKK()
    # q.read_excel()
    q.down()