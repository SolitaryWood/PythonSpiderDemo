# coding=utf-8
import requests
import re
import os


class GetMeizi_1(object):
	# 爬取路径：图集页 -》获取所有图集页地址 -》遍历图集页 -》获取图集地址 
	# 				-》遍历图集 -》获取图片地址 -》遍历下载图片
	# 数据解析：利用正则

	# 负责发送请求
	def Request_Url(self, url):
		headers = {
			'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
		}
		response = requests.get(url, headers=headers)
		html =  response.content
		return html

	# 获取所有图集页地址
	def Get_Pages(self,html):
		url = "http://www.meizitu.com/a/"
		# 匹配页面地址
		pattern = re.compile(r'<li><a href=\'more_(\d+).html\'>')
		page_num = int(pattern.findall(html)[-1])
		page_url_list = []
		for i in range(1,page_num + 1):
			page_url_list.append(url + 'more_' + str(i) + '.html')
		return page_url_list

	# 获取所有图集地址
	def Get_aLabel(self,url):
		html = self.Request_Url(url)
		# 匹配a标签
		pattern = re.compile(r'<a target=.*?href="(.*?)">.*?<b>(.*?)</b>')
		# 这里获取到的是以多个元组构成的列表，元组的第一个元素为图集地址，第二个元素为图集名
		alabel_list = pattern.findall(html)
		# print alabel_list
		return alabel_list

	def Get_Images(self, url):
		html = self.Request_Url(url)
		# 匹配图片地址
		pattern = re.compile(r'<img alt=.*?src="(.*?)".*?>')
		image_list = pattern.findall(html)
		# 移除最后一个，那是一张二维码。。。。
		image_list.pop()
		return image_list

	def Download_Image(self, filepath, image_list):
		s = os.mkdir('images/' + filepath)
		# print os.path.join('images',filepath)
		for image in image_list:
			filename = image[-18:].replace('/','')
			# print filename
			res = self.Request_Url(image)
			with open('images/' + filepath  + '/' + filename, 'wb') as f:
				f.write(res)

	def Start(self):
		URL = 'http://www.meizitu.com/a/more_1.html'
		html = self.Request_Url(URL)
		page_url_list = self.Get_Pages(html)
		for page_url in page_url_list:
			alabel_list = self.Get_aLabel(page_url)
			for alabel in alabel_list:
				image_list = self.Get_Images(alabel[0])
				self.Download_Image(alabel[1], image_list)

		print "Complete..."


def main():
	meizi_1 = GetMeizi_1()
	meizi_1.Start()

if __name__ == '__main__':
	main()