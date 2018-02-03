# coding:utf-8
import requests
from bs4 import BeautifulSoup
import urllib
import os
import threading

gLock = threading.Lock()  # 定义线程锁
url = "https://www.doutula.com/photo/list/?page="  # 将页面固定url地址盛放在变量里
pagelist = []  # 定义一个列表用来盛放获取的页面url
imgurllist = []  # 定义一个列表用来盛放获取的图片链接地址


def getMaxPage():  # 定义获取最大页面数的函数
    res = requests.get(url)  # 向网页提交get请求
    soup = BeautifulSoup(res.text, 'html.parser')  # 分析获取的网页数据
    ul = soup.select(".pagination")[0]
    aLabel = ul.select("a")[-2]  # 选择包含最大页面数的a标签
    # ul=soup.find_all("ul",attrs={"class":"pagination"})
    maxPage = int(aLabel.text)  # 获取最大页面数
    return maxPage


def getPage():  # 定义得到页面url地址的函数
    maxPage = getMaxPage()  # 调用函数获取最大页面数
    for i in range(1, maxPage + 1):  # 循环遍历页面数
        pagelist.append(url + str(i))  # 拼接获得所有页面url地址

# --------------------------------------------------------------------------------------------
def getImgUrl():  # 定义获得图片地址的函数
    for page in pagelist:  # 循环遍历页面地址
        res = requests.get(page)  # 请求
        soup = BeautifulSoup(res.text, 'html.parser')  # 解析
        imglist = soup.find_all(
            'img', attrs={"class": "img-responsive lazy image_dta"})  # 获取所有承载表情图片的img标签
        for img in imglist:  # 遍历循环所有img标签
            imgurl = img["data-backup"][:-4]  # 获取img标签中图片的地址
            if not imgurl.startswith("http:"):  # 判断地址是否完整，如果不完整在前面拼接http:
                imgurl = "http:" + imgurl

            downloadImg(imgurl)  # 调用下载函数进行图片下载

# 单线程下载函数
def downloadImg(imgurl):  # 定义图片下载函数
    filename = imgurl.split("/")[-1]  # 截取地址中图片名称用作本地图片名称
    filepath = os.path.join("images", filename)  # 拼接图片保存路径
    urllib.urlretrieve(imgurl, filename=filepath)  # 下载图片
# ------------------------------------------------------------------------------------------------

def th_getImgUrl():  # 定义使用多线程方式获取图片地址的函数
    while True:
        gLock.acquire()  # 开启线程锁
        if len(pagelist) == 0:  # 判断是否已经访问所有页面
            gLock.release()  # 释放线程锁
            break  # 如果已经访问所有页面，跳出循环
        pageurl = pagelist.pop()  # 取出列表中的页面地址
        gLock.release()  # 释放线程锁
        res = requests.get(pageurl)
        soup = BeautifulSoup(res.text, 'html.parser')
        imglist = soup.find_all(
            'img', attrs={"class": "img-responsive lazy image_dta"})
        for img in imglist:
            imgurl = img["data-backup"][:-4]
            if not imgurl.startswith("http:"):
                imgurl = "http:" + imgurl
            imgurllist.append(imgurl)


def th_downloadImg():  # 定义多线程方式下载图片的函数
    while True:
        gLock.acquire()
        if len(imgurllist) == 0:  # 判断图片地址列表是否有值
            gLock.release()
            continue  # 如果没有，结束本次循环，继续下次循环
        imgurl = imgurllist.pop()  # 取出图片地址
        gLock.release()
        filename = imgurl.split("/")[-1]
        filepath = os.path.join("images", filename)
        urllib.urlretrieve(imgurl, filename=filepath)
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        getPage()
        # getImgUrl()
        threadList1 = []
        threadList2 = []

        for i in range(3):  # 定义三个获取图片地址的线程
            th = threading.Thread(target=th_getImgUrl)
            threadList1.append(th)
        for th in threadList1:
            th.start()
        for th in threadList1:
            th.join()

        for i in range(5):  # 定义五个下载图片的线程
            th = threading.Thread(target=th_downloadImg)
            threadList2.append(th)
        for th in threadList2:
            th.start()
        for th in threadList2:
            th.join()

    except:
        print "请求错误。。。。。。"
    else:
        print "所有表情图片已全部下载完成，新一代的斗图帝就是你！！！"
