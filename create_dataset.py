from tkinter.tix import Tree
from bs4 import BeautifulSoup
from matplotlib.pyplot import cla
import requests, csv
import re
import time

# Files
sell_house = open("predaj_domy.csv", "w")
sell_apartmant = open("predaj_byty.csv", "w")
sell_together = open("predaj_spolu.csv", "w")

house_writer = csv.writer(sell_house)
apartmant_writer = csv.writer(sell_apartmant)
together_writer = csv.writer(sell_together)

header = [
  'price', # Cena
  'price_for_m2', # Cena za m2
  'locality', # Lokalita
  'street', # Ulica 
  'usable_area', # Úžitková plocha
  'floor', # Poschodie
  'elevator', # Výťah
  'state', # Stav
  'state_of_real_estate', # Stav nehnuteľnosti
  'real_estate_type', # Typ nehnuteľnosti
  'type_of_ownership', # Predaj / prenájom
  'balcony', # Balkón
  'basement', # Pivnica
  'material', # Materiál
  'land', # Pozemok
  'build_up_area' # Zastavaná plocha
] 

house_writer.writerow(header)
apartmant_writer.writerow(header)
together_writer.writerow(header)

###############################
# GET LINKS
###############################

webs_to_scrap = [
    "https://www.topreality.sk/vyhladavanie-nehnutelnosti.html?form=1&type%5B%5D=101&type%5B%5D=108&type%5B%5D=102&type%5B%5D=103&type%5B%5D=104&type%5B%5D=105&type%5B%5D=106&type%5B%5D=109&type%5B%5D=110&type%5B%5D=107&type%5B%5D=113&obec=&searchType=string&distance=&q=&cena_od=&cena_do=&vymera_od=0&vymera_do=0&n_search=search&page=estate&gpsPolygon=",
    "https://www.topreality.sk/vyhladavanie-nehnutelnosti.html?form=1&type%5B%5D=201&type%5B%5D=204&type%5B%5D=205&type%5B%5D=206&type%5B%5D=207&type%5B%5D=208&type%5B%5D=211&type%5B%5D=212&type%5B%5D=213&type%5B%5D=214&obec=&searchType=string&distance=&q=&cena_od=&cena_do=&vymera_od=0&vymera_do=0&n_search=search&page=estate&gpsPolygon=",
]

page = 0

def make_request(web): 
  print('scraping: {}'.format(web))
  
  try:
    req = requests.get(web).text 
  except:
    print('error at {}'.format(web))
    time.sleep(60)
    req = requests.get(web).text 
  return req

for index, web in enumerate(webs_to_scrap):
  html_text = make_request(web) 

  while True:
    print('{}page number: {}{}'.format('\033[95m', page + 1, '\x1b[0m'))
    page += 1
    pageSoup = BeautifulSoup(html_text, 'lxml')

    ###############################
    # Scrape Page
    ###############################
    
    for card_title in pageSoup.find_all('h2', class_='card-title'):
      for link in card_title.find_all('a', href=True):
        
        ###############################
        # Scrape the property insertion
        ###############################
        
        property = (
          make_request(link['href'])
        )
        
        soup = BeautifulSoup(property, 'lxml')
        table = soup.find('ul', class_='list-group-flush')

        prices = table.findAll('strong', class_='price')
        price = re.sub("[^0-9]", "", prices[0].text)
        price_for_m2 = re.sub("[^0-9]", "", prices[1].text) if len(prices) == 2 else None

        locality = table.find(
          "span", string="Lokalita"
        ).next_sibling.text.replace(",", "") if table.find("span", string="Lokalita") else None

        street = table.find(
          "span", string="Ulica"
        ).next_sibling.text if table.find("span", string="Ulica") else None

        usable_area = re.sub(
          "[^0-9]", "",
          table.find("span", string="Úžitková plocha").next_sibling.text
        )[0:-1] if table.find("span", string="Úžitková plocha") else None

        floor = table.find(
          "span", string="Poschodie"
        ).next_sibling.text.replace(" ", "") if table.find(
          "span", string="Poschodie"
        ) else None

        state = table.find(
          "span", string="Stav"
        ).next_sibling.text if table.find(
          "span", string="Stav"
        ) else None

        state_of_real_estate = table.find(
          "span", string="Stav nehnuteľnosti:"
        ).next_sibling.text if table.find(
          "span", string="Stav nehnuteľnosti:"
        ) else None

        elevator = table.find(
          "span", string="Výťah"
        ).next_sibling.text if table.find("span", string="Výťah") else None
        elevator = elevator == "Áno"

        balcony = table.find(
          "span", string="Balkón / loggia"
        ).next_sibling.text if table.find("span", string="Balkón / loggia") else None
        balcony = balcony == "Áno"

        basement = table.find(
          "span", string="Pivnica"
        ).next_sibling.text if table.find("span", string="Pivnica") else None
        basement = basement == "Áno"

        material = table.find(
          "span", string="Materiál"
        ).next_sibling.text if table.find(
          "span", string="Materiál"
        ) else None

        land = re.sub(
          "[^0-9]", "",
          table.find("span", string="pozemok").next_sibling.text
        )[0:-1] if table.find("span", string="pozemok") else None

        build_up_area = table.find(
          "span", string="Zastavaná plocha"
        ).next_sibling.text[:-len(' m2')] if table.find(
          "span", string="Zastavaná plocha"
        ) else None

        category =  " ".join(table.find(
          "span", string="Kategória"
        ).find_next_siblings(
          "strong")[0].text.split()
        ) if table.find("span", string="Kategória") else None

        real_estate_type = category.split('/')[0].strip()
        type_of_ownership = category.split('/')[1].strip()

        ###############################
        # Write to files
        ###############################

        data = [
          price,
          price_for_m2,
          locality,
          street,
          usable_area,
          floor,
          elevator,
          state,
          state_of_real_estate,
          real_estate_type,
          type_of_ownership,
          balcony,
          basement,
          material,
          land,
          build_up_area
        ]

        if index == 0: apartmant_writer.writerow(data)
        if index == 1: house_writer.writerow(data)
        together_writer.writerow(data)
      
      time.sleep(1)
    time.sleep(15)

    # if on the end of web, break loop
    if 'd-none' in (
      pageSoup
        .select('li.page-item.page-item-number.active')[0]
        .next_sibling['class']
    ): 
      break

    next_link = 'https://www.topreality.sk{}'.format(
      pageSoup
        .select('li.page-item.page-item-number.active')[0]
        .next_sibling
        .find("a")['href']
    )

    html_text = make_request(next_link) 