import csv
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import date
from datetime import timedelta
from datetime import datetime
import os.path

s = HTMLSession()
url = 'https://finviz.com/screener.ashx?v=111&f=geo_usa,sh_curvol_o200,sh_price_u15,sh_short_u25,ta_highlow52w_nh&ft=4'
response = s.get(url)
response.html.render()
soup = BeautifulSoup(response.content, 'lxml')
table = soup.find('table', attrs={'class': 'styled-table-new'})
allTr = table.findAll('tr', attrs={'valign': 'top'})
stocks = []
dt = datetime.now()
today = date.today()
yesterday = today - timedelta(days = 1)
yesterday = yesterday.strftime("%m/%d/%Y")
yesterday = str(yesterday)
begWeek = today - timedelta(days = 3)
begWeek = begWeek.strftime("%m/%d/%Y")
begWeek = str(begWeek)
today = today.strftime("%m/%d/%Y")
today = str(today)
dow = dt.weekday()
li1 = []
weekDay = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
if os.path.isfile('Pennystock.csv'):
    with open('Pennystock.csv') as file1:
        reader1 = csv.reader(file1)
        # sideA = random.choice(list(reader1))
        li1 = list(reader1)
    file1.close()
existingStock = []
if len(li1) > 1:
    for st in li1:
        if len(st) == 0:
            continue
        dt = datetime.strptime(st[5], "%m/%d/%Y")
        st[5] = dt.strftime("%m/%d/%Y")
        st[5] = str(st[5])
        if (st[5] == yesterday and dow != 0) or (st[5] == begWeek and dow == 0):
            existingStock.append(st[0])
    print(existingStock)
for i in range(len(allTr)):
    inARow = 'no'
    stockName = allTr[i].contents[3].findAll('a')[0].text
    category = allTr[i].contents[4].findAll('a')[0].text
    subcategory = allTr[i].contents[5].findAll('a')[0].text
    price = allTr[i].contents[9].findAll('a')[0].text
    growth = allTr[i].contents[10].findAll('a')[0].text
    if stockName in existingStock:
        inARow = 'yes'
    stocks.append([stockName, category, subcategory, price, growth, today, weekDay[dow], inARow])
with open('Pennystock.csv', 'a', newline= '') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(stocks)