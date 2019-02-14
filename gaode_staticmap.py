import requests
import json
from bs4 import BeautifulSoup
import urllib.request
import xlrd
import xlwt

from urllib.parse import quote
import string

headers = {'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip,deflate,br',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Cache-Control': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64;rv:64.0)Gecko/20100101 Firefox/64.0'}


key = "2c35b4d07b6fba9f3dcbd6128fb0119b"
location = ""
zoom = "12"
size = "1024*1024"
scale = 2
markers = ""
labels = ""
paths = "10,0x0000FF,1,,:112,34;113,35"
traffic = 1

name = []
longitude = []
latitude = []

num_data = 0
data_list = []
longitude_ave = 0
latitude_ave = 0


"""
url = "https://restapi.amap.com/v3/staticmap?location={location}"\
    "&zoom={zoom}&size={size}&scale={scale}&markers={markers}&labels={labels}&paths={paths}&traffic={traffic}&key={key}"
"""

url = "https://restapi.amap.com/v3/staticmap?location={location}"\
    "&zoom={zoom}&size={size}&scale={scale}&labels={labels}&traffic={traffic}&key={key}"

def getexcel():
    workbook = xlrd.open_workbook(r'D:\python project\get_local\第二批 .xlsx')
    sheet = workbook.sheet_by_index(0)
    global name
    global longitude
    global latitude
    global labels
    global num_data
    global data_list
    global longitude_ave
    global latitude_ave
    global location
    name = sheet.col_values(0)
    longitude = sheet.col_values(1)
    latitude = sheet.col_values(2)
    del name[0]
    del longitude[0]
    del latitude[0]
    num_data =(len(name)//10) + 1
    for a in range(len(name)):
        longitude_ave += longitude[a]
        latitude_ave += latitude[a]
    longitude_ave = longitude_ave/len(name)
    latitude_ave = latitude_ave/len(name)
    location = "%f,%f"%(longitude_ave,latitude_ave)
    for k in range(num_data):
        labels = ""
        if k == num_data - 1:
            for i in range(10 * k,10 * k + (len(name)%10)):
                labels += "%s,2,0,16,,:%f,%f|"%(name[i],longitude[i],latitude[i])
        else:
            for i in range(10 * k,10 * (k + 1)):
                labels += "%s,2,0,16,,:%f,%f|"%(name[i],longitude[i],latitude[i])
        labels = labels.strip("|")
        print(labels)
        data_list.append(labels)

def gethtml(url,location,zoom,size,scale,temp,key,traffic,headers,num):
    url = url.format(location = location,zoom = zoom,size = size,scale = scale, \
                     labels = temp,traffic = traffic,key = key)
    url = quote(url, safe=string.printable)
    try:
        r = requests.get(url,headers = headers)
        r.raise_for_status()
        web = urllib.request.urlopen(url)
        data = web.read()
    except requests.RequestException as e:
        print(e)
    else:
        f = open('d:/python project/get_local/'+ str(num) +'.png', "wb")
        f.write(data)
        f.close()

getexcel()
for j in range(num_data):
    gethtml(url,location,zoom,size,scale,data_list[j],key,traffic,headers,j)