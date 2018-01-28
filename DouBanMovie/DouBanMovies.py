# coding=utf-8
import requests
import json

API_URL_1 = 'https://api.douban.com/v2/movie/top250'
API_URL_2 = 'https://api.douban.com/v2/movie/subject/'
API_URL_3 = 'https://api.douban.com/v2/movie/search?q='


def Data_Extract(res):
	movie_list = []
	data =  json.loads(res.content)
	for movie in data['subjects']:
		movie_dict = {}
		movie_dict['movie_name'] = movie['title'].encode('utf-8')
		movie_dict['movie_year'] = movie['year'].encode('utf-8')
		movie_dict['movie_id'] = movie['id'].encode('utf-8')
		movie_directors = movie['directors']
		movie_directors_name = ''
		for director in movie_directors:
			movie_directors_name += director['name'].encode('utf-8') + " "
		movie_dict['movie_directors_name'] = movie_directors_name
		movie_dict['movie_rating'] = movie['rating']['average']

		movie_list.append(movie_dict)
	return movie_list


def Movie_Top():
	response = requests.get(API_URL_1)
	return Data_Extract(response)


def Movie_Details(movie_id):
	movie_url = API_URL_2 + movie_id
	# print movie_url
	response = requests.get(movie_url)
	data = json.loads(response.content)

	print '\n电影详情\n' + '*'*50
	print '电影名：' + str(data['title'].encode('utf-8'))
	print '上映时间：' + str(data['year'])
	directors = ''
	for director in data['directors']:
		directors += director['name'].encode('utf-8') + ' '
	print '导演：' + str(directors)
	casts = ''
	for cast in data['casts']:
		casts += cast['name'].encode('utf-8') + ' '
	print '主演：' + str(casts)
	countries = ''
	for country in data['countries']:
		countries += country.encode('utf-8') + ' '
	print '国家：' + str(countries)
	genres = ''
	for genre in data['genres']:
		genres += genre.encode('utf-8') + ' '
	print '种类：' + str(genres)
	print '摘要：' + str(data['summary'].encode('utf-8'))
	print '评分：' + str(data['rating']['average'])


def Movie_Search(keyword):
	search_url = API_URL_3 + keyword
	response = requests.get(search_url)
	return Data_Extract(response)


def Movie_Print(movie_list):
	print '\n电影列表\n' + '-' * 50
	for movie in movie_list:
		# print movie
		print "电影ID：" + movie['movie_id']
		print "电影名：" + movie['movie_name']
		print "电影上映时间：" + movie['movie_year']
		print "电影导演：" + movie['movie_directors_name']
		print "电影评分：" + str(movie['movie_rating'])
		print '-'*50


def Look_Details():
	movie_id = raw_input('请输入要查看电影详情的电影ID：')
	# movie_id = '1300267'
	Movie_Details(movie_id)


def Logo_Title(title):
	length = len(title) / 3
	num = 50 / 2 - length - 1
	# print length
	print '=' * 50
	print '|' + ' ' * 48 + '|'
	print '|' + ' ' * num + title + ' ' * num + '|'
	print '|' + ' ' * 48 + '|'
	print '=' * 50


def main():
	Logo_Title('豆瓣电影')
	print '1.查看电影排行'
	print '2.搜索电影'
	code = raw_input('请输入操作码：')
	# code = '1'
	if code == '1':
		movie_list = Movie_Top()
		Movie_Print(movie_list)
		Look_Details()
	elif code == '2':
		keyword = raw_input('请输入搜索关键词：')
		movie_list = Movie_Search(keyword)
		Movie_Print(movie_list)
		Look_Details()
	else:
		print '错误的操作码！'

if __name__ == '__main__':
	main()
