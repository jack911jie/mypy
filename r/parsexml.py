import xml.etree.cElementTree as et
import re

def parsexml():
    tree=et.parse('/home/jack/data/r/rpPaper/family/GSE73731_family.xml')
    root=tree.getroot()
    ptn='GSM193\d*'
    out=[]
    for box in root:    
        if re.match(ptn,box.attrib['iid']):
        # if box.attrib['iid']=='GSM1930996':
            gsm=[]
            gsm.append(box.attrib['iid'])
            for ctn in box.iter('{http://www.ncbi.nlm.nih.gov/geo/info/MINiML}Source'):
                if ctn.text:
                    gsm.append(ctn.text.strip())
            for ctn in box.iter('{http://www.ncbi.nlm.nih.gov/geo/info/MINiML}Characteristics'):
                if ctn.text:
                    gsm.append(ctn.text.strip())
            # print(gsm)
            out.append(','.join(gsm))
    print(out)

    with open ('/home/jack/data/r/rpPaper/family.csv','w',encoding='utf-8') as f:
        f.write('\n'.join(out))

def rmdata():
    fn='/home/jack/data/r/rpPaper/shortRes4.csv'
    with open (fn,'r',encoding='utf-8') as f:
        lns=f.readlines()
        ptn=r'_Sample_\d*.CEL.gz'
        lns[0]=re.sub(ptn,'',lns[0])
        print(lns[0])
    
    with open('/home/jack/data/r/rpPaper/shortRes4_2.csv','a',encoding='utf-8') as ff:
        for ln in lns:
            ff.write(ln)

rmdata()