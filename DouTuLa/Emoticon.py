# coding:utf-8
import requests
from bs4 import BeautifulSoup
import urllib
import os
import threading


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

# --------------------------------------------------------------------------------------------
# 单线程
def getImgUrl():  # 定义获得图片地址的函数
    # for page in page_list:  # 循环遍历页面地址
        response = requests.get(page)  # 请求
        soup = BeautifulSoup(response.text, 'html.parser')  # 解析
        imglist = soup.find_all(
            'img', attrs={"class": "img-responsive lazy image_dta"})  # 获取所有承载表情图片的img标签
        for img in imglist:  # 遍历循环所有img标签
            img_url = img["data-backup"][:-4]  # 获取img标签中图片的地址
            if not img_url.startswith("http:"):  # 判断地址是否完整，如果不完整在前面拼接http:
                img_url = "http:" + img_url

            downloadImg(img_url)  # 调用下载函数进行图片下载

def downloadImg(img_url):  # 定义图片下载函数
    filename = img_url.split("/")[-1]  # 截取地址中图片名称用作本地图片名称
    filepath = os.path.join("images", filename)  # 拼接图片保存路径
    urllib.urlretrieve(img_url, filename=filepath)  # 下载图片
# ------------------------------------------------------------------------------------------------
# 多线程

def Get_Img_Url():
    while True:
        # 一个线程开启线程锁，其他线程如果执行到这里，将处于阻塞状态
        gLock.acquire()
        # 如果列表中内容为空，代表已访问完所有页面
        if len(page_list) == 0:
            # 释放线程锁
            gLock.release()
            break
        # 取出列表中的页面地址
        page_url = page_list.pop()
        gLock.release()
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 通过分析页面发现所有表情包都盛放在class属性为img-responsive lazy image_dta的img标签
        imgLabel_list = soup.find_all(
            'img', attrs={"class": "img-responsive lazy image_dta"})
        for img in imgLabel_list:
            # 从img标签中取出图片地址，去掉图片地址后面四个干扰字符
            img_url = img.get("data-backup")[:-4]
            # 使用startswich函数检查url地址是否是以http:开头
            if not img_url.startswith("http:"):
                # 如果不是拼接图片地址
                img_url = "http:" + img_url
            img_url_list.append(img_url)


# 图片下载函数
def Img_Download():
    while True:
        gLock.acquire()
        # 判断是否下载完
        if len(img_url_list) == 0:
            gLock.release()
            break
        img_url = img_url_list.pop()
        gLock.release()
        # 将图片地址中图片名作为本地图片名
        filename = imgurl.split("/")[-1]
        filepath = os.path.join("images", filename)
        urllib.urlretrieve(img_url, filename=filepath)
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        # 定义一个全局的线程锁
        gLock = threading.Lock()
        url = "https://www.doutula.com/photo/list/?page="
        # 定义一个列表用来盛放所有的页面url地址
        page_list = [] 
        # 定义一个列表用来盛放获取的图片链接地址
        img_url_list = []

        Get_Pages()
        print "Get Pages Completed..."

        threadList1 = []
        threadList2 = []

        # 定义三个获取图片地址的线程
        for i in range(5):
            th = threading.Thread(target=Get_Img_Url)
            threadList1.append(th)
        for th in threadList1:
            # 开启线程
            th.start()

        # 主线程阻塞，等待所有获取图片地址的线程完成，才继续向下执行
        # 这里会先获取完所有图片地址，然后才开始下载图片
        for th in threadList1:
            th.join()

        print "Starting Download Images..."
        # 定义五个下载图片的线程
        for i in range(5):
            th = threading.Thread(target=Img_Download)
            threadList2.append(th)
        for th in threadList2:
            th.start()

        for th in threadList2:
            th.join()

    except:
        print("Error...")
    else:
        print("Download Completed...")
