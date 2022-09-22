#!/usr/bin/env python
# coding: utf-8

# In[164]:


#cell: init driver


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument(r'--user-data-dir=C:\Users\write\OneDrive\Desktop\small-programs\web scraping projects\profileUpwork')

path = ChromeDriverManager().install()
with open(path, "rb") as f:   
    filedata = f.read()
filedata = filedata.replace(b'$cdc_asdjflasutopfhvcZLmcfl_',b'$btlhsaxJbTXmBATUDvTRhvcZLm_')
with open(path, "wb") as f:   
    f.write(filedata)

driver = webdriver.Chrome(service=Service(path),options=option)
driver.get("https://www.upwork.com")
driver.maximize_window()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pickle
import sys
sys.setrecursionlimit(100000) #is set to allow pickle work with larger files

class TagData: #all data about tag is stored in this class
    def __init__(self,tagName,entry,intermediate,expert,prop5,prop510,prop1015,prop1520,prop2050,previousClients,paymentVerified,hourly,fixedPrice,fp100,
                 fp100500,fp5001k,fp1k5k,fp5k,projLen1,projLen13,projLen36,projLen6,hoursLess30,hoursMore30,hires0,hires19,
                 hires10,connect2,connect4,connect6):
        self.tagName = tagName
        self.entry = entry
        self.intermediate = intermediate
        self.expert = expert
        self.prop5 = prop5
        self.prop510 = prop510
        self.prop1015 = prop1015
        self.prop1520 = prop1520
        self.prop2050 = prop2050
        self.previousClients = previousClients
        self.paymentVerified = paymentVerified
        self.hourly = hourly
        self.fixedPrice = fixedPrice
        self.fp100 = fp100
        self.fp100500 = fp100500
        self.fp5001k = fp5001k
        self.fp1k5k = fp1k5k
        self.fp5k = fp5k
        self.projLen1 = projLen1
        self.projLen13 = projLen13
        self.projLen36 = projLen36
        self.projLen6 = projLen6
        self.hoursLess30 = hoursLess30
        self.hoursMore30 = hoursMore30
        self.hires0 = hires0
        self.hires19 = hires19
        self.hires10 = hires10
        self.connect2 = connect2
        self.connect4 = connect4
        self.connect6 = connect6

class customNewButton(object): #custom wait in google login for next window to load
  def __init__(self, element):
    self.element = element

  def __call__(self, driver):
    buttonNext2 = driver.find_element(By.XPATH , "//*/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
    if buttonNext2.id != self.element.id:
        return buttonNext2
    else:
        return False

class customReload(object): #custom wait until results load after search input
  def __init__(self, oldEntry,oldIntermediate,oldExpert):
    self.oldEntry = oldEntry
    self.oldIntermediate = oldIntermediate
    self.oldExpert = oldExpert

  def __call__(self, driver):
    newEntry = driver.find_element(By.XPATH , "//*[@id='main']/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[1]/label/span[2]/small")
    newIntermediate = driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[2]/label/span[2]/small')
    newExpert = driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[3]/label/span[2]/small')
    if (newEntry.text != self.oldEntry or newIntermediate.text != self.oldIntermediate or newExpert.text != self.oldExpert
    or (newEntry.text == 0 and newIntermediate.text == 0 and newExpert.tex == 0)):
        return True
    else:
        return False

def captchaHandlerResult(elementSearch):
    try:
        result = elementSearch()
    except:
        a = input()
        result = elementSearch()
    finally:
        return result
def captchaHandler(action):
    try:
        action()
    except:
        a = input()
        action()


# In[165]:


#function per page approach to handle captcha exceptions.
#cell: colecting data

def mainPage():
    global finishedGlobal
    goToSearchPage = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.XPATH,'//button[@data-test="job-search-button"]')))
    goToSearchPage.click()
    finishedGlobal = True

def searchPage():
    
    searchNotActive = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/section/div[1]/div[1]/div[1]/div/div/div/div/input')))
    searchNotActive.click()

    search = WebDriverWait(driver, 10).until( 
        EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/section/div[1]/div[1]/div[1]/div/span/div/div[1]/div/input')))
    searchButton = driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/section[1]/div[1]/div[1]/div[2]/button')


    with open("savedTagsList", "rb") as f:   
        myStoredList = pickle.load(f)

    time.sleep(1)
    global resultsGlobal
    global startAtGlobal
    global finishedGlobal
    upTo = 4 #len(myStoredList)
    for i in myStoredList[startAtGlobal:upTo]:
        oldEntry = driver.find_element(By.XPATH , "//*[@id='main']/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[1]/label/span[2]/small")
        oldEntryStr = oldEntry.text #need to make string variable because elements get reloaded.
        oldIntermediate = driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[2]/label/span[2]/small')
        oldIntermediateStr = oldIntermediate.text
        oldExpert = driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[3]/label/span[2]/small')
        oldExpertStr = oldExpert.text
        print(i)
        search.send_keys(Keys.CONTROL,'a')
        search.send_keys(i)
        time.sleep(1)
        searchButton.click()
        WebDriverWait(driver, 15).until(customReload(oldEntryStr,oldIntermediateStr,oldExpertStr))
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        filters = soup.find(attrs={"data-test": "filters-sidebar"})
        counts = filters.find_all('small',attrs={"class": "text-muted"})
        l = []
        s = 's'
        myTable = s.maketrans('','','()')
        for c in counts:
            l.append(int(c.string.translate(myTable)))
        o = TagData(i,*l)
        resultsGlobal.append(o)
        startAtGlobal+=1
    finishedGlobal = True

finishedGlobal = False
while(True):
    try:
        mainPage()
    except:
        a = input()
    if (finishedGlobal):
        break

startAtGlobal = 0
resultsGlobal = []
finishedGlobal = False
while(True):
    try:
        searchPage()
    except:
        a = input()
    if (finishedGlobal):
        break


# In[89]:


# In[97]:


#not used anymore, because i now use browser profile, and login happens automatically.
#cell: navigate to search page
#How to navigate to search page manualy: login, then just click the button with magnifying glass symbol on the right of 
#search input field.

# accept = WebDriverWait(driver, 10).until( 
#     EC.presence_of_element_located((By.ID,"onetrust-accept-btn-handler"))
# )
# time.sleep(2)
# accept.click()
# login = WebDriverWait(driver, 5).until( 
#     EC.presence_of_element_located((By.XPATH,"//a[@class='nav-item login-link d-none d-lg-block px-20']"))
# )
# time.sleep(5)
# login.click()
# googleConnect = WebDriverWait(driver, 5).until( 
#     EC.presence_of_element_located((By.XPATH,'//*[@id="login_google_submit"]'))
# )
# time.sleep(5)
# googleConnect.click()

# WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
# driver.switch_to.window(driver.window_handles[1])

# email = driver.find_element(By.XPATH , "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input")
# time.sleep(5)
# email.send_keys('fakem7506@gmail.com')

# buttonNext = driver.find_element(By.XPATH , "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
# time.sleep(5)
# buttonNext.click()

# password = WebDriverWait(driver, 5).until( 
#     EC.presence_of_element_located((By.XPATH , "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"))
# )
# time.sleep(5)
# password.send_keys('zaidimas8')

# buttonNext2 = WebDriverWait(driver, 5).until( 
#     customNewButton(buttonNext)
# )
# time.sleep(5)
# buttonNext2.click()

# WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(1))
# driver.switch_to.window(driver.window_handles[0])

# suggestionClose = WebDriverWait(driver, 15).until( 
#     EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div/aside/div/div[1]/div[1]/section/div[2]/div[2]/div/div/div/div[2]/button'))
# )
# suggestionClose.click()

# search = driver.find_element(By.XPATH , '//button[@data-test="job-search-button"]')
# search.click()


# In[152]:


#failed approach to handle captchas on every driver action. Fails because webpage gets reloaded and elements get lost.
#cell: colecting data
#different behaviour: if search field wasnt clicked then 4 lines about searchNotActive should be uncommented, but if it was clicked then should comment them.

# goToSearchPage = captchaHandlerResult(lambda : WebDriverWait(driver, 10).until( 
#     EC.presence_of_element_located((By.XPATH,'//button[@data-test="job-search-button"]')))
# )
# captchaHandler(lambda : goToSearchPage.click())
# time.sleep(2) #wait for captcha to pop up

# searchNotActive = captchaHandlerResult(lambda : WebDriverWait(driver, 10).until( 
#     EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/section/div[1]/div[1]/div[1]/div/div/div/div/input')))
# )
# captchaHandler(lambda : searchNotActive.click())

# search = captchaHandlerResult(lambda : WebDriverWait(driver, 10).until( 
#     EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/section/div[1]/div[1]/div[1]/div/span/div/div[1]/div/input')))
# )
# searchButton = captchaHandlerResult(lambda : driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[2]/div/div[2]/div/section[1]/div[1]/div[1]/div[2]/button'))


# with open("savedTagsList", "rb") as f:   
#     myStoredList = pickle.load(f)

# results = []
# time.sleep(1)
# startAt = 0
# upTo = 2#len(myStoredList)
# for i in myStoredList[startAt:upTo]:
#     oldEntry = captchaHandlerResult(lambda : driver.find_element(By.XPATH , "//*[@id='main']/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[1]/label/span[2]/small"))
#     oldEntryStr = oldEntry.text #need to make string variable because elements get reloaded.
#     oldIntermediate = captchaHandlerResult(lambda : driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[2]/label/span[2]/small'))
#     oldIntermediateStr = oldIntermediate.text
#     oldExpert = captchaHandlerResult(lambda : driver.find_element(By.XPATH , '//*[@id="main"]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div[3]/label/span[2]/small'))
#     oldExpertStr = oldExpert.text
#     print(i)
#     captchaHandler(lambda : search.send_keys(Keys.CONTROL,'a'))
#     captchaHandler(lambda : search.send_keys(i))
#     time.sleep(1)
#     captchaHandler(lambda : searchButton.click())
#     captchaHandlerResult(lambda : WebDriverWait(driver, 15).until( 
#         customReload(oldEntryStr,oldIntermediateStr,oldExpertStr))
#     )
#     source = driver.page_source
#     soup = BeautifulSoup(source, 'html.parser')

#     filters = soup.find(attrs={"data-test": "filters-sidebar"})
#     counts = filters.find_all('small',attrs={"class": "text-muted"})
#     l = []
#     s = 's'
#     myTable = s.maketrans('','','()')
#     for c in counts:
#         l.append(int(c.string.translate(myTable)))
#     o = TagData(i,*l)
#     results.append(o)


# In[166]:


driver.quit()


# In[ ]:


print(resultsGlobal)

