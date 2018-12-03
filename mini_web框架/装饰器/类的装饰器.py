import requests
from lxml import html
url='https://music.douban.com/' #需要爬的网址
page=requests.Session().get(url) 
tree=html.fromstring(page.text) 
result=tree.xpath('//tr//a/text()') #需要获取的数据
result1=tree.xpath('//tr//a/@href')
result2=tree.xpath('//tr[last()]//a/@href')
print(result)
print(result1)
print(result2)
