import concurrent.futures
from fake_useragent import UserAgent
import requests
import re
import pprint
import json
import subprocess

baseurl="https://www.bilibili.com/video/BV1PP4y1U7qA/?spm_id_from=333.1007.top_right_bar_window_history.content.click"
headers={'user-agent':UserAgent(use_cache_server=False).random,'referer':'https://search.bilibili.com/all?keyword=%E7%88%AC%E5%8F%96b%E7%AB%99&from_source=webtop_search&spm_id_from=333.1007&search_source=5'}

response=requests.get(url=baseurl,headers=headers).text
pattern=r'<script>window.__playinfo__=(.*?)</script>'
string=re.findall(pattern,response)[0]
pattern1=r'<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>'
title='原神纳西妲'

Json=json.loads(string)
audio=Json['data']['dash']['audio'][0]['baseUrl']
video=Json['data']['dash']['video'][0]['baseUrl']
mydic={'video':video,'audio':audio}

audioC=requests.get(url=audio,headers=headers).content
videoC=requests.get(url=video,headers=headers).content
audioC_name='./'+title+'.mp3'
videoC_name='./'+title+'.mp4'
with open(audioC_name,'wb') as fp:
    fp.write(audioC)
    print('audio爬取成功！')

with open(videoC_name,'wb') as fp:
    fp.write(videoC)
    print('video爬取成功!')

CMD=f'ffmpeg -i {videoC_name} -i {audioC_name} -c:v copy -c:a copy -bsf:a aac_adtstoasc R{title}.mp4'
subprocess.run(CMD,shell=True)
