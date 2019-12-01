from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib2
import requests
import cgitb
import os
import csv
import string

'''

path = 'D:\\bugs.csv'


bug_list=[]
with open(path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        if row[1] != 'Id':
         print row[1]
         bug_list.append(row[1])
print bug_list       
csvFile.close()
'''

'''


#for bug in bug_list:


    chrome_options = webdriver.ChromeOptions()
    
    prefs = {'download.prompt_for_download': False,
             'download.directory_upgrade': True,
             'safebrowsing.enabled': False,
             'safebrowsing.disable_download_protection': True}
    #chrome_options.add_experimental_option('prefs', prefs)
    
    
    path=r'D:\chromedriver.exe'
    
    #driver.maximize_window()
    
    
    ticket_id=bug
    
    download_path = 'D:\\RTC_dump_2\\' + ticket_id
    
    print download_path
    try:
        os.mkdir(download_path)
        print("Directory " , download_path ,  " Created ") 
    except Exception:
        print("Directory " , download_path ,  " already exists")
        
        
    prefs['download.default_directory'] = download_path
    print prefs
    chrome_options.add_experimental_option('prefs', prefs)
    #chrome_options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
    time.sleep(10)
    
    driver.get("https://www.google.com")  
    time.sleep(10)
    search_field = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')
    
    search_field.click()
    '''
'''
    href_list = []
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
            href=elem.get_attribute("href")
            if 'https://rb-alm-20-p.de.bosch.com/ccm/resource/itemOid/com.ibm.team.workitem.Attachment/' in href:
                if href not in href_list:
                    href_list.append(href)
                    print href
                    try:
                        driver.get(href)
                    except Exception as e:
                        print e    
                        driver.get(href)
                        continue
                    
            
    
    
    time.sleep(10)
    '''
    
    #driver.quit()
    
from selenium import webdriver

search_query = raw_input("Enter the search query")
search_query = search_query.replace(' ', '+') #structuring our search query for search url.
executable_path = r'D:\chromedriver.exe'
browser = webdriver.Chrome(executable_path=executable_path)


for i in range(20):
    browser.get("https://www.google.com/search?q=" + search_query + "&start=" + str(10 * i))
    matched_elements = browser.find_elements_by_xpath('//a[starts-with(@href, "https://www.thetaranights.com")]')
    if matched_elements:
        matched_elements[0].click()
        break

browser.quit()
