#!/usr/bin/env python
# coding: utf-8

# In[20]:


import os
import sys
import folium
import numpy as np
from folium.plugins import HeatMap
import requests
import json
import pandas as pd
import webbrowser



class Data:
    def __init__(self,excel):
        self.excel=os.path.join(os.getcwd(),excel)
        self.kkCusPosData='快快地理数据.txt'
    
    def read_excel(self):
        print('\n正在读取数据……\n',end='')
        df=pd.read_excel(self.excel,index_col=False)
        df_have_addr=df[~df['住址'].isin(['-'])] #去掉地址为'-‘的值
        addrs_counts=pd.DataFrame(pd.value_counts(df_have_addr['住址']))
        addrs_counts.reset_index(level=0, inplace=True)
        addrs_counts.columns=['住址','数量']
        addrs_counts['百分比']= addrs_counts['数量']/addrs_counts['数量'].sum()     #计算占比 
        addrs=addrs_counts.values.tolist()
        print('完成')        
        print('\n正在获取地址坐标……\n',end='')
        addrXY=[]
        for addr in addrs:
            if addr and addr[0]!='-':
                XY=self.get_lat_lng(addr)
                if XY not in addrXY:
                    addrXY.append(XY)        
        print('完成')
        return addrXY   
        
        
    def drawMap(self,addrXY):
        print('\n正在标记地图……',end='')
        city_map = folium.Map(location=[22.806421,108.398991],                               zoom_start=16,                               tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',attr='default' #                               tiles='http://wprd0{1-4}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7&ltype=1',attr='default' \
                             )
        tooltip =self.utf2asc('请点击我查看该点信息')
        folium.Marker([22.806421,108.398991], popup=('<i>'+self.utf2asc('快快')+'</i>'),icon=folium.Icon(color='orange',icon='flag',prefix='fa')).add_to(city_map)

        #构造热力图所需的数据结构
        lat=np.array([addrXY[i][1] for i in range(len(addrXY))],dtype=float)
        lng=np.array([addrXY[i][2] for i in range(len(addrXY))],dtype=float)
        amt=np.array([addrXY[i][3] for i in range(len(addrXY))],dtype=float)
        
        data=[[lat[i],lng[i],amt[i]] for i in range(len(addrXY))]
        HeatMap(data).add_to(city_map) #绘制热力图
      
        for addr in addrXY:
            folium.Marker([addr[1],addr[2]], popup=self.utf2asc(addr[0]+'\n\n'+str(addr[3])+'人次'),                           icon=folium.Icon(color='purple',icon='user',prefix='fa')).add_to(city_map)
            
        print('\n标记完成，正在绘图：\n')    
        
        if os.path.basename(sys.argv[0])=='ipykernel_launcher.py':
            display(city_map)
        else:
            city_map.save('KK_cus_inf_temp.html')
            webbrowser.open('KK_cus_inf_temp.html')
        
    def get_lat_lng(self,kw):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        key='7VQBZ-OLIK6-2ERS7-EZHVL-VYQF7-EUB5M'
       
        fn=os.path.join(os.getcwd(),self.kkCusPosData)
        if os.path.exists(fn):
            with open(fn,'r') as f:
                lines=f.readlines()
                dat=[]
                for line in lines:
                    if line:
                        dat.append(line.strip().split(','))
                data=pd.DataFrame(dat,columns=['住址','lat','lng'])  
        else:
            f=open(fn,'a')
            f.write('')
            f.close()
            data=pd.DataFrame(columns=['住址','lat','lng']) 
#             f.save(fn)
        mapAddr=[]

        if data.shape[0]>0 and kw[0] in data['住址'].values:
            print('本地获取【 {} 】地址'.format(kw[0]))
            adr,lat,lng=kw[0],data[data['住址']==kw[0]]['lat'].values[0],data[data['住址']==kw[0]]['lng'].values[0]
            mapAddr=[adr,lat,lng,kw[1],kw[2]] 
        else:
            print('远程获取【 {} 】地址……'.format(kw[0]),end='')
            url='https://apis.map.qq.com/ws/place/v1/search?keyword='+kw[0]+'&boundary=nearby(22.808139,108.398066,1000)&key='+key
            req=requests.get(url,headers=headers)
            t=req.text

            mapList=json.loads(t)
            lat,lng=mapList['data'][0]['location']['lat'],mapList['data'][0]['location']['lng']
            mapAddr=[kw[0],lat,lng,kw[1],kw[2]]
            
            adr_to_write=','.join([kw[0],str(lat),str(lng)])
            with open(self.kkCusPosData,'a') as ff:
                ff.write('\n'+adr_to_write)
            print('写入本地经纬度数据文件')
        return mapAddr
    
    def utf2asc(self,s): #正确显示中文
        return str(str(s).encode('ascii', 'xmlcharrefreplace'))[2:-1]    
    
if __name__=='__main__':
    mydata=Data('南宁五洲国际店6月1号到今天业绩数据明细.xlsx')
    addrXY=mydata.read_excel()
#     print(addrXY)
#     addrXY=['']
    mydata.drawMap(addrXY)

    

