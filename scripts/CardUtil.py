#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import mysql.connector
import time
import json
import urllib

class MarketItem:
  def __init__(self, id, price, name, link,  image, quantity, game):
    self.id = id
    self.price = price
    self.name = name
    self.link = link
    self.image = image
    self.quantity = quantity
    self.game = game

class VolumeItem:
  def __init__(self, success, lowest_price, volume, median_price):
    self.success = success
    self.lowest_price = lowest_price
    self.volume = volume
    self.median_price = median_price

def cleanString(data):
  data = data.replace('\\"', '"').replace('\\/', '/')
  return data

def convertUnicode(data):
  while ('\\u' in data):
    location = data.find('\\u')
    unicodestring = data[location:location+6]
    data = data.replace(unicodestring, unicode(int(unicodestring[2:6],16)))
  return data
  
def scrapeMarket(search, db, callback):
  TIMEOUT = 3
  count = 100
  start = 0
  end_of_page = False
  while (not end_of_page):
    url = 'http://steamcommunity.com/market/search/render/?query='+search+'&start='+str(start)+'&count='+str(count)+'&search_descriptions=0&appid=753&sort_column=name&sort_dir=asc'
    r = requests.get(url)
    data = r.text
    
    if (r.status_code != requests.codes.ok):
      print('Error: Unexpected status code')
      time.sleep(TIMEOUT)
    elif ('There was an error' in data):
      print('Error: Error performing search')
      time.sleep(TIMEOUT)
    elif ('There were no items matching your search' in data):
      end_of_page = True
    else:
      data = cleanString(data)
      data = convertUnicode(data)
      soup = BeautifulSoup(data)
      total_count = re.search('"total_count":([0-9]*)', data).group(1)
      print("Item "+str(start)+"/"+str(total_count))

      for element in soup.find_all('a', class_='market_listing_row_link'):
        price = float(element.find('span', class_='market_table_value').span.string.replace('$',''))
        link = re.sub('\?filter=.*','',element.get('href'))
        id = int(re.search('753/(.*?)\-', link).group(1))
        image = element.find('img').get('src')
        quantity = int(element.find('span', class_='market_listing_num_listings_qty').string.replace(',',''))
        name = element.find('span', class_='market_listing_item_name').get_text()
        game = element.find('span', class_='market_listing_game_name').get_text()
        
        item = MarketItem(id, price, name, link, image, quantity, game)
        callback(item, db)
      start += count
      db.commit()
	  
def getMarketVolume(namehash):
  url = 'http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=753&market_hash_name='+namehash
  r = requests.get(url)
  if (r.status_code != requests.codes.ok):
    print('Error: Unexpected status code')
    return VolumeItem(False, 0, 0, 0)
  jsonobj = r.json()
  success = jsonobj["success"] if ("success" in jsonobj) else False
  lowest_price = jsonobj["lowest_price"].replace('&#36;','') if ("lowest_price" in jsonobj) else 0
  volume = jsonobj["volume"] if ("volume" in jsonobj) else 0
  median_price = jsonobj["median_price"].replace('&#36;','') if ("median_price" in jsonobj) else 0
  return VolumeItem(True, lowest_price, volume, median_price)

def updateStart(type, db):
  cursor = db.cursor()
  cursor.execute("INSERT INTO scrape_info (type, scrape_start) VALUES (%s, NOW()) ON DUPLICATE KEY UPDATE scrape_start=NOW();",
                (type,))
  db.commit()

def updateEnd(type, db):
  cursor = db.cursor()
  cursor.execute("UPDATE scrape_info SET scrape_end=NOW() WHERE type = %s;",
                (type,))
  db.commit()