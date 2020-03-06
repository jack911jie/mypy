# -*- coding: UTF-8 -*-
import os
import time
from tkinter import *
from tkinter.filedialog import askdirectory
import xlrd
from urllib.request import quote

def selectPath():
	path_=askdirectory()
	# path.set(path_)
	print(path_)
	path0= StringVar()
	path0.set(path_)
	Label(root, textvariable=path0).grid(row=1, column=0)
	rename(path_)

def rename(x):
	path=StringVar
	_path = askdirectory()
	path.set(_path)


	for root,dirs,files in os.walk(x):
		for file in files:
			if len(file)>14 and file[-3:]=='jpg':
				print(file)

def to_html(thename,month):
	mtoM={"1":"一月","2":"二月","3":"三月","4":"四月","5":"五月","6":"六月","7":"七月","8":"八月","9":"九月","10":"十月","11":"十一月","12":"十二月"}

	# month=input('月份：')
	# month='7'
	filepath='I:\\每周实验课_学员\\'
	filename=filepath+'2019科学实验课学员档案.xlsx'
	data = xlrd.open_workbook(filename)
	table_total = data.sheet_by_name('学员名单')
	course_total = table_total.row_values(2, 12)
	del course_total[-1]

	names = table_total.col_values(2, 3)  # 第3列，从第4行开始
	inf_basic = []
	course = []
	for n in names:
		if n == thename:
			tick_row = names.index(thename) + 3

			for j in range(12, table_total.ncols - 1):
				# print(table_total.cell(tick_row,j).value=='√')
				if table_total.cell(tick_row, j).value == '√':
					course.append([xlMonth(table_total.cell(1, j).value), table_total.cell(2, j).value])

	title_course=''
	course_to_comment=[]
	for i in course:
		if i[0]==month:
			title_course=title_course+i[1]+' | '
			course_to_comment.append(i[1])

	# print(thename,title_course)
	#判断该学员是否在该月有课程，如无，后面则不生成文件。
	if title_course:
		out_yn=1
	else:
		out_yn=0

	html_title=[mtoM[month],title_course[:-3]]

	t1 = '''<p style="color: #1e9be8;line-height: 2em;">
	                            <strong style="color: inherit;" class="135brush" data-brushtype="text">{0}月&nbsp;</strong><span style="caret-color: red;font-size: 12px;">{1}</span>
	                        </p>
		'''.format(month,html_title[1])

	#处理图片地址
	photo_path='I:\\每周实验课_学员\\'
	dir_name=photo_path+thename
	html_pic_addr=''
	_pre_pic='''
	</section>
                    <section style="color: #bfbfbf;padding-top: 10px;padding-bottom: 10px;display: inline-block;width: 100%;box-sizing: border-box;" data-width="75%">
                        <section class="_135editor" data-tools="135编辑器" data-id="95138">
                            <section class="_135editor">
                                <section style="margin: 1em auto;text-align: center;padding: 5px;border-width: 1px;border-style: solid;border-color: transparent;overflow: hidden;box-sizing: border-box;">
                                    <section class="135brush" data-style="display: inline-block;width: 100%;margin:0;padding:0;" style="white-space: nowrap;overflow-x: scroll;">
	'''
	pre_pic_addr='''
	 <img class="" data-ratio="0.75" data-type="jpeg" data-w="1200" data-width="100%" src="https://chuntianhuahua-1257410889.cos.ap-guangzhou.myqcloud.com/dzxc/
	 '''
	after_pic_addr='"/>'
	for root,dirs,files in os.walk(dir_name):
		for file in files:
			if len(file) > 5 and file[-3:] == 'jpg' :
				if file[5:7]==month.zfill(2):
					a='{0}{1}/{2}{3}'.format(pre_pic_addr.rstrip(),quote(thename),file,after_pic_addr)
					html_pic_addr=html_pic_addr+a
	html_pic_addr=_pre_pic+html_pic_addr
	# print(html_pic_addr)


	#处理课程评论
	table_exp = data.sheet_by_name('实验课内容')
	comments = table_exp.col_values(1, 1)
	cmt=''
	html_cmt=[]
	for c in course_to_comment:
		for i in comments:
			if i==c:
				# print(comments.index(c)+1)
				_cmt=table_exp.cell(comments.index(c)+1,3).value
				cmt=cmt+_cmt+'\n'
	html_cmt=cmt.split('\n')

	t2='''
								<p style="text-align:center; box-sizing: border-box; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding: 0px; font-weight: 300; color: #262626; overflow-wrap: break-word; font-size: 14px; margin-top: 0px !important; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Noto Sans&quot;, &quot;Noto Sans CJK SC&quot;, &quot;Microsoft YaHei&quot;, 微软雅黑, sans-serif;" align="center">
									<span style="font-size: 12px;color: #7f7f7f;">{0}在科学实验室里，<br/></span>
								</p>
	'''.format(mtoM[month])

	t3=''
	for html in html_cmt:
		if html:
			_t3='''
								<p style="text-align:center;box-sizing: border-box; margin: 0px; padding: 0px; font-weight: 300; color: #262626; overflow-wrap: break-word; font-size: 14px; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Noto Sans&quot;, &quot;Noto Sans CJK SC&quot;, &quot;Microsoft YaHei&quot;, 微软雅黑, sans-serif;" align="center">
									<span style="font-size: 12px;color: #7f7f7f;">{0}</span>
								</p>
			'''.format(html)
			t3=t3+_t3

	pre_t='''
	<section data-role="outer" label="Powered by 135editor.com" style="font-size:16px;">
    <section class="_135editor" data-tools="135编辑器" data-id="86457" data-color="#1e9be8" style="font-size: 16px;">
        <section class="_135editor" style="font-size: 16px;border-width: 0px;border-style: none;border-color: initial;box-sizing: border-box;" data-color="#1e9be8">
            <section style="width: 1.2em;height: 1.2em;border-radius: 100%;background-color: #1e9be8;display: inline-block;margin-top: 1em;vertical-align: top;color: #ffffff;box-sizing: border-box;"></section>
            <section style="display: inline-block;width: 95%;border-left: 1px solid #1e9be8;border-top-color: #1e9be8;border-right-color: #1e9be8;border-bottom-color: #1e9be8;margin-left: -0.66em;box-sizing: border-box;" data-width="95%">
                <section style="margin-top: 2px;color: inherit;display: inline-block;width: 100%;padding-left: 15px;box-sizing: border-box;" data-width="100%">
                    <section style="color: #bfbfbf;padding: 5px;display: inline-block;width: 100%;float: left;box-sizing: border-box;" data-width="100%">
	'''

	after_t='''
	</section>
                                    <p style="line-height:32px;margin: 10px;">
                                        <span style="font-size: 12px;">左右滑动查看更多</span>
                                    </p>
                                </section>
                            </section>
                        </section>
                    </section>
                </section>
            </section>
        </section>
    </section>
	'''
	html_text=pre_t+t1+t2+t3+html_pic_addr+after_t

	out=[thename,month,html_text,out_yn]
	# print(out)
	return out

def to_file(txt):
	# path=os.getcwd()+'\\' #要改为每个学员的文件夹
	# print(txt)
	if txt[3]==1:
		path = 'I:\\每周实验课_学员\\html\\'
		filename=path+txt[1].zfill(2)+'-'+single_get_first(txt[0][0:1]).upper()+"-"+txt[0]+'.html'
		f=open(filename,'w+')
		f.writelines(txt[2])
		print('生成文件：{0}'.format(filename))
		f.close()
	else:
		if txt[0]!='html':
			print('{0} 在 {1} 月未上课。'.format(txt[0],txt[1].zfill(2)))

def walkDir():
	path='I:\\每周实验课_学员'
	out=[]
	for root,dirs,files in os.walk(path):
		for dir in dirs:
			if dir:
				out.append(dir)
	return out

def xlDate(date):
	d=xlrd.xldate_as_tuple(date,0)
	#dd=str(d[0])+'-'+str(d[1])+'-'+str(d[2])
	dd = str(d[1]) + '月' + str(d[2])+ '日'
	return dd

def xlMonth(date):
	d=xlrd.xldate_as_tuple(date,0)
	#dd=str(d[0])+'-'+str(d[1])+'-'+str(d[2])
	dd = str(d[1])
	return dd

def main():
	root = Tk()  # 创建窗口对象的背景色
	path = StringVar()
	# Entry(root,textvariable=path).grid(row=0,column=1)
	Button(root,text='请选择文件夹',command=selectPath).grid(row=0,column=0)
	Button(root,text='改名',command=rename).grid(row=0,column=1)
	# root.mainloop()

def do_html():
	month=input('输入月份：')
	dirs=walkDir()
	for dir in dirs:
		txt=to_html(dir,month)
		to_file(txt)

def single_get_first(unicode1):
	str1 = unicode1.encode('gbk')
	# print(len(str1))
	try:
		ord(str1)
		return str1
	except:
		asc = str1[0] * 256 + str1[1] - 65536
		# print(asc)
		if asc >= -20319 and asc <= -20284:
			return 'a'
		if asc >= -20283 and asc <= -19776:
			return 'b'
		if asc >= -19775 and asc <= -19219:
			return 'c'
		if asc >= -19218 and asc <= -18711:
			return 'd'
		if asc >= -18710 and asc <= -18527:
			return 'e'
		if asc >= -18526 and asc <= -18240:
			return 'f'
		if asc >= -18239 and asc <= -17923:
			return 'g'
		if asc >= -17922 and asc <= -17418:
			return 'h'
		if asc >= -17417 and asc <= -16475:
			return 'j'
		if asc >= -16474 and asc <= -16213:
			return 'k'
		if asc >= -16212 and asc <= -15641:
			return 'l'
		if asc >= -15640 and asc <= -15166:
			return 'm'
		if asc >= -15165 and asc <= -14923:
			return 'n'
		if asc >= -14922 and asc <= -14915:
			return 'o'
		if asc >= -14914 and asc <= -14631:
			return 'p'
		if asc >= -14630 and asc <= -14150:
			return 'q'
		if asc >= -14149 and asc <= -14091:
			return 'r'
		if asc >= -14090 and asc <= -13119:
			return 's'
		if asc >= -13118 and asc <= -12839:
			return 't'
		if asc >= -12838 and asc <= -12557:
			return 'w'
		if asc >= -12556 and asc <= -11848:
			return 'x'
		if asc >= -11847 and asc <= -11056:
			return 'y'
		if asc >= -11055 and asc <= -10247:
			return 'z'
		return ''

do_html()