#!/usr/bin/env python
# coding: utf-8

# In[100]:


import os
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
        
        print('\n正在获取地址坐标……',end='')
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
#         addrXY=[['东盟昌泰中央城', 22.805712, 108.400131, 4, 0.15384615384615385], ['幸福里', 22.810561, 108.394393, 4, 0.15384615384615385], ['凤岭1号', 22.80616, 108.397258, 3, 0.11538461538461539], ['五洲国际', 22.806906, 108.39822, 2, 0.07692307692307693], ['新新家园', 22.815392, 108.407608, 2, 0.07692307692307693], ['中新小区', 22.817791, 108.284548, 2, 0.07692307692307693], ['尚城街区', 22.81481, 108.42537, 1, 0.038461538461538464], ['江南检察院', 22.786126, 108.339691, 1, 0.038461538461538464], ['恒大苹果园', 22.80043, 108.422976, 1, 0.038461538461538464], ['江南', 22.809551, 108.40438, 1, 0.038461538461538464], ['华凯', 22.818324, 108.423162, 1, 0.038461538461538464], ['东葛路', 22.830012, 108.36001, 1, 0.038461538461538464], ['山语城', 22.81665, 108.40703, 1, 0.038461538461538464], ['五象新区', 22.770811, 108.38882, 1, 0.038461538461538464], ['莱茵湖畔', 22.81, 108.415951, 1, 0.038461538461538464]]
#         print('\n',addrXY)
        city_map = folium.Map(location=[22.808139, 108.398066],                               zoom_start=16,                               tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',attr='default' #                               tiles='http://wprd0{1-4}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7&ltype=1',attr='default' \
                             )
        tooltip ='请点击我查看该点信息'
        folium.Marker([22.808139, 108.398066], popup='快快',tooltip=tooltip).add_to(city_map)
        
        #构造热力图所需的数据结构
        lat=np.array([addrXY[i][1] for i in range(len(addrXY))],dtype=float)
        lng=np.array([addrXY[i][2] for i in range(len(addrXY))],dtype=float)
        amt=np.array([addrXY[i][3] for i in range(len(addrXY))],dtype=float)
        
        data=[[lat[i],lng[i],amt[i]] for i in range(len(addrXY))]
        HeatMap(data).add_to(city_map) #绘制热力图
        
#         data1 = [[lat[i],lon[i],pop[i]] for i in range(len(addrXY))] 
#         for addr in addrXY:
#             data=[addr[1],addr[2],addr[3]]
#             HeatMap(data).add_to(city_map)
            
        
#         for addr in addrXY:
#             folium.Marker([addr[1],addr[2]], popup=self.utf2asc(addr[0]),icon=folium.Icon(color='red')).add_to(city_map)
        print('\n标记完成，正在出图：')    
        city_map.save('temp.html')
#         display(city_map)
        webbrowser.open('temp.html')
        
    def get_lat_lng(self,kw):        
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        key='7VQBZ-OLIK6-2ERS7-EZHVL-VYQF7-EUB5M'
        url='https://apis.map.qq.com/ws/place/v1/search?keyword='+kw[0]+'&boundary=nearby(22.808139,108.398066,1000)&key='+key
        req=requests.get(url,headers=headers)
        t=req.text

        mapList=json.loads(t)
        lat,lng=mapList['data'][0]['location']['lat'],mapList['data'][0]['location']['lng']
        mapAddr=[kw[0],lat,lng,kw[1],kw[2]]

        return mapAddr
    
    def utf2asc(self,s): #正确显示中文
        return str(str(s).encode('ascii', 'xmlcharrefreplace'))[2:-1]    
    
if __name__=='__main__':
    mydata=Data('南宁五洲国际店6月1号到今天业绩数据明细.xlsx')
    addrXY=mydata.read_excel()
#     print(addrXY)
#     addrXY=['']
    mydata.drawMap(addrXY)

    

