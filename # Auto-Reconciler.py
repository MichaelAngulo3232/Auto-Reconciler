# Auto-Reconciler

from pickle import APPEND
import selenium
import time
import creds
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import glob
import os
import csv
import pandas

#launch webpage

driver = webdriver.Chrome(executable_path='/Users/michaelangulo/Documents/Python Programs/chromedriver')
driver.get("https://sweetgreen-em.net-chef.com/standalone/modern.ct#Login")


# username and password sign in to EM then Net Chef

location = "walnut"

time.sleep(1)
driver.find_element(By.ID, "ext-element-22").send_keys(creds.EMusername)
driver.find_element(By.ID, "ext-element-36").send_keys(creds.EMpassword)
time.sleep(1)
driver.find_element(By.ID, "ext-element-65").click()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "#ext-element-102").click()
time.sleep(3)
driver.find_element(By.ID, "tool-1028-toolEl").click()
time.sleep(4)
driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div[2]/a/span").click()
time.sleep(3)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)
element =  driver.find_element(By.CSS_SELECTOR, "#ext-element-22")
element.send_keys(location)
time.sleep(1)
element.send_keys(Keys.RETURN)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#ext-element-51").click()

# display page of stores to be reconciled

time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#button-1191-btnInnerEl").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#menuitem-1194-textEl").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#menuitem-1201-textEl").click()
time.sleep(2)
driver.find_element(By.ID, "cescombogridpicker-1277-inputEl").click()
time.sleep(1)
driver.find_element(By.ID, "cescombogridpicker-1277-inputEl").send_keys(Keys.BACKSPACE)
time.sleep(1)
driver.find_element(By.ID, "cescombogridpicker-1277-inputEl").send_keys("fleet")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#gridfilters-1302-toolEl").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#listfiltercombobox-1392-trigger-picker").click()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div[8]/div[1]/ul/li[7]").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#button-1395-btnInnerEl").click()


# Download CSV File

time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#gridexport-1303-toolEl").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#combo-1402-inputEl").click()
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div[10]/div[1]/ul/li[3]").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#button-1407-btnInnerEl").click()


# Pull the most recent CSV file from downloads folder

time.sleep(4)
list_of_files = glob.glob('/Users/michaelangulo/Downloads/*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)


# Create new list of only the store locations in the file and filter out duplicate store names

locations = []

with open (latest_file, "r") as latest_file:
    reader = csv.reader(latest_file)
    
    next(reader, None) # skip cell 1
    next(reader, None) # skip cell 2
    
    for row in reader:
        if row[0] not in locations: 
            locations.append(row[0]) 
           
locations.pop()   
print(locations)


# loop through list of stores and reconcile all errors on their page

sizeOfList = len(locations)

# for i in range (sizeOfList):


time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#button-1016-btnEl").click() # select location arrow
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#menuitem-1018-textEl").click() # select change location
time.sleep(1)
#driver.find_element(By.CSS_SELECTOR, "#ext-element-22").send_keys(locations[i]) 
driver.find_element(By.CSS_SELECTOR, "#ext-element-22").send_keys(locations[0]) 
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#ext-element-22").send_keys(Keys.RETURN)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#ext-element-51").click() 

# at the stores page now navigate to: location >> purchasing >> recent vendor orders >> reconcile #1
# look at that video about looping and selenium








