import os
from selenium import webdriver
from time import sleep
import pandas as pd


def checkEmpty(lagerID, lagerPLZ):
    
  path = "Leere_Suchen"
  try:
    os.mkdir(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
  else:
    print ("Successfully created the directory %s " % path)

  # Subordner pro PLZ erstellen, falls der noch nicht existiert
  try:
    os.mkdir(path + "/" + lagerID + '_' + lagerPLZ)
  except OSError:
    print ("Creation of the directory %s failed" % (path + "/" + lagerPLZ))
  else:
    print ("Successfully created the directory %s " % (path + "/" + lagerID + "_" + lagerPLZ))
  
  # Starten und HTLP übergehen
  driver = webdriver.Firefox()
  driver.get('https://www.flaschenpost.de')

  zipcodeInput = driver.find_element_by_xpath('//*[@id="validZipcode"]')
  zipcodeInput.send_keys(lagerPLZ)

  zipcodeInputEnter = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/button')
  zipcodeInputEnter.click()
  sleep(3)

  # csv einlesen (Suchbegriffe)
  top = pd.read_csv("analytics.csv", header=0, usecols=['Suchbegriff', 'WarehouseId'], sep=';')
  filter = top['WarehouseId'] == float(lagerID)
  top = top[filter]
  print(top)

  # Suchen und Screenshots erstellen
  x = 1

  for i in top['Suchbegriff']:
    print(lagerID + "_" + str(x) + i + '.png')
    searchIcon = driver.find_element_by_xpath('/html/body/div[1]/header/div[3]/div/div[2]/div[1]/div/div')
    searchTerm = driver.find_element_by_xpath('//*[@id="searchTerm"]')
    searchTermSubmit = driver.find_element_by_xpath('//*[@id="search-form-header"]/div[1]/button')
    sleep(2)
    searchIcon.click()
    sleep(2)
    searchTerm.send_keys(i)
    sleep(2)
    searchTermSubmit.click()
    sleep(3)
    body = driver.find_element_by_xpath('/html/body')
    sleep(2)
    checked = driver.find_element_by_xpath('//*[@id="fp-articleList-container"]/div[1]')
    if checked.text == "Deine Suche nach " + i + " ergab leider keine Treffer!":
      element_png = body.screenshot_as_png
      sleep(2)
      with open(path + "/" + lagerID + '_' + lagerPLZ + "/" +lagerID + "_" + str(x) + '_' + i + ".png", "wb") as file:
        file.write(element_png)
      sleep(2)  # body.screenshot(i + '.png')
    x += 1

warehouse = pd.read_csv('warehouse.csv', header=0, usecols=['LagerId', 'LagerPLZ'], sep=',')


for i in warehouse['LagerId']:
  mask = warehouse['LagerId'] == i
  lagerplz = int(warehouse.loc[mask, 'LagerPLZ'])
  print (lagerplz)
  checkEmpty(str(i), str(lagerplz))