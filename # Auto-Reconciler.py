# Auto-Reconciler

from pickle import APPEND
from tarfile import REGULAR_TYPES
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
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "#ext-element-102").click()
time.sleep(5)
driver.find_element(By.ID, "tool-1028-toolEl").click()
time.sleep(4)
driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div[2]/a/span").click()
time.sleep(4)
driver.switch_to.window(driver.window_handles[-1])
time.sleep(2)
element =  driver.find_element(By.CSS_SELECTOR, "#ext-element-22")
element.send_keys(location)
time.sleep(1)
element.send_keys(Keys.RETURN)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#ext-element-51").click()

# display page of stores to be reconciled

time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "#button-1191-btnInnerEl").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#menuitem-1194-textEl").click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#menuitem-1201-textEl").click()
time.sleep(4)
driver.find_element(By.ID, "cescombogridpicker-1277-inputEl").click()
time.sleep(4)
driver.find_element(By.ID, "cescombogridpicker-1277-inputEl").send_keys(Keys.BACKSPACE)
time.sleep(4)
driver.find_element(By.ID, "cescombogridpicker-1277-inputEl").send_keys("fleet")
time.sleep(2)
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

time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#button-1016-btnEl").click() # select location arrow
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "#menuitem-1018-textEl").click() # select change location

for i in range (sizeOfList):

    time.sleep(1)
    #driver.find_element(By.CSS_SELECTOR, "#ext-element-22").send_keys(locations[i]) 
    driver.find_element(By.CSS_SELECTOR, "#ext-element-22").send_keys(locations[i]) 
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#ext-element-22").send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#ext-element-51").click() 

    # at the stores page now navigate to: location >> purchasing >> recent vendor orders >> reconcile #1
    # look at that video about looping and selenium


    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#button-1059-btnInnerEl").click() # click purchasing
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#menuitem-1063-textEl").click() # click recent vendor orders
    time.sleep(2)


    # reconcile all over/short errors

    # Choose the first reconcile on page and click it. This chooses the "Ready for Reconcile option"
    # Click next reconcile
    # Click reconcile action button

    # if no other pop up, go see if theres any more to reconcile for that store, if not then do the next store

    # The structure goes as follows:

    driver.find_element(By.PARTIAL_LINK_TEXT, "Reconcile").click()

    while True:
        try: # to resolve an over/short error
            time.sleep(2)
            driver.find_element(By.LINK_TEXT, "Reconcile").click()
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "#button-1717-btnInnerEl").click()
            time.sleep(2)
            error = driver.find_element(By.CSS_SELECTOR, "#messagebox-1002-msg").text
            print("CrunchTime! Error: " + error)
            if error == "You must adjust your Invoice Total so that the Over/Short Field is equal to zero.":
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                numberField = driver.find_element(By.CSS_SELECTOR, "#displayfield-1692-inputEl").text
                time.sleep(2)
                print("... Pasting: " + numberField)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").click() 
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").send_keys(Keys.BACKSPACE)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").send_keys(numberField)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").send_keys(Keys.ENTER)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1717-btnInnerEl").click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                break

            if error == '''At least one Invoice Price is displayed in red, indicating that it varies by 100% or more from the current Issue Cost for the product.\n\nClick "OK" to continue Reconciling the order, or "Cancel" to return to the order screen.''':
                
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                numberField = driver.find_element(By.CSS_SELECTOR, "#displayfield-1692-inputEl").text
                time.sleep(2)
                print("... Pasting: " + numberField)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").click() 
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").send_keys(Keys.BACKSPACE)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").send_keys(numberField)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#numberfield-1689-inputEl").send_keys(Keys.ENTER)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1717-btnInnerEl").click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "#button-1006-btnInnerEl").click()
                time.sleep(2)
                break

        except: # stop trying, go back to the main loop and try the same thing with the next store

            print("end of process")
            time.sleep(2)
            driver.back()
            time.sleep(2)
            driver.back()

            break
# at the end click back like 3 times to get to the original working page