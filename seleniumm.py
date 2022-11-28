import requests
from lxml import etree
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
max_behot_time=0
video_list=[]
def get_json():
	global max_behot_time
	url='https://www.tiktok.com/@the.littlebeast/video/7148208852352240939?is_copy_url=1&is_from_webapp=v1&lang=zh-Hant&q=dumbell%20squat&t=1669661613757'+str(max_behot_time)
	r=requests.get(url,headers=headers)
	obj=json.loads(r.text)
	max_behot_time=obj['next']['max_behot_time']
	data=obj['data']
	for video_data in data:
		title=video_data['title']
		a_href='http://www.365yg.com'+video_data['source_url']
		down_video(title,a_href)

def down_video(title,href):
	#通过selenium来解析视频网址，
	path=r'E:\Student\python\day05\driver\chromedriver.exe'
	chrome_options=Options()
	chrome_options.add_argument('--Headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"')
	browser=webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
	browser.get(href)
	time.sleep(5)
	browser.save_screenshot(r'PjPhoto\baidu.png')
	#获取源码，生成对象，查找video 里面的src
	tree=etree.HTML(browser.page_source)
	video_url=tree.xpath('//video[@mediatype="video"]/@src')[0]
	video_url='http:'+video_url
	filepath='video/'+title+'.mp4'
	print('正在下载视频 %s'%title)
	r=requests.get(video_url)
	with open(filepath,'wb') as fp:
		fp.write(r.content)
	print('%s已下载'%title)
	browser.quit()

def main():
	# page=int(input('请输入你要下载的页数(每页7个):'))
	page=1
	for x in range(0,page):
		get_json()

if __name__ == '__main__':
	main()