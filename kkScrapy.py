import os
from bs4 import BeautifulSoup
import requests
from lxml import etree
import re        
import urllib.request as urlReq
import pandas as pd
from tqdm import tqdm
import time


class kk:
    def __init__(self):
        pass

    def date_time(self):
        dt=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()) )
        return dt

    def main(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        # req = requests.get('https://i.kuaikuaikeji.com/kims/boss/tool/helpQuestion2.html?tabId=5',timeout=5,headers=headers)
        # req = requests.get('https://i.kuaikuaikeji.com/kims/boss/tool/data/hn_5_3.html',timeout=5,headers=headers)
        # req = requests.get('https://i.kuaikuaikeji.com/kims/boss/tool/helpQuestion2.html?tabId=5',timeout=5,headers=headers)
        # req = requests.get('d:\\下载\\培训师必读.html',timeout=5,headers=headers)

        
        ptn='(?<=\"clearfix\"\>).*(?=\<\/span\>)'
        # soup = BeautifulSoup(req.content, "lxml")
        htmlfile = open('d:\\下载\\培训师必读.html', 'r', encoding='utf-8')
        htmlhandle = htmlfile.read()
        soup = BeautifulSoup(htmlhandle, "lxml")
        # res=re.findall(ptn,soup)
        # res=soup.find_all('span',class_='clearfix')
        res=soup.find_all('dt')
        # print(res)
        for rr in res:
            # print(str(rr),'\n')
            ptn_1='https://.*\.mp4'
            url=re.findall(ptn_1,str(rr))[0]
            v_name=re.findall(ptn,str(rr))[0]
            print(v_name,',',url)
        # for txt in res:
        #     resss=txt.text
        #     print(resss)

class downKK:
    def __init__(self):
        # self.xls='E:\\WXWork\\1688852895928129\\WeDrive\\大智小超科学实验室\\我的文件\\我的文档\\快快app真实地址.xlsx'
        self.xls='c:\\users\\jack\\desktop\\快快app真实地址.xlsx'

    def read_excel(self):
        self.df=pd.read_excel(self.xls,sheet_name='Sheet2')
        vname=self.df['课程名称'].tolist()
        lst=self.df['地址'].values.tolist()
        odr=self.df['序号'].values.tolist()
        return lst,vname,odr

    def down(self): 
        def getHtml(url):
            html = urlReq.urlopen(url).read()
            return html
        
        def saveHtml(file_name, file_content):
            #    注意windows文件命名的禁用符，比如 /
            with open(os.path.join('d:/temp/kk',file_name) + ".html", "wb") as f:
                #   写文件用bytes而不是str，所以要转码
                f.write(file_content)     

        for addr in tqdm(self.read_excel()):
            aurl = addr
            if aurl!='-':
                savename=aurl.split('/')[-1][0:-5]
                # print(savename)
                html = getHtml(aurl)
                saveHtml(savename,html)

    def patch_down_video(self):
        lst=self.read_excel()
        urls,vnames,odr=lst
        for k,url in enumerate(urls):
            print('正在下载：',k,' ',url.split('/')[-1],'\n')
            savename=os.path.join('d:\\temp\\kk_4',str(odr[k])+'_'+vnames[k]+'_'+url.split('/')[-1])
            self.downvideo_small(url,savename)


    def downvideo_big(self,url,savename):
        r = requests.get(url, stream=True)
        f = open(savename, "wb")
        start = time.time()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        # iter_content：一块一块的遍历要下载的内容
        # iter_lines：一行一行的遍历要下载的内容
        # 这两个函数下载大文件可以防止占用过多的内存，因为每次只下载小部分数据
        # end = time.time()
        # print('Finish in ：', end - start)

    def downvideo_small(self,url,savename):
        start = time.time()
        r = requests.get(url)
        with open(savename, 'wb') as video:
            video.write(r.content)
        end = time.time()
        # print ('Finish in ：', end - start)


if __name__=='__main__':
    # q=kk()
    # q.main()

    q=downKK()
    # rst=q.read_excel()
    # print(rst)
    # q.down()
    q.patch_down_video()