#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys
import CardUtil
import mysql.connector
import re

def main():
  db = mysql.connector.connect(user=DatabaseConfig.database_user,
                               password=DatabaseConfig.database_password,
                               host=DatabaseConfig.database_host,
                               database=DatabaseConfig.database_name)
  CardUtil.updateStart('cardvolume',db)
  cursor = db.cursor()
  cursor.execute("SELECT app_id, name, link FROM cards ORDER BY last_updated ASC")
  cardlist = cursor.fetchall()
  count = 0
  numrows = len(cardlist)
  for (app_id, name, link) in cardlist:
    try:
      cleanlink = re.search('\/753\/(.*)', link).group(1)
      volumeitem = CardUtil.getMarketVolume( cleanlink )
      if (not volumeitem.success):
        print(cleanlink)
      elif (volumeitem.lowest_price != 0):
        cursor.execute("UPDATE cards SET lowest_price = %s, volume = %s, median_price = %s, last_updated = NOW() WHERE app_id = %s AND name = %s",
                         (volumeitem.lowest_price, volumeitem.volume, volumeitem.median_price, app_id, name))
      else:
        cursor.execute("UPDATE cards SET quantity = 0, volume = %s, median_price = %s, last_updated = NOW() WHERE app_id = %s AND name = %s",
                         (0, 0, app_id, name))
    except KeyboardInterrupt:
      raise SystemExit
    except:
      print sys.exc_info()[0]
    if (count%100 == 0):
      db.commit()
      print (str(count)+" / "+str(numrows))
    count += 1

  cursor.close()
  db.commit()
  CardUtil.updateEnd('cardvolume',db)
  db.close()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
