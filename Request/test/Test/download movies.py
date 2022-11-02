# -*- codeing =utf-8 -*-
# author:XC
# @Time :2022/5/4 15:08
# @File :download movies.py
# @Software: PyCharm




'''尝试爬取电影'''
import time
from tqdm import tqdm
from fake_useragent import UserAgent
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from ffmpy3 import FFmpeg
import json
from lxml import etree
import concurrent.futures

#目标地址和伪装浏览器
baseurl = 'http://www.6uzy.cc/detail/80175.html'
headers={'user-agent':UserAgent().random}

#获取资源url保存为json格式文件
class Selenium():
    # 初始化并用无头浏览器selenium模拟网页行为
    def __init__(self):
        global driver
        self.options=Options()
        self.options.add_argument('--headless')
        driver=webdriver.Chrome(chrome_options=self.options)
        driver.implicitly_wait(10)

    #获取第一页文件解析出每一个播放视频地址
    def get_playHref(self):
        response=requests.get(url=baseurl,headers=headers).text
        BaseHtml=etree.HTML(response)
        playHrefs=BaseHtml.xpath(r'//div[@id="tab1"]/a/@href')
        return playHrefs

    #通过selenium模拟请求嵌套获取每一个url下的m3u8视频地址片段，并拼接成完整地址
    def get_m3u8Href(self):
        Firsturl='http://www.6uzy.cc'
        playHrefs=self.get_playHref()
        needurls={}
        flag=0
        for href in tqdm(playHrefs):
            flag=flag+1
            url=Firsturl+href
            #用selenium无头浏览器自动化获取所需元素
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver=webdriver.Chrome(chrome_options=chrome_options)
            driver.implicitly_wait(10)
            driver.maximize_window()
            driver.get(url=url)
            #获取#document下的数据多重iframe嵌套
            iframe = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,'//iframe[2]')))
            driver.switch_to.frame(iframe)
            iframe1=driver.find_element(By.XPATH,r'//iframe[@id="lineFrame"]')
            driver.switch_to.frame(iframe1)
            iframe2=driver.find_element(By.ID,"zzapi")
            driver.switch_to.frame(iframe2)
            page_soure=driver.page_source
            pattern=r'var videoUrl = "(.*)";'
            needurl=re.findall(pattern=pattern,string=page_soure)
            driver.quit()
            time.sleep(5)
            #保存为字典集
            name="{0}{1}".format("浮生印第"+str(flag),"集")
            needurls[name]=needurl
        return needurls

    #返回一个json格式的文件
    def store_url(self):
        urls=self.get_m3u8Href()
        jsonurls=json.dumps(urls)
        name='浮生印.json'
        with open(name,'w') as fp:
            fp.write(jsonurls)


#通过多线程池和已经获取的json文件，用FFmpeg获得目标地址的m3u8视频流文件
mydict=json.loads('{"\u6d6e\u751f\u5370\u7b2c1\u96c6": ["https://v.kdianbo.com/20220901/fFg1mcJK/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c2\u96c6": ["https://v.kdianbo.com/20220901/wHq80GTy/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c3\u96c6": ["https://v.kdianbo.com/20220901/mZwPi708/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c4\u96c6": ["https://v.kdianbo.com/20220901/W9ihtQwJ/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c5\u96c6": ["https://v.kdianbo.com/20220901/EI4Afavc/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c6\u96c6": ["https://v.kdianbo.com/20220901/bRmh1R03/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c7\u96c6": ["https://v.kdianbo.com/20220901/ToDtJzj9/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c8\u96c6": ["https://v.kdianbo.com/20220901/XulfMufG/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c9\u96c6": ["https://v.kdianbo.com/20220902/wEpkVafp/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c10\u96c6": ["https://v.kdianbo.com/20220902/vxrATSs9/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c11\u96c6": ["https://v.kdianbo.com/20220903/P22LFPEh/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c12\u96c6": ["https://v.kdianbo.com/20220903/NXFsexGb/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c13\u96c6": ["https://v.kdianbo.com/20220908/AcEaUJgB/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c14\u96c6": ["https://v.kdianbo.com/20220908/SbuYlugS/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c15\u96c6": ["https://v.kdianbo.com/20220909/ByWcZrUl/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c16\u96c6": ["https://v.kdianbo.com/20220909/gMrcrVOP/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c17\u96c6": ["https://v.kdianbo.com/20220910/v6YOYB0e/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c18\u96c6": ["https://v.kdianbo.com/20220910/JqY4wnMg/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c19\u96c6": ["https://v.kdianbo.com/20220915/O79HqYdu/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c20\u96c6": ["https://v.kdianbo.com/20220915/RWdI9Vz5/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c21\u96c6": ["https://v.kdianbo.com/20220916/EWijnemk/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c22\u96c6": ["https://v.kdianbo.com/20220916/Epnx7PFT/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c23\u96c6": ["https://v.kdianbo.com/20220917/Q8kOCXSi/index.m3u8"], "\u6d6e\u751f\u5370\u7b2c24\u96c6": ["https://v.kdianbo.com/20220917/wfAp6gzK/index.m3u8"]}')
Baseurl='/2000kb/hls/index.m3u8'
Truedict={}
for key in mydict:
    url=mydict[key][0].split('/index.m3u8')[0]+Baseurl
    Truedict[url]=key

def download_video(url):
    name='{0}.mp4'.format(Truedict[url])
    FFmpeg(inputs={url:None},outputs={name:None},executable=r'D:\website\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe').run()

with concurrent.futures.ThreadPoolExecutor() as pool:
    pool.map(download_video,Truedict.keys())






