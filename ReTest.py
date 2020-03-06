import requests,json

def get_json():
    json_url=r'https://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
    re=requests.get(json_url)
    with open('down_load_json.json','w') as f:
        f.write(re.text)
    file_req=re.json()


numbers = {'a':1,'b':2,'c':3,'d':4}
filename = 'numbers.json'
# with open(filename, 'w') as f_obj:
#     json.dump(numbers, f_obj)

with open(filename,'r') as f_read:
    f=json.load(f_read)
    print(type(f))
    for k in f.values():
        print(k)
