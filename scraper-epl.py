from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv

teams = {
    "Man City": ["A"],
    "Arsenal": ["B"],
    "Man Utd": ["C"],
    "Newcastle": ["D"],
    "Liverpool": ["E"],
    "Brighton": ["F"],
    "Aston Villa": ["G"],
    "Tottenham Hotspur": ["H"],
    "Brentford": ["I"],
    "Fulham": ["J"],
    "Crystal Palace": ["K"],
    "Chelsea": ["L"],
    "Wolves": ["M"],
    "West Ham": ["N"],
    "Bournemouth": ["O"],
    "Nott'm Forest": ["P"],
    "Everton": ["Q"],
    "Leicester": ["R"],
    "Leeds": ["S"],
    "Southampton": ["T"]
}

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# 2022/23 Season (range(74911 - 75291))
# 2021/22 Season (range(66342 - 66722))
pageUrl = 'https://www.premierleague.com/match/7'
matchNum = 4911 # Page index of the first game of the 2X/2Y EPL Season
firstIdx = 4911 # Used for if-statements that should only execute during the 1st loop iteration
lastIdx = 5291 # Page index of the last game of the 2X/2Y EPL Season
roundCount = 1

print("Start of for-loop: Round " + str(roundCount) + "\n")

for i in range(matchNum, lastIdx): # MAX is exclusive (matchNum - MAX)
    if ((i - 1) % 10 == 0) and (i != firstIdx):
        roundCount =  roundCount + 1
        print("Start of for-loop: Round " + str(roundCount) + "\n")

    driver.get(pageUrl + str(matchNum))
    
    #  <- FIND TEAMS THAT ARE PLAYING ->
    # print(driver.title)
    words = driver.title.split(' ')
    v = words.index('v')
    com = 0
    if ',' in words[v + 1]:
        com = v + 1
    else:
        com = v + 2

    teamOne = ""
    if v == 2:
        teamOne = words[0] + ' ' + words[1]
    else:
        teamOne = words[0]

    teamTwo = ""
    if com == v+2:
        teamTwo = words[v + 1] + ' ' + words[v + 2]
    else:
        teamTwo = words[v + 1]
        
    teamTwo = teamTwo[:len(teamTwo)-1]

    print(teamOne + " vs " + teamTwo)

    # <- PRESS (ACCEPT COOKIES & STATS) & WAIT ->
    if matchNum == firstIdx: 
        driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click() #This works (Accepts All Cookies)
        time.sleep(0.5) # ensure Accept Cookies has been clicked

    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/section[2]/div[2]/div/div[1]/div/div/ul/li[3]').click() #This works (Clicks the Stats Button)

    driver.implicitly_wait(6) # wait for 6 seconds to make sure all fetches are processed

    # print('Before Sleep')
    time.sleep(0.2) # sleeps for 250ms, this allows for both of the buttons to be clicked before the page is printed
    # print('After Sleep')
    # print(driver.page_source)

    # <- FIND OFFSIDE STATS ->
    statContainer = driver.find_element(By.CLASS_NAME, "matchCentreStatsContainer") #finds the <tbody> that holds the Match Stats
    # print(statContainer.get_attribute('innerHTML'))

    statList = statContainer.find_elements(By.CSS_SELECTOR, "*")
    # print(len(statList))

    teamOneOff = int(statList[58].text)
    labelOff = statList[60].text
    teamTwoOff = int(statList[62].text)
    # print(type(teamOneOff))
    # print(type(teamTwoOff))
    print(str(teamOneOff) + " " + labelOff + " " + str(teamTwoOff) + "\n")
    
    # <- INSERT OFFSIDES & INCREMENT MATCH NUMBER ->
    if labelOff == 'Offsides':
        # Add letter of other team if 0 offsides
        # Append LowerCase: offside == 0, UpperCase: offside >= 4
        if teamOneOff == 0: 
            if teamTwoOff >= 4:                                         # Case 1: one == 0 and two >= 4
                teams[teamOne].append(teams[teamTwo][0].lower())
                teams[teamTwo].append(teams[teamOne][0] + "-" + str(teamTwoOff))
            else:                                                       # Case 2: one == 0 and two < 4
                teams[teamOne].append(teams[teamTwo][0].lower())
                teams[teamTwo].append(teamTwoOff)         
        elif teamTwoOff == 0: 
            if teamOneOff >= 4:                                         # Case 3: two == 0 and one >= 4
                teams[teamTwo].append(teams[teamOne][0].lower())
                teams[teamOne].append(teams[teamTwo][0] + "-" + str(teamOneOff))
            else:                                                       # Case 4: two == 0 and one < 4
                teams[teamTwo].append(teams[teamOne][0].lower())
                teams[teamOne].append(teamOneOff)    
        elif teamOneOff >= 4:   
            if teamTwoOff >= 4:                                         # Case 5: one >= 4 and two >= 0
                teams[teamOne].append(teams[teamTwo][0] + "-" + str(teamOneOff))
                teams[teamTwo].append(teams[teamOne][0] + "-" + str(teamTwoOff))  
            else:                                                       # Case 6: one >= 4 and two != 0
                teams[teamOne].append(teams[teamTwo][0] + "-" + str(teamOneOff))
                teams[teamTwo].append(teamTwoOff)
        elif teamTwoOff >= 4:                                           # Case 7: two >= 4 and one !=0
            teams[teamTwo].append(teams[teamOne][0] + "-" + str(teamTwoOff))
            teams[teamOne].append(teamOneOff)   
        else:                                                           # Case 8: everything else
            teams[teamOne].append(teamOneOff)
            teams[teamTwo].append(teamTwoOff)        
    else:                                                               # Case 9: one == 0 and two == 0
        teams[teamOne].append(None)
        teams[teamTwo].append(None)
    
    matchNum = matchNum + 1


print(teams)


# <- OPEN CSV WRITER & WRITE DATA TO FILE ->
fileName = "epl22-23.csv"
# set newline to be '' so that that new rows are appended without skipping any
f = csv.writer(open(fileName, 'w', newline='')) #'w' -> open for writing, truncating the file first
# write a new row as a header
partOne = ['Team', 'Nickname']
partTwo = list(range(1,39))
f.writerow(partOne + partTwo) #These are the column names


for i in range(0, 20):
    f.writerow([list(teams.keys())[i]] + teams[list(teams.keys())[i]])







# Useful Lines of Code that I Didn't Need

# //*[@id="onetrust-accept-btn-handler"]                                        # Xpath to Accept Cookies button
# //*[@id="mainContent"]/div/section[2]/div[2]/div/div[1]/div/div/ul/li[3]      # Xpath to Stats button
# innerHTML = driver.execute_script("return document.body.innerHTML")           # This is used to make the driver execute JS script
# //*[@id="mainContent"]/div/section[2]/div[2]/div/div[1]/div/div/ul/li[3]
# //*[@id="mainContent"]/div/section[2]/div[2]/div/div[1]/div/div/ul/li[3]



# <- TEAM LIST BY SEASON ->
# Letters are meant to be put when there are 0 offsides.

# 2022/23 Season (range(74911 - 75291))
# teams = {
#     "Man City": ["A"],
#     "Arsenal": ["B"],
#     "Man Utd": ["C"],
#     "Newcastle": ["D"],
#     "Liverpool": ["E"],
#     "Brighton": ["F"],
#     "Aston Villa": ["G"],
#     "Tottenham Hotspur": ["H"],
#     "Brentford": ["I"],
#     "Fulham": ["J"],
#     "Crystal Palace": ["K"],
#     "Chelsea": ["L"],
#     "Wolves": ["M"],
#     "West Ham": ["N"],
#     "Bournemouth": ["O"],
#     "Nott'm Forest": ["P"],
#     "Everton": ["Q"],
#     "Leicester": ["R"],
#     "Leeds": ["S"],
#     "Southampton": ["T"]
# }

# 2021/22 Season (range(66342 - 66722))
# teams = {
#     "Man City": ["A"],
#     "Liverpool": ["B"],
#     "Chelsea": ["C"],
#     "Tottenham Hotspur": ["D"],
#     "Arsenal": ["E"],
#     "Man Utd": ["F"],
#     "West Ham": ["G"],
#     "Leicester": ["H"],
#     "Brighton": ["I"],
#     "Wolves": ["J"],
#     "Newcastle": ["K"],
#     "Crystal Palace": ["L"],
#     "Brentford": ["M"],
#     "Aston Villa": ["N"],
#     "Southampton": ["O"],
#     "Everton": ["P"],
#     "Leeds": ["Q"],
#     "Burnley": ["R"],
#     "Watford": ["S"],
#     "Norwich City": ["T"]
# }