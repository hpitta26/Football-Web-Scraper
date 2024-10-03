from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv

teams = {
    "Barcelona": ["A"],
    "Real Madrid": ["B"],
    "Atletico Madrid": ["C"],
    "Real Sociedad": ["D"],
    "Villarreal": ["E"],
    "Real Betis": ["F"],
    "Osasuna": ["G"],
    "Athletic Club": ["H"],
    "Mallorca": ["I"],
    "Girona": ["J"],
    "Rayo Vallecano": ["K"],
    "Sevilla": ["L"],
    "Celta Vigo": ["M"],
    "Cadiz": ["N"],
    "Getafe": ["O"],
    "Valencia": ["P"],
    "Almeria": ["Q"],
    "Valladolid": ["R"],
    "Espanyol": ["S"],
    "Elche": ["T"]
}

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

pageUrl = 'https://www.laliga.com/en-GB/laliga-easports/results/2022-23/gameweek-'
matchNum = 1 # Page index of the first round of the 2X/2Y LaLiga Season
firstIdx = 1 # Used for if-statements that should only execute during the 1st loop iteration
lastIdx = 38 # Page index of the last round of the 2X/2Y LaLiga Season
roundCount = 1

print("Start of for-loop: Round " + str(roundCount) + "\n")

# for i in range(matchNum, lastIdx): # MAX is exclusive (matchNum - MAX)
#     if ((i - 1) % 10 == 0) and (i != firstIdx):
#         roundCount =  roundCount + 1
#         print("Start of for-loop: Round " + str(roundCount) + "\n")

driver.implicitly_wait(15) # wait for 6 seconds to make sure all fetches are processed

# //*[@id="onetrust-accept-btn-handler"]

driver.get(pageUrl + str(matchNum))
driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click() #Accept Cookies Btn (Works)
delay = driver.find_element(By.XPATH,"randomXpath")
print(driver.page_source)