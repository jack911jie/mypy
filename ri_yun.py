#!/usr/bin/env python
# coding: utf-8

# In[52]:


import os
import time
import copy
import random
import logging
import pandas as pd

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(funcName)s-%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

class riyun:
    def __init__(self,GZ):
        self.GZ=GZ    
        self.wx={'甲':'阳木','乙':'阴木','丙':'阳火','丁':'阴火','戊':'阳土',                  '己':'阴土','庚':'阳金','辛':'阴金','壬':'阳水','癸':'阴水',                  '子':'阳水','丑':'阴土','寅':'阳木','卯':'阴木',                  '辰':'阳土','巳':'阳火','午':'阴火','未':'阴土',                  '申':'阳金','酉':'阴金','戌':'阳土','亥':'阴水'}   
        self.wxSheng=[['木','火'],['火','土'],['土','金'],['金','水'],['水','木']]
        self.wxKe=[['木','土'],['火','金'],['土','水'],['金','木'],['水','火']]
        
#         S00 食伤驾杀
#         S01 伤官见官
#         S02 食伤生财
#         S03 枭印夺食
#         S04 比劫生食伤
#         S05 比劫克财
#         S06 财破印
#         S07 财生官
#         S08 官生印
#         S09 印生比劫
        self.geju=self.GeJu()
        self.rel_name=['食伤驾杀','伤官见官','食伤生财','枭印夺食','比劫生食伤',                        '比劫克财','财破印','财生官','官生印','印生比劫']
        self.txt_addr=os.path.join(os.getcwd(),'日运语句数据库2.0.xlsx')
        
    #写日运
    def write_RiYun(self):
        def read_excel_1(): #1.0版本的数据库，不区分官杀等
            txt_GeJu=pd.read_excel(self.txt_addr,sheet_name=0)        
            txt_mu=pd.read_excel(self.txt_addr,sheet_name=2)

            txt_rels=pd.read_excel(self.txt_addr,sheet_name=1,skiprows=2)
            txt_rels_Chong=txt_rels.iloc[:,0:10]
    #         txt_rels_He.columns = ['比劫-财','食伤-官杀', '财-印','官杀-比劫', \
    #                                 '印-食伤','比劫-比劫','食伤-食伤','财-财', \
    #                                 '官杀-官杀','印-印']

            txt_rels_He=txt_rels.iloc[:,10:15]
            txt_rels_He.columns = ['比劫-财','食伤-官杀','财-印枭','官杀-比劫','印枭-食伤']      


            txt_rels_Hai=txt_rels.iloc[:,15:25]
            txt_rels_Hai.columns=['比劫-财','比劫-官杀','食伤-官杀','食伤-印枭','财-印枭','比劫-印枭','比劫-食伤','食伤-财','财-官杀','官杀-印枭']

            txt_rels_Xing=txt_rels.iloc[:,25:]
            txt_rels_Xing.columns=['比劫-食伤-官杀','食伤-财-印枭','财-官杀-比劫','官杀-印枭-食伤','印枭-比劫-财',                                    '比劫-比劫-比劫', '食伤-食伤-食伤','财-财-财','官杀-官杀-官杀','印枭-印枭-印枭',                                     '比劫-食伤','食伤-财','财-官杀','官杀-印枭','比劫-印枭',                                     '比劫-比劫','食伤-食伤','财-财','官杀-官杀','印枭-印枭']        
            return [txt_GeJu,txt_mu,txt_rels,txt_rels_Chong,txt_rels_He,txt_rels_Hai,txt_rels_Xing]
        
        def read_excel_2(): #1.0版本的数据库，区分官杀等
            txt_GeJu=pd.read_excel(self.txt_addr,sheet_name='常见格局（生克）',skiprows=1)        
            txt_mu=pd.read_excel(self.txt_addr,sheet_name='墓',skiprows=1)
            txt_rels=[]
            txt_rels_Chong=pd.read_excel(self.txt_addr,sheet_name='冲',skiprows=1)
            txt_rels_He=pd.read_excel(self.txt_addr,sheet_name='合',skiprows=1)
            txt_rels_Hai=pd.read_excel(self.txt_addr,sheet_name='害',skiprows=1)
            txt_rels_Xing=pd.read_excel(self.txt_addr,sheet_name='刑',skiprows=2)
  

       
            return [txt_GeJu,txt_mu,txt_rels,txt_rels_Chong,txt_rels_He,txt_rels_Hai,txt_rels_Xing]       
                
        def exp_geju():        
            #--------------------------------格局语句  --------------------------------   

            #必须先运行，否则后面的入墓及冲合害刑无数据来源
            geju=self.GeJu_out()
            logger.info(self.GZ)     

            for gj in geju[1]:              
                t=txt_GeJu[gj].iloc[random.randint(0,txt_GeJu[gj].count()-1)]
                logger.info(''.join([gj,'：',str(t)]))            
    #             print(gj,'：',t)            
                out_txt.append(gj+'：'+str(t))
            
        def exp_mu():
            #--------------------------------入墓语句--------------------------------
            mu=self.Mu()
            _mu=[]
            for m in mu:
                if m=='偏财' or m=='正财':
                    _mu.append('财')

                if m=='正官' or m=='七杀':
                    _mu.append('官杀')

                if m=='食神' or m=='伤官':
                    _mu.append('财')

                if m=='正印' or m=='偏印':
                    _mu.append('印枭')

                if m=='比肩' or m=='劫财':
                    _mu.append('财')
            Mu_wx=list(set(_mu))

            for mu_wx in Mu_wx:
                t=txt_mu[mu_wx].iloc[random.randint(0,txt_mu[mu_wx].count()-1)]
                logging.info(''.join([mu_wx,'入墓：',str(t)]))
    #             print(mu_wx+'入墓：',t)

                out_txt.append(mu_wx+'入墓：'+str(t))
        
        def exp_C_H_H_X():            
                #--------------------------------冲合害刑语句--------------------------------
            rels=self.relToSs()    
    #         rels_ren=self.replace_elements(rels)  #将食神伤官合并为食伤，官、杀合并为官杀，正偏财合并为财。。。
            rels_ren=rels

            title_Chong=self.split_title(txt_rels_Chong.columns.values.tolist())
            title_He=self.split_title(txt_rels_He.columns.values.tolist())
            title_Hai=self.split_title(txt_rels_Hai.columns.values.tolist())
            title_Xing=self.split_title(txt_rels_Xing.columns.values.tolist())
            titles=[title_Chong,title_He,title_Hai,title_Xing]            


            num=0     
            txt_chong=[]
            txt_he=[]
            txt_hai=[]
            txt_xing=[]
            txt_xing_3=[]
            txt_xing_2=[]
            txt_xing_1=[]


            for INF in rels_ren:
                for info in INF:
                    t=''.join(info)
                    logging.info(t)

            for r in rels_ren:
                if r:
                    for rr in r:                    
                        if num==0 or num==3:  # 天干冲 或 地支冲
                            m=0                        
                            for t in titles[0]:
                                if len(list(set(rr).intersection(set(t))))==2:
                                    temp_t=txt_rels_Chong.iloc[:,m][random.randint(0,txt_rels_Chong.iloc[:,m].count()-1)]
                                    txt_chong.append(rr[0]+'-'+rr[1]+' 冲：'+str(temp_t))
                                m+=1

                        if num==2 or num==6 or num==7:  # 天干合 或 地支六合
                            m=0
                            for t in titles[1]:
                                if len(list(set(rr).intersection(set(t))))==2 :                                
                                    temp_t=txt_rels_He.iloc[:,m][random.randint(0,txt_rels_He.iloc[:,m].count()-1)]
                                    txt_he.append(rr[0]+'-'+rr[1]+' 合：'+str(temp_t))
                                m+=1

                        if num==4:  # 地支害
                            m=0
                            for t in titles[2]:
                                if len(list(set(rr).intersection(set(t))))==2:   
                                    temp_t=txt_rels_Hai.iloc[:,m][random.randint(0,txt_rels_Hai.iloc[:,m].count()-1)]
                                    txt_hai.append(rr[0]+'-'+rr[1]+' 害：'+str(temp_t))
                                m+=1

                        if num==5:  # 地支三刑  刑的地支是完全互斥的，完成一个后，就可以break
                            m=0
                            for t in titles[3]:
                                if len(t)==3 :
                                    if rr==t and t[0]==t[1]==t[2]:
                                        temp_t=txt_rels_Xing.iloc[:,m][random.randint(0,txt_rels_Xing.iloc[:,m].count()-1)]
                                        txt_xing.append(rr[0]+'-'+rr[1]+'-'+rr[2]+' 三刑：'+str(temp_t))
                                    else:
                                        if len(list(set(rr).intersection(set(t))))==3 :   #三刑
                                            temp_t=txt_rels_Xing.iloc[:,m][random.randint(0,txt_rels_Xing.iloc[:,m].count()-1)]
                                            txt_xing.append(rr[0]+'-'+rr[1]+'-'+rr[2]+' 三刑：'+str(temp_t))
                                            break
                                elif len(t)==2:                           
                                    if rr==t and t[0]==t[1]: #自刑
                                        temp_t=txt_rels_Xing.iloc[:,m][random.randint(0,txt_rels_Xing.iloc[:,m].count()-1)]
                                        txt_xing.append(rr[0]+'-'+rr[1]+' 自刑：'+str(temp_t)) 
                                    if len(list(set(rr).intersection(set(t))))==2:   #相刑
                                        temp_t=txt_rels_Xing.iloc[:,m][random.randint(0,txt_rels_Xing.iloc[:,m].count()-1)]
                                        txt_xing.append(rr[0]+'-'+rr[1]+' 相刑：'+str(temp_t))  
                                        break                           
                                m+=1
                num+=1

            list_C_H_H_X=[txt_chong,txt_he,txt_hai,txt_xing]        
            txt_C_H_H_X=[]
            for t in list_C_H_H_X:
                 txt_C_H_H_X.extend(self.remove_empty(t))

            out_txt.extend(txt_C_H_H_X)
            
        def exp_3he():
            DZ_3He=self.dz_3he()
            if DZ_3He:
                t='-'.join(DZ_3He[0])+" 三合"
                out_txt.append(t)
        
        def exp_3hui():
            #--------------------------------三会语句--------------------------------
            DZ_3Hui=self.dz_3hui()
            if DZ_3Hui:
                t='-'.join(DZ_3Hui[0])+" 三会"
                out_txt.append(t)

            logging.info('  '.join(out_txt))
            
        para=read_excel_2()
        txt_GeJu,txt_mu,txt_rels,txt_rels_Chong,txt_rels_He,txt_rels_Hai,txt_rels_Xing             = para[0],para[1],para[2],para[3],para[4],para[5],para[6]
        
        
        out_txt=[]
        exp_geju()
        exp_mu()
        exp_C_H_H_X()
        exp_3he()
        exp_3hui()
        
        return out_txt    
            
    #天干冲
    def tg_chong(self):
        h1=['甲','庚']
        h2=['乙','辛']
        h3=['丙','壬']
        h4=['丁','癸']
        H=[h1,h2,h3,h4]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==2:
#                 print(h[0],h[1],'冲')
                logger.info(''.join([h[0],h[1],'冲']))
                out.append([h[0],h[1]])
        return out        
                
    #天干克
    def tg_ke(self):
        #天干相克： 庚克甲，辛克乙，壬克丙，癸克丁。
        h1=['甲','庚']
        h2=['乙','辛']
        h3=['丙','壬']
        h4=['丁','癸']
        H=[h1,h2,h3,h4]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==2:
#                 print(h[1],'克',h[0])
                logger.info(''.join([h[1],'克',h[0]]))
                out.append([h[1],h[0]])
        return out
                
    # 天干合
    def tg_he(self):
        h1=['甲','己']
        h2=['乙','庚']
        h3=['丙','辛']
        h4=['丁','壬']
        h5=['戊','癸']        
        H=[h1,h2,h3,h4,h5]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==2:
#                 print(h[0],h[1],'合')
                logger.info(''.join([h[0],h[1],'合']))
                out.append([h[0],h[1]])
        return out
                
    #地支冲
    def dz_chong(self):
        #地支六冲： 子午相冲，卯酉相冲，寅申相冲， 已亥相冲，辰戌相冲，丑未相冲
        h1=['子','午']
        h2=['卯','酉']
        h3=['寅','申']
        h4=['巳','亥']
        h5=['辰','戌']
        h6=['丑','未']
        H=[h1,h2,h3,h4,h5,h6]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==2:
#                 print(h[0],h[1],'冲')
                logger.info(''.join([h[0],h[1],'冲']))
                out.append([h[0],h[1]])
        return out
                
    #地支害
    def dz_hai(self):
        #地支相害:未相害 丑午相害 寅巳相害 卯辰相害 申亥相害 戌酉相害
        h1=['子','未']
        h2=['丑','午']
        h3=['寅','巳']
        h4=['卯','辰']
        h5=['申','亥']
        h6=['戌','酉']
        H=[h1,h2,h3,h4,h5,h6]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==2:
#                 print(h[0],h[1],'相害')
                logger.info(''.join([h[0],h[1],'相害']))
                out.append([h[0],h[1]])
        return out
    
    #地支刑
    def dz_xing(self):
        #地支相刑:寅巳申三刑 丑戌未三刑 子卯相刑 辰、酉、午、亥自刑
        h1=['寅','巳','申']
        h2=['丑','戌','未']
        h3=['子','卯']

        H=[h1,h2]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==3:                
#                 print(h[0],h[1],h[2],'三刑')
                logger.info(''.join([h[0],h[1],h[2],'三刑']))
                out.append([h[0],h[1],h[2]])
                
        if len(list(set(h3).intersection(set(self.GZ))))==2:
#             print(h3[0],h3[1],'相刑')  
            out.append([h3[0],h3[1]])
                
        c=[]
        for h in self.GZ:
            if h=='辰':
                c.append(h)
        if len(c)>=2:
#             print('辰辰自刑')
            out.append(['辰','辰'])
            
        c=[]
        for h in self.GZ:
            if h=='酉':
                c.append(h)
        if len(c)>=2:
#             print('酉酉自刑')
            out.append(['酉','酉'])
            
        c=[]
        for h in self.GZ:
            if h=='午':
                c.append(h)
        if len(c)>=2:
#             print('午午自刑')
            out.append(['午','午'])
            
        c=[]
        for h in self.GZ:
            if h=='亥':
                c.append(h)
        if len(c)>=2:
#             print('亥亥自刑')    
            out.append(['亥','亥'])
                
        return out
    
    #地支三合
    def dz_3he(self):
        #地支三合局： 申子辰三合水局，亥卯未三合木局， 寅午戌三合火局，巳酉丑三合金局
        h1=['申','子','辰']
        h2=['亥','卯','未']
        h3=['寅','午','戌']
        h4=['巳','酉','丑']

        H=[h1,h2,h3,h4]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==3:
#                 print(h[0],h[1],h[2],'三合')
                logger.info(''.join([h[0],h[1],h[2],'三合']))
                out.append([h[0],h[1],h[2]])
        return out
    
    #地支六合
    def dz_6he(self):
        #地支六合： 子丑合土，寅亥合木，戌卯合火，辰酉合金，巳申合水，午未合火
        h1=['子','丑']
        h2=['寅','亥']
        h3=['戌','卯']
        h4=['辰','酉']
        h5=['巳','申']
        h6=['午','未']
        
        H=[h1,h2,h3,h4,h5,h6]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==2:
#                 print(h[0],h[1],'六合')
                logger.info(''.join([h[0],h[1],'六合']))
                out.append([h[0],h[1]])
        return out
                
    #地支三会    
    def dz_3hui(self):
        #地支三会局： 申酉戌三会金局. 寅卯辰三会木局. 亥子丑三会水局. 巳午未三会火局.
        h1=['申','酉','戌']
        h2=['寅','卯','辰']
        h3=['亥','子','丑']
        h4=['巳','午','未']

        H=[h1,h2,h3,h4]
        out=[]
        for h in H:
            if len(list(set(h).intersection(set(self.GZ))))==3:
#                 print(h[0],h[1],h[2],'三会')
                logger.info(''.join([h[0],h[1],h[2],'三会']))
                out.append([h[0],h[1],h[2]])
        return out
                
    #干支转为十神
    def GeJu_out(self):
        todayGZ=[self.GZ[0],self.GZ[1],self.GZ[2],self.GZ[3],self.GZ[4],self.GZ[5]]
        rz=self.GZ[6] #日主       
            
        rel=[]
        for gz in todayGZ:
            temp=[self.wx[rz][1],self.wx[gz][1]]
#             print(gz+self.wx[gz][1])
            
            if self.wx[gz][1]==self.wx[rz][1]:
                if self.wx[gz][0]==self.wx[rz][0]:
#                     print(self.wx[gz],'同',self.wx[rz],'比肩')
                    rel.append('比肩')
                else:
#                     print(self.wx[gz],'同',self.wx[rz],'劫财')
                    rel.append('劫财')
            else:       
                for h in self.wxSheng:
                    if len(list(set(temp).intersection(set(h))))==2:
                        if h[0]==self.wx[rz][1]: #我生
                            if self.wx[gz][0]==self.wx[rz][0]: #同性
#                                 print(self.wx[rz],'生',self.wx[gz][0]+h[1],'食神')
                                rel.append('食神')
                            else: #异性
#                                 print(self.wx[rz],'生',self.wx[gz][0]+h[1],'伤官')
                                rel.append('伤官')
                                
                        if h[1]==self.wx[rz][1]: #生我
                            if self.wx[gz][0]==self.wx[rz][0]: #同性
#                                 print(self.wx[gz][0]+h[0],'生',self.wx[rz],'偏印')
                                rel.append('偏印')
                            else: #异性
#                                 print(self.wx[gz][0]+h[0],'生',self.wx[rz],'正印')
                                rel.append('正印')
                            
                for k in self.wxKe:
                    if len(list(set(temp).intersection(set(k))))==2:
                        if k[0]==self.wx[rz][1]: #我克
                            if self.wx[gz][0]==self.wx[rz][0]: #同性
#                                 print(self.wx[rz],'克',self.wx[gz][0]+k[1],'偏财')
                                rel.append('偏财')
                            else: #异性
#                                 print(self.wx[rz],'克',self.wx[gz][0]+k[1],'正财')
                                rel.append('正财')
                                
                        if k[1]==self.wx[rz][1]: #克我
                            if self.wx[gz][0]==self.wx[rz][0]: #同性
#                                 print(self.wx[gz][0]+k[0],'克',self.wx[rz],'七杀')
                                rel.append('七杀')
                            else: #异性
#                                 print(self.wx[gz][0]+k[0],'克',self.wx[rz],'正官')
                                rel.append('正官')
                    
#         print(rel)
        
        num=0
        rel_GeJu=[]
        for g in self.geju:
            for gg in g:
                if len(list(set(gg).intersection(set(rel))))==2:
#                     print(self.rel_name[num])
                    rel_GeJu.append(self.rel_name[num])
            num+=1      
#         print(list(set(rel_GeJu)))    
        
        self.rel=rel  
        return [self.rel,list(set(rel_GeJu))]
            
    #冲克合刑害会 等关系转十神
    def relToSs(self):  
        out=[]
        
        #1.天干冲 转为十神
        tgChong=self.tg_chong()
#         print(tgChong)
        ss_TGChong=[]
        for WX in tgChong:
            _ss=[]
            for wx in WX:
                try:
                    _ss.append(self.rel[self.GZ.index(wx)])
                except:
                    _ss.append('日主')
            ss_TGChong.append(_ss)
#         print(ss_TGChong)
        out.append(ss_TGChong)
        
        #2.天干克 转为十神
        tgKe=self.tg_ke()
#         print(tgKe)
        ss_TGKe=[]
        for WX in tgKe:
            _ss=[]
            for wx in WX:
                try:
                    _ss.append(self.rel[self.GZ.index(wx)])
                except:
                    _ss.append('日主')
            ss_TGKe.append(_ss)
#         print(ss_TGKe)
        out.append(ss_TGKe)
        
        #3.天干合 转为十神
        tgHe=self.tg_he()
#         print(tgHe)
        ss_TGHe=[]
        for WX in tgHe:
            _ss=[]
            for wx in WX:
                try:
                    _ss.append(self.rel[self.GZ.index(wx)])
                except:
                    _ss.append('日主')
            ss_TGHe.append(_ss)
#         print(ss_TGHe)
        out.append(ss_TGHe)
        
        #4.地支冲 转为十神
        dzChong=self.dz_chong()
#         print(dzChong)    
        ss_DZChong=[]
        for WX in dzChong:
            _ss=[]
            for wx in WX:
                _ss.append(self.rel[self.GZ.index(wx)])
            ss_DZChong.append(_ss)
#         print(ss_DZChong)
        out.append(ss_DZChong)
        
        #5.地支害 转为十神
        dzHai=self.dz_hai()
#         print(dzHai)    
        ss_DZHai=[]
        for WX in dzHai:
            _ss=[]
            for wx in WX:
                _ss.append(self.rel[self.GZ.index(wx)])
            ss_DZHai.append(_ss)
#         print(ss_DZHai)
        out.append(ss_DZHai)
        
        #6.地支刑 转为十神
        dzXing=self.dz_xing()
#         print(dzXing)    
        ss_DZXing=[]
        for WX in dzXing:
            _ss=[]
            for wx in WX:
                _ss.append(self.rel[self.GZ.index(wx)])
            ss_DZXing.append(_ss)
#         print(ss_DZXing)
        out.append(ss_DZXing)
        
        #7.地支三合 转为十神
        dz3he=self.dz_3he()
#         print(dz3he)    
        ss_DZ3he=[]
        for WX in dz3he:
            _ss=[]
            for wx in WX:
                _ss.append(self.rel[self.GZ.index(wx)])
            ss_DZ3he.append(_ss)
#         print(ss_DZ3he)
        out.append(ss_DZ3he)
        
        #8.地支六合 转为十神
        dz6he=self.dz_6he()
#         print(dz6he)    
        ss_DZ6he=[]
        for WX in dz6he:
            _ss=[]
            for wx in WX:
                _ss.append(self.rel[self.GZ.index(wx)])
            ss_DZ6he.append(_ss)
#         print(ss_DZ6he)
        out.append(ss_DZ6he)
        
        #9.地支三会 转为十神
        dz3hui=self.dz_3hui()
#         print(dz3he)    
        ss_DZ3hui=[]
        for WX in dz3hui:
            _ss=[]
            for wx in WX:
                _ss.append(self.rel[self.GZ.index(wx)])
            ss_DZ3hui.append(_ss)
#         print(ss_DZ3hui)   
        out.append(ss_DZ3hui)
        
#         print(out)
        return out
    
    #墓
    def Mu(self):
        #辰为水库，戌为火库，丑为金库，未为木库
        todayGZ=[self.GZ[0],self.GZ[1],self.GZ[2],self.GZ[3],self.GZ[4],self.GZ[5]]
        rz=self.GZ[6]        
        out=[]
        if '未' in todayGZ :
            num=0
            for mu in todayGZ:
                if mu=='甲' or mu=='乙' or mu=='寅' or mu=='卯':
#                     print(mu,self.rel[num])
                    out.append(self.rel[num])
                num+=1
                
        if '戌' in todayGZ :
            num=0
            for mu in todayGZ:
                if mu=='丙' or mu=='丁' or mu=='巳' or mu=='午':
#                     print(mu,self.rel[num])
                    out.append(self.rel[num])
                num+=1
                
        if '丑' in todayGZ :
            num=0
            for mu in todayGZ:
                if mu=='庚' or mu=='辛' or mu=='申' or mu=='酉':
#                     print(mu,self.rel[num])
                    out.append(self.rel[num])
                num+=1
                
        if '辰' in todayGZ :
            num=0
            for mu in todayGZ:
                if mu=='壬' or mu=='癸' or mu=='亥' or mu=='壬':
#                     print(mu,self.rel[num])
                    out.append(self.rel[num])
                num+=1
        return out    
     
    #格局基本数据
    def GeJu(self):
        #几大关系:食神（伤官）驾杀、食伤生财、枭印夺食、比劫生食伤、比劫克财、财破印、财生官、官生印、印生比劫
        
        #食伤-官杀
        ShenS_01=['食神','正官']        
        ShenS_02=['伤官','正官']
        ShenS_03=['食神','七杀']
        ShenS_04=['伤官','七杀']
        
        #食伤-财
        ShenS_05=['食神','正财']
        ShenS_06=['食神','偏财']
        ShenS_07=['伤官','正财']
        ShenS_08=['伤官','偏财']
        
        #枭印-食伤
        ShenS_09=['正印','食神']
        ShenS_10=['偏印','食神']
        ShenS_11=['正印','伤官']
        ShenS_12=['偏印','伤官']
        
        #比劫-食伤
        ShenS_13=['比肩','食神']
        ShenS_14=['劫财','食神']
        ShenS_15=['比肩','伤官']
        ShenS_16=['劫财','伤官']
        
        #比劫-财
        ShenS_17=['比肩','正财']
        ShenS_18=['劫财','正财']
        ShenS_19=['比肩','偏财']
        ShenS_20=['劫财','偏财']

        #财-印
        ShenS_21=['正财','正印']
        ShenS_22=['偏财','正印']
        ShenS_23=['正财','偏印']
        ShenS_24=['偏财','偏印']
        
        #财-官
        ShenS_25=['正财','正官']
        ShenS_26=['偏财','正官']
        ShenS_27=['正财','七杀']
        ShenS_28=['偏财','七杀']

        #官-印
        ShenS_29=['正官','正印']
        ShenS_30=['七杀','正印']
        ShenS_31=['正官','偏印']
        ShenS_32=['七杀','偏印']
        
        #印-比劫
        ShenS_33=['正印','比肩']
        ShenS_34=['偏印','比肩']
        ShenS_35=['正印','劫财']
        ShenS_36=['偏印','劫财']
        
        #食伤驾杀
        S00=[ShenS_03,ShenS_04]
        
        #伤官见官
        S01=[ShenS_02]
        
        #食伤生财
        S02=[ShenS_05,ShenS_06,ShenS_07,ShenS_08]
        
        #枭印夺食
        S03=[ShenS_09,ShenS_10]
        
        #比劫生食伤
        S04=[ShenS_13,ShenS_14,ShenS_15,ShenS_16]
        
        #比劫克财
        S05=[ShenS_17,ShenS_18,ShenS_19,ShenS_20]
        
        #财破印
        S06=[ShenS_21,ShenS_22,ShenS_23,ShenS_24]
        
        #财生官
        S07=[ShenS_25,ShenS_26,ShenS_27,ShenS_28]
        
        #官生印
        S08=[ShenS_29,ShenS_30,ShenS_31,ShenS_32]
        
        #印生比劫
        S09=[ShenS_33,ShenS_34,ShenS_35,ShenS_36]
        
        return [S00,S01,S02,S03,S04,S05,S06,S07,S08,S09]       
            
    #将列名中的“-”去掉并组合成列表
    def split_title(self,c):
        out=[]
        for c_name in  c:
            out.append(c_name.split('-'))
        return out
    
    #将食伤、伤官等合并为“食伤”
    def replace_elements(self,a):
        c=copy.deepcopy(a)
        n=0
        for cc in c:
            m=0
            for ccc in cc:
                k=0
                for cccc in ccc:
                    if cccc=='食神' or cccc=='伤官':
                        c[n][m][k]='食伤'                        
                    if cccc=='正印' or cccc=='偏印':
                        c[n][m][k]='印枭'
                    if cccc=='正财' or cccc=='偏财':
                        c[n][m][k]='财'
                    if cccc=='正官' or cccc=='七杀':
                        c[n][m][k]='官杀'
                    if cccc=='比肩' or cccc=='劫财':
                        c[n][m][k]='比劫'

                    k+=1
                m+=1
            n+=1
        return c
    
    def remove_empty(self,TXTs):
        out=[]
        for t in TXTs:
            if t:
                out.append(t)
                break #有多个结果时候，只要一个，停止循环。
        return out

def write_10_tg():
    fmt_time=time.strftime("%Y-%m-%d", time.localtime())
    today=input('请输入本日干支：')
#     today='庚子戊辰壬申'
    if today:
        k=list(today)
        k.append('x')    
        tgX10=['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
#         tgX10=['甲','乙']
        print(k)
        
        for tg in tgX10:
            k[6]=tg
            ri=riyun(k)
            txt=tg+'：\n'+'\n'.join(ri.write_RiYun())
            txt=txt+'\n\n'            
            
            print(txt)        
            with open(os.path.join(os.getcwd(),fmt_time+' 日运.txt'),'a+') as f:
                f.write(txt)
                
        input('完成，按回车退出。')
        
    else:
        print('未输入，退出。')
        pass    
    
        
if __name__=='__main__':
    write_10_tg()
    


# 天干： 甲、乙、丙、丁、戊、已、庚、辛、壬、癸 
# 地支： 子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥
# 
# 地支三会局：
# 申酉戌三会金局. 
# 寅卯辰三会木局. 
# 亥子丑三会水局. 
# 巳午未三会火局.
# 
# 天干相冲：
# 甲庚冲，乙辛冲，丙壬冲，丁癸冲
# 
# 
# 天干相克：
# 庚克甲，辛克乙，壬克丙，癸克丁。
# 
# 天干合化
# 甲己合化土，乙庚合化金，丙辛合化水，丁壬合化木，戊癸合化火
# 
# 地支六冲：
# 子午相冲，卯酉相冲，寅申相冲， 已亥相冲，辰戌相冲，丑未相冲
# 
# 地支相害
# 子未相害
# 丑午相害
# 寅巳相害
# 卯辰相害
# 申亥相害
# 戌酉相害
# 
# 地支相刑
# 寅巳申三刑
# 丑戌未三刑
# 子卯相刑
# 辰、酉、午、亥自刑
# 
# 
# 地支三合局：
# 申子辰三合水局，亥卯未三合木局， 寅午戌三合火局，巳酉丑三合金局
# 
# 地支六合：
# 子丑合土，寅亥合木，戌卯合火，辰酉合金，巳申合水，午未合火
# 五行四方：东方属木，南方属火，西方属金，北方属水，中央属土。
# 
# 几种常见关系：
# 
# 食神（伤官）驾杀、食伤生财、枭印夺食、比劫生食伤、比劫克财、财破印、财生官、官生印、印生比劫、墓神的关系（辰戌丑未四个库，对于天干地支相对应五行出现时候的影响）
# 
# （这些关系在同柱之间、在地支之间、在天干之间，都需要考虑）
