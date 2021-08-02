import os
import csv
from posixpath import dirname
import re
import pandas as pd
from PIL import Image

#将照片改为5m以下大小，以适应notion的需要
class Pic_size:
    def __init__(self):
        pass

    def judge_size(self,img_src,thresh_hold=5):
        thresh_hold=thresh_hold*1024*1024
        size=os.path.getsize(img_src)
        if size>thresh_hold:
            return 'bigger' 
        else:
            return 'smaller'
        
    def reduce_pic_file_size(self,dir):
        for fn in os.listdir(dir):
            if fn[-3:].lower()=='jpg' or fn[-4:].lower()=='jpeg':
                print('正在处理：{}'.format(fn))
                jpg=os.path.join(dir,fn)
                img=Image.open(jpg)
                size=os.path.getsize(jpg)
                diff_res=self.judge_size(jpg,thresh_hold=5)
                n=1
                while diff_res=='bigger':
                    print('第{}次压缩'.format(n))
                    img=img.resize((int((img.size[0]*0.95)),int(img.size[1]*img.size[0]*0.95/img.size[0])),Image.ANTIALIAS)
                    save_temp=jpg[0:-3]+'_temp.jpg'
                    img.save(save_temp,quality=90,subsampling=0)
                    n+=1
                    diff_res=self.judge_size(save_temp)
                    os.remove(save_temp)
                img.save(jpg,quality=90,subsampling=0)
                print('完成')

if __name__=='__main__':
    dir='D:\\photo\\20210425路飞生日'
    p=Pic_size()
    p.reduce_pic_file_size(dir=dir)