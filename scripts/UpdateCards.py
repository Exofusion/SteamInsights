#!/usr/bin/python

import sys
import mysql.connector

import DatabaseConfig
import CardUtil

def processItem(item, db):
  if ('Trading Card' in item.game):
    foil = 1 if 'Foil' in item.game else 0
    cursor = db.cursor()
    cursor.execute("INSERT IGNORE INTO apps (id, name) VALUES (%s, %s)",
                   (item.id, item.game.replace(' Foil Trading Card','').replace(' Trading Card','')))
    cursor.execute("INSERT INTO cards (app_id, name, lowest_price, quantity, foil, link, image, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW()) "+
                   "ON DUPLICATE KEY UPDATE lowest_price=%s, quantity=%s, last_updated=NOW()",
                   (item.id, item.name, item.price, item.quantity, foil, item.link, item.image, item.price, item.quantity))
    cursor.close()

def main():
  db = mysql.connector.connect(user=DatabaseConfig.database_user,
                               password=DatabaseConfig.database_password,
                               host=DatabaseConfig.database_host,
                               database=DatabaseConfig.database_name)
  CardUtil.updateStart('cards',db)
  CardUtil.scrapeMarket('trading+card', db, processItem)
  CardUtil.updateEnd('cards',db)
  db.close()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
