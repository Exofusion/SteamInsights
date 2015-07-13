#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys
import CardUtil
import mysql.connector

def processItem(item, db):
  if ('Booster Pack' in item.game):
    cursor = db.cursor()
    cursor.execute("INSERT IGNORE INTO apps (id, name) VALUES (%s, %s)",
                   (item.id, item.name.replace(' Booster Pack','')))
    cursor.execute("INSERT INTO boosters (app_id, price, quantity, link, image, last_updated) VALUES (%s, %s, %s, %s, %s, NOW()) "+
                   "ON DUPLICATE KEY UPDATE price=%s, quantity=%s, last_updated=NOW()",
                   (item.id, item.price, item.quantity, item.link, item.image, item.price, item.quantity))
    cursor.close()
	
def zeroQuantities(db):
  cursor = db.cursor()
  cursor.execute("UPDATE boosters AS b,(SELECT scrape_start FROM scrape_info) AS s SET b.quantity = 0 WHERE b.last_updated < s.scrape_start")
  cursor.close()
  db.commit()

def main():
  db = mysql.connector.connect(user=DatabaseConfig.database_user,
                               password=DatabaseConfig.database_password,
                               host=DatabaseConfig.database_host,
                               database=DatabaseConfig.database_name)
  CardUtil.updateStart('boosters',db)
  CardUtil.scrapeMarket('booster+pack', db, processItem)
  CardUtil.updateEnd('boosters',db)
  zeroQuantities(db)
  db.close()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
