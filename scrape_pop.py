import requests, re
from bs4 import BeautifulSoup
from datetime import datetime
from string import ascii_lowercase

url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"

r = requests.get(url)
print(r.status_code)
	
if r.status_code != 200:
	print(r.status_code)
	sys.exit(1)

fout = open("populations.csv","w")
fout.write("city, pop_2015, pop_2010, lat, lon\n")

alpha_reg = re.compile('[^a-zA-Z \'\.]')
latlon_reg = re.compile('[^0-9 \-\.]')

soup = BeautifulSoup(r.text, "html.parser")
table = soup.find("table",{"class":"wikitable sortable"})
for tr in table.find_all("tr")[2:]:
	tds = tr.find_all("td")
	city = alpha_reg.sub('',tds[1].text)
	pop_2015 = tds[3].text
	pop_2010 = tds[4].text
	location = tds[8].text.split("/")[-1]
	location = latlon_reg.sub('',location)
	lat = location.split()[0]
	lon = location.split()[1]
	fout.write("{},{},{},{},{}\n".format(city,pop_2015,pop_2010,lat,lon))

fout.close()
