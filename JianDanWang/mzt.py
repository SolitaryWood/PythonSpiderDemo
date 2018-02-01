# coding=utf-8
import requests
from selenium import webdriver
from lxml import etree
import os


headers = {
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
err_url_list = []

# 使用phantomjs浏览器创建浏览器对象
# 在环境变量中需要设置Phantomjs浏览器地址
driver = webdriver.PhantomJS()
# driver = webdriver.PhantomJS(executable_path='./phantomjs')


def Parse_Image_Url(data):
	# 将字符串解析为HTML文档
	html = etree.HTML(data)
	image_url_list = html.xpath('//p/img/@src')
	return image_url_list

def Get_Page_list(data):
	url = 'http://jandan.net/ooxx/page-'
	html = etree.HTML(data)
	result = html.xpath('//div[@class="cp-pagenavi"]/a')
	# 获取a标签的内容
	pages = result[0].text
	page_url_list = []
	for page in range(1,int(pages) + 1):
		page_url = url + str(page)
		page_url_list.append(page_url)

	return page_url_list

def Request_Page(url):
	# 加载网页
	driver.get(url)
	# 获取网页渲染后的源代码
	data = driver.page_source.encode('utf-8')
	return data

def Download_Image(filedir, image_url_list):
	for image_url in image_url_list:
		response = requests.get(image_url, headers=headers)
		# print response.status_code
		if response.status_code == 200:
			filename = image_url[image_url.rfind('/')+1:]
			filepath = os.path.join(filedir, filename)
			with open(filepath, 'wb') as f:
				f.write(response.content)
		else:
			err_url_list.append(image_url)

def main():
	print "Starting..."
	# 爬取首页
	url = 'http://jandan.net/ooxx/'
	data = Request_Page(url)
	page_url_list = Get_Page_list(data)
	image_url_list = Parse_Image_Url(data)
	Download_Image('images', image_url_list)
	# 遍历其他页面
	for page_url in page_url_list:
		data = Request_Page(page_url)
		image_url_list = Parse_Image_Url(data)
		Download_Image('images', image_url_list)

	# 重新处理出错的url，请求三次
	for i in range(3):
		Download_Image(err_url_list)

	if err_url_list:
		print "下载失败的url列表："
		print err_url_list

	driver.quit()

	print "Ending..."

if __name__ == '__main__':
	main()
