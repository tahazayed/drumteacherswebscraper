# -*- coding: utf-8 -*-
import warnings
import sys
import pandas as pd



#https://medium.com/@hoppy/how-to-test-or-scrape-javascript-rendered-websites-with-python-selenium-a-beginner-step-by-c137892216aa
#https://medialab.github.io/artoo/
warnings.filterwarnings("ignore")

from time import sleep
from random import randint
from selenium import webdriver
from pyvirtualdisplay import Display

class MuncherySpider():

    def __init__(self):
        pass

    # Open headless chromedriver
    def start_driver(self):

        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        
        self.driver = webdriver.Chrome("/var/chromedriver/chromedriver")
        sleep(4)

    # Close chromedriver
    def close_driver(self):
        self.display.stop()
        self.driver.quit()


    # Tell the browser to get a page
    def get_page(self, url):
        self.driver.get(url)
        sleep(randint(2,3))

    def grab_list_items(self):
        Telephone=''
        Mobile=''
        Website=''
        Teaching_Location=''
        Email=''
        Map=''
        Teacher_Name=''
        for tr in self.driver.find_elements_by_xpath('//*[@id="plugin19"]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr'):
            #try:
                tds=tr.find_elements_by_xpath('./td')
                
                currentText=tds[0].find_element_by_xpath("./strong").text
                if currentText == 'Telephone:':
                    Telephone = tds[1].text
                elif currentText == 'Mobile:':
                    Mobile = tds[1].text
                elif currentText == 'Website:':
                    Website = tds[1].text
                elif currentText == 'Teaching Location:':
                   Map = tds[1].find_element_by_xpath("./a").get_attribute('href')
                   Teaching_Location = tds[1].text.replace('\nView on map','')
                elif currentText == 'Email:':
                    Teacher_Name = tds[1].text.replace('Contact ','')
                
            #except:
            #    pass
        #return Teacher_Name,Telephone,Mobile,Website,Teaching_Location
        self.all_items={'TEACHER_NAME':Teacher_Name,'Telephone':Telephone,'Mobile':Mobile,'URL':Website,'Teaching_Location':Teaching_Location,'index':1}
      

    def parse(self,url_to_crawl):
        #self.start_driver()

        self.get_page(url_to_crawl)

        self.grab_list_items()

        #self.close_driver()

        if self.all_items:
            return self.all_items
        else:
            return False

links=[]
with open("/home/taha/findteacher/links.txt") as f:
    for line in f:
        if(line.strip() != ''):
            links.append(line.strip())                

links=list(set(links))
links.sort()


df = pd.DataFrame(columns=['TEACHER_NAME','Telephone','Mobile','URL','Teaching_Location'])
counter = -1

failed=[]
              
# Run spider
munchery = MuncherySpider()
munchery.start_driver()
for link in links:
    try:
        print(link)
        data = munchery.parse('http://www.drumteachers.co.uk/find-a-teacher/profile/?tuid='+link)
        counter=counter+1
        df.loc[counter,'TEACHER_NAME']=data['TEACHER_NAME']
        df.loc[counter,'Telephone']=data['Telephone']
        df.loc[counter,'Mobile']=data['Mobile']
        df.loc[counter,'URL']=data['URL']
        df.loc[counter,'Teaching_Location']=data['Teaching_Location']
        sleep(randint(2,3))
    except:
        print ("Unexpected error:", sys.exc_info())
        failed.append(link)
        continue 
munchery.close_driver()

df.to_csv('/home/taha/findteacher/all.csv', index = False)

with open("/home/taha/findteacher/linksFailed.txt",'a') as fo:
    fo.write("\n".join(failed))
    fo.flush()
    fo.close()

print (failed)
