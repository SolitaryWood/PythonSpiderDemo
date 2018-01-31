# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
import os

class GetMeizi_2(object):
	# 爬取路径：网站首页 -》获取所有美女分类标签地址 -》遍历标签地址页 -》获取图集地址 -》获取图片地址 -》下载
	# 数据解析：BeautifulSoup和正则

	# 负责发送请求
	def Request_Url(self, url):
		headers = {
			'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
		}
		response = requests.get(url, headers=headers)
		html =  response.content
		return html

	def Get_Images(self, url):
		html = self.Request_Url(url)
		# 匹配图片地址
		pattern = re.compile(r'<img alt=.*?src="(.*?)".*?>')
		image_list = pattern.findall(html)
		# 移除最后一个，那是一张二维码。。。。
		image_list.pop()
		return image_list

	def Download_Image(self, filepath, image_list):
		os.mkdir(os.path.join('images',filepath))
		# os.mkdir('images' + filepath)
		for image in image_list:
			filename = image[-18:].replace('/','')
			# print filename
			res = self.Request_Url(image)
			with open(os.path.join('images', filepath, filename), 'wb') as f:
			# with open('images/' + filepath  + '/' + filename, 'wb') as f:
				f.write(res)

	def Get_Tags(self,html):
		soup = bs(html,'lxml')
		tag_list = soup.select('span a')
		tag_url_list = []
		# print len(tag_list)
		# 获取所有妹子分类标签的地址
		for tag in tag_list:
			tag_url_list.append(tag.get('href'))
			# print type(tag.text)
			# print type(tag.string)
			# print type(tag.get_text())

		return tag_url_list

	def Get_aLabel(self,url):
		html = self.Request_Url(url)
		soup = bs(html,'lxml')
		# alabel_list = soup.select('div[class="pic"] a')
		alabel_list = soup.select('h3[class="tit"] a')
		# print len(alabel_list)
		alabel_url_list = []
		for alabel in alabel_list:
			# print alabel.contents[0].string
			alabel_tup = alabel.get('href'), alabel.contents[0].string
			alabel_url_list.append(alabel_tup)

		return alabel_url_list

	def Start(self):
		URL = 'http://www.meizitu.com/'
		html = self.Request_Url(URL)
		tag_url_list = self.Get_Tags(html)
		for tag_url in tag_url_list:
			alabel_url_list = self.Get_aLabel(tag_url)
			for alabel_tup in alabel_url_list:
				image_list = self.Get_Images(alabel_tup[0])
				self.Download_Image(alabel_tup[1], image_list)

		print "Complete..."


def main():

	meizi_2 = GetMeizi_2()
	meizi_2.Start()

if __name__ == '__main__':
	main()