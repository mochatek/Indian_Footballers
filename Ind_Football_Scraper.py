import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd

name_list=[]
pos_list=[]
age_list=[]
club_list=[]
value_list=[]

page_num=1

print("Scraping Started.")

while True:

	# Povide the URL here.
	url="https://www.transfermarkt.co.in/spieler-statistik/wertvollstespieler/marktwertetop/plus/ajax/yw1/ausrichtung/alle/spielerposition_id/alle/altersklasse/alle/jahrgang/0/land_id/67/yt0/Show/0//page/"+str(page_num)
	
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res=rq.get(url, headers=headers)

	soup=bs(res.content,'lxml')

	rows=soup.find('table',{'class':'items'}).findAll('tr',{'class':['odd','even']})

	for row in rows:
		name_pos=row.find('table',{'class':'inline-table'}).findAll('tr')
		age=row.findAll('td',{'class':'zentriert'})[1].text
		club=row.findAll('td',{'class':'zentriert'})[3].find('img')['alt']
		value=int(row.find('td',{'class':'rechts hauptlink'}).text.split()[0])

		name_list.append(name_pos[0].text)
		pos_list.append(name_pos[1].text)
		age_list.append(age)
		club_list.append(club)
		value_list.append(int(round(value*78409.46)))

	if not soup.find('li',{'title':'Go to next page'}):
		break
	else:
		page_num+=1

print("Scraping Completed.")

data=pd.DataFrame(zip(name_list,pos_list,age_list,club_list,value_list),
                  columns=['NAME','POSITION','AGE','CLUB','VALUE(Rs)'])
data.to_excel("Indian_Footballers.xlsx")

print("Data Exported Successfully.")
