#!/usr/bin/env python
# coding: utf-8

# In[12]:


import datetime

def calculate_age(birth_s='20181215'):
    birth_d = datetime.datetime.strptime(birth_s, "%Y%m%d")
    today_d = datetime.datetime.now()
    birth_t = birth_d.replace(year=today_d.year)
    if today_d > birth_t:
        age = today_d.year - birth_d.year
    else:
        age = today_d.year - birth_d.year - 1
    return age


def calculate_days(date_input='20181215'):
    today=datetime.datetime.now()
    date_s = datetime.datetime.strptime(date_input, "%Y%m%d")    
    return (today-date_s).days

