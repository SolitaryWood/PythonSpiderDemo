# coding:utf-8
import requests
from bs4 import BeautifulSoup
import urllib
import os
import threading
from Queue import Queue


# 函数用于获取所有页面
def Get_Pages():
    response = requests.get(url)
    # 解析网页数据
    soup = BeautifulSoup(response.text, 'html.parser')
    # 页面链接标签在ul标签中，我这里先获取ul标签
    ul_label = soup.select(".pagination")[0]
    # ul_label=soup.find_all("ul",attrs={"class":"pagination"})
    # 然后获取包含最大页面数的a标签，并从中取出页面数
    maxPage = int(ul_label.select("a")[-2].text)
    # 循环遍历获取所有页面
    for i in range(1, maxPage + 1):
        # 拼接页面url地址
        page_list.append(url + str(i))


def Get_Img_Url():
	# 声明queue为全局变量
	global queue
	while page_list:
		# 从队列中取出的页面地址
		page_url = page_list.pop() 
		response = requests.get(page_url)
		soup = BeautifulSoup(response.text, 'html.parser')
		# 通过分析页面发现所有表情包都盛放在class属性为img-responsive lazy image_dta的img标签
		imgLabel_list = soup.find_all(
		    'img', attrs={"class": "img-responsive lazy image_dta"})
		for img in imgLabel_list:
		    # 从img标签中取出图片地址，去掉图片地址后面四个干扰字符
		    img_url = img.get("data-backup")[:-4]
		    # 获取图片的描述信息作为图片文件名
		    img_name = img.get("alt")
		    # 使用startswich函数检查url地址是否是以http:开头
		    if not img_url.startswith("http:"):
		        # 如果不是拼接图片地址
		        img_url = "http:" + img_url
		    # 定义一个元组，盛放图片名和图片地址
		    img_tuple = (img_name, img_url)
		    # 放入数据进队列
		    queue.put(img_tuple)


# 图片下载函数
def Img_Download():
	global queue
	while True:
		# 如果队列为空，并且页面列表也为空，代表下载完成
		if queue.empty() and not page_list:
			break
		img_tuple = queue.get()
		filename = img_tuple[0] + '.jpg'
		img_url = img_tuple[1]
		filepath = os.path.join("images", filename)
		try:
			urllib.urlretrieve(img_url, filename=filepath)
		except Exception:
			# 如果报错，更改一下图片名
			img_name = img_url.split("/")[-1] 
			# 重新放入队列
			queue.put((img_name, img_url))
		finally:
			# 重开线程
			threading.Thread(target=Img_Download).start()

if __name__ == "__main__":
	try:
		url = "https://www.doutula.com/photo/list/?page="
		page_list = []
		# 定义一个全局队列
		queue = Queue()

		Get_Pages()

		print "Get Pages Completed..."
		threadList1 = []
		threadList2 = []

		# 定义三个获取图片地址的线程
		for i in range(3):
			th = threading.Thread(target=Get_Img_Url)
			threadList1.append(th)
		for th in threadList1:
			# 开启线程
			th.start()
		print "Starting Download Images..."
		# 定义五个下载图片的线程
		for i in range(5):
			th = threading.Thread(target=Img_Download)
			threadList2.append(th)
		for th in threadList2:
		    th.start()

		# 主线程等待所有线程执行完毕，获取图片线程与下载图片进程同时执行
		for th in threadList1:
			th.join()
		for th in threadList2:
			th.join()

	except:
		print("Error...")
	else:
		print("Download Completed...")
