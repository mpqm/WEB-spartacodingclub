import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
#네이버 영화 순위 제목 평점 크롤링
# mongodb set
client = MongoClient('localhost', 27017)
db = client.dbsparta

# bs4 crawling
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#old_content > table > tbody > tr')
for tr in trs:
    a_tag = tr.select_one('td.title > div > a')
    if a_tag is not None:
        rank = tr.select_one('td:nth-child(1) > img ')['alt']
        title = a_tag.text
        point = tr.select_one('td.point').text
        doc = {
            'rank' : rank,
            'title' : title,
            'point' : point
        }
        db.movies.insert_one(doc)

# quiz 1
# user = db.movies.find_one({'title':'매트릭스'})
# target_star = user['point']
#
# target_movies = list(db.movies.find({'point':target_star},{'_id':False}))
#
# for m in target_movies:
#     print(m['title'])

db.movies.update_one({'title':'매트릭스'},{'$set':{'point':'0'}})
