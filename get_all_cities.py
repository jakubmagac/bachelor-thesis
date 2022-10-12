from tkinter.tix import Tree
from bs4 import BeautifulSoup
from matplotlib.pyplot import cla
import requests

village = 'http://www.sodbtn.sk/obce/abeceda.php'
city = 'https://sk.wikipedia.org/wiki/Zoznam_miest_na_Slovensku'

req_v = requests.get(village)
html_text_v = req_v.content

req_c = requests.get(city)
html_text_c = req_c.content

soup_v = BeautifulSoup(html_text_v.decode('utf-8','ignore'), features="lxml", from_encoding="utf-8")
tables_v = soup_v.findAll('td', class_='stlpec')

soup_c = BeautifulSoup(html_text_c.decode('utf-8','ignore'), features="lxml", from_encoding="utf-8")
tables_c = soup_c.find('table').find_all('b')

with open('city.txt', 'w') as f:
  for t in tables_v:
    f.write(t.find('b').text)
    f.write('\n')

  # remove city
  for tab in tables_c:
    f.write(tab.text)
    f.write('\n')

