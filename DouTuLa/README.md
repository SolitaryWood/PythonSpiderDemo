## 多线程爬取斗图表情包

爬取 [斗图啦](https://www.doutula.com/photo/list/) 斗图表情图，做一名优雅的斗图帝！！！

使用python2编写，用到requests库发送请求，BeautifulSoup进行数据提取，`urllib.urlretrieve()`下载表情包。

使用多线程threading模块，并且根据python线程同步的两种不同机制，互斥锁和队列，编写了两个版本的代码。

最后来一张效果图：

![](1.png)

emm 几分钟爬了一万多张，大小有五百多M，多线程还是挺快的。。。