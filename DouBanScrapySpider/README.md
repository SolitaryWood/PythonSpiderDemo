## 豆瓣电影爬虫scrapy版

爬取豆瓣电影top250，并将数据存储到本地数据库MongoDB

首先需要安装一下MongoDB数据库 `apt install mongodb`

启动MongoDB数据库

	service mongodb start

停止

	service mongodb stop

在终端输入`mongo`启动MongoDB客户端，MongoDB数据库默认端口为27017

常用命令：

	# 查看当前数据库名称
	db 

	# 查看所有数据库名称
	show dbs 

	# 切换数据库，默认连接test数据库
	use 数据库名 

	# 查看当前数据库信息
	db.stats() 

	# 删除数据库
	db.dropDatabase()

	# 查看当前数据库的集合/表
	show collections

	# 查看集合中的文档/行
	db.集合名.find()

	# 查看集合中文档的个数
	db.集合名.find().count()

	# 删除集合中所有文档
	db.集合名.drop()

在setting.py文件中数据库信息

	# 数据库地址
	MONGODB_HOST = '127.0.0.1'
	# 数据库端口
	MONGODB_PORT = 27017
	# 数据库名
	MONGODB_DBNAME = 'DoubanDB'
	# 数据库表/集合
	MONGODB_TABLE = 'DoubanMovie'

注：在setting文件中要配置user-agent头，有防爬机制

爬虫文件

	import re
	
	# 利用正则匹配出所有请求url
	# 需要注意的是，豆瓣这里有防爬机制，响应url会变为https://movie.douban.com/top250?0&filter=
	# 这里start=没有，但是还可以访问，不过是访问的是第一页
	# 所以这里需要自己重构请求url
	page = int(re.search(r'top250\?(\D*)(\d+)', response.url).group(2))
	s = re.search(r'top250\?(\D*)(\d+)', response.url).group(1)
	if s == '':
	    s = 'start='
	
	if page <= 225:
	    url = re.sub(r'top250\?(\D*)(\d+)', 'top250?' + s + str(page + 25), response.url)
	    yield scrapy.Request(url, callback=self.parse)

管道文件

	# 导入python操作MongoDB数据库的库
	import pymongo
	# 引入setting文件
	from scrapy.conf import settings
	
	class DoubanspiderPipeline(object):
	    def __init__(self):
	        # 获取setting文件中设置的数据配置信息
	        host = settings['MONGODB_HOST']
	        port = settings['MONGODB_PORT']
	        dbname = settings['MONGODB_DBNAME']
	        table = settings['MONGODB_TABLE']
	
	        # 连接数据库
	        client = pymongo.MongoClient(host=host, port=port)
	        # 指向指定的数据库
	        mdb = client[dbname]
	        # 指定集合
	        self.post = mdb[table]
	
	    def process_item(self, item, spider):
	        data = dict(item)
	        # 向表插入数据
	        self.post.insert(data)
	
	        return item

运行爬虫

	scrapy crawl DoubanMovieSpider


