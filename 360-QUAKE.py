#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import sys
version = sys.version_info
if version < (3, 0):
    print('The current version is not supported, you need to use python3+')
    sys.exit()
import json
import os
import datetime
nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
nowtime='result-'+str(nowtime).replace(' ','-').replace(':','-')+'.txt'
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
ttt = """360-QUAKE-API批量查询工具 v1.0
作者微信：TWluR2Vla3k=
"""
print(ttt)




email = '123@qq.com'#账号，可不填
key = 'sxxxxx'   #360  API KEY：
maxcount=10000  #100~10000， 每次最多检索数量，积分多可忽略



headers = {'Content-Type': 'application/json',"X-QuakeToken": key}
count=0
starts=0
text=str(input('请输入查询语法：'))
open(nowtime,'a',encoding='utf-8').write(text+'\n')
keyword=text
while True:
    try:
        data = {"query": keyword, "start": starts, "size": 100}
        url = 'https://quake.360.cn/api/v3/search/quake_service'
        req = requests.post(url,data=json.dumps(data),verify=False,headers=headers,timeout=50)
        rsp = json.loads(req.text)
        #print(rsp)
        starts=starts+100
        if len(rsp['data'])>=1:
            for xxx in rsp['data']:
                try:
                    if 'http/ssl' == xxx['service']['name']:
                        count=count+1
                        print('https://'+xxx['service']['http']['host'] + ':' + str(xxx['port']), xxx['service']['http']['title'],'\t第：'+str(count))
                        open(nowtime, 'a', encoding='utf-8').write(str('https://'+xxx['service']['http']['host'])+':'+ str(xxx['port'])+'\t'+str(xxx['service']['http']['title'])+'\n')
                    elif 'http' == xxx['service']['name']:
                        count = count + 1
                        print('http://' + xxx['service']['http']['host'] + ':' + str(xxx['port']), xxx['service']['http']['title'],'\t第：'+str(count))
                        open(nowtime, 'a', encoding='utf-8').write(str('https://'+xxx['service']['http']['host'])+':'+ str(xxx['port'])+'\t'+str(xxx['service']['http']['title'])+'\n')
                    else:#非HTTP相关,协议数据
                        count = count + 1
                        print(str(xxx['service']['name']) + '\t' + str(xxx['ip'])+ '\t'+str(xxx['hostname'])+str(xxx['port']),'\t第：'+str(count))
                        open(nowtime, 'a', encoding='utf-8').write(str(xxx['service']['name']) + '\t' + str(xxx['ip'])+ '\t'+str(xxx['hostname'])+str(xxx['port'])+'\t'+'\n')
                except Exception as e:
                    #print(e)
                    pass
        else:
            if count !=0:
                print('本次检索到',count,'条数据，结果保存在'+nowtime)
                sys.exit()
            elif count ==0:
                print('本次检索到', count, '条数据')
                os.remove(nowtime)
                sys.exit()
        if count>=maxcount:
            print('本次检索到', count, '条数据，结果保存在' + nowtime)
            sys.exit()
    except Exception as e:
        try:
            if req.status_code==401:
                print('无效的key')
                os.remove(nowtime)
                sys.exit()
        except Exception as e2:
            pass
        os.remove(nowtime)
        print('出错啦',e)
        sys.exit()
