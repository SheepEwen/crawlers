#Try to craw the information of shoes on Tmall
import requests
import re
from bs4 import BeautifulSoup
import traceback
import xlwt 

def getHTMLText(url):								#获取指定页面html文本
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print("wrong1")
		return ""

def parsePage(ilt, html):
	try:
		soup = BeautifulSoup(html, 'html.parser')
		glt = soup.find_all('div', attrs={'class':'product'})
		ult = soup.find('a', attrs={'class':'ui-page-next'})

		for goods in glt:						#提取每件商品的价格和名称
			try:
				pp = goods.find('p', attrs={'class':'productPrice'})
				em = pp.em
				price = em.attrs['title']
				tp = goods.find('p', attrs={'class':'productTitle'})
				a = tp.a
				title = a.text
				ilt.append([title, price])
			except:
				continue

		nurl = ult.attrs['href']					#返回下一页的url
		return nurl
	except:
		traceback.print_exc()						#校验错误信息
		print("wrong2")
		return ""
	
def saveGoodList(ilt, fpath):
	f = xlwt.Workbook()
	sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)			
										#写入表头
	sheet1.write(0,0,"序号")
	sheet1.write(0,1,"名称")
	sheet1.write(0,2,"价格")							

	count = 0
	for g in ilt:								#存入每件商品的信息
		count = count + 1						
		sheet1.write(count,0,count)
		sheet1.write(count,1,g[0])
		sheet1.write(count,2,float(g[1]))

	path = fpath + "Tmall.xls"
	f.save(path)								#保存文件至指定目录

def main():
	depth = 3 								#爬取的页面数目
	start_url = "https://list.tmall.com/search_product.htm"
	end_url = "?q=%E4%B9%A6%E5%8C%85"					#需查询的商品名称码
	fpath = "F://"								#文件存储的目录
	infoList = []
	for i in range(depth):
		try:
			url = start_url + end_url				#拼接新的页面url
			print(url)
			html = getHTMLText(url)
			end_url = parsePage(infoList, html)
			if end_url == "":					#所有页面爬取完成
				break
		except:
			continue						#若爬取出错，则继续爬取下一页面
	saveGoodList(infoList, fpath)

main()
