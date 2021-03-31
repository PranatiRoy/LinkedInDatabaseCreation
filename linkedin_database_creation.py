cd="C:\\Users\\Pranati\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe"
import time
import pandas as pd
from bs4 import BeautifulSoup # for the beautiful soup we have to send the source code for the page.
from selenium import webdrive

#opening browser and signin to linkedin
browser=webdriver.Chrome(cd)
browser.get("https://www.linkedin.com/login")
un=browser.find_element_by_xpath('//input[@id="username"]') #locate the element and click
un.send_keys("=====") #send input user id to that
passwrd=browser.find_element_by_xpath('//input[@id="password"]')
passwrd.send_keys("=====") #write the password 
sign_in=browser.find_element_by_xpath('//button[@class="btn__primary--large from__button--floating"]')
sign_in.click( )

#getting the connection list
browser.get("https://www.linkedin.com/mynetwork/invite-connect/connections")
time.sleep(2)

num_of_connections= (browser.find_element_by_xpath('//h1[@class="t-18 t-black t-normal"]')).text
num_of_connections=int(num_of_connections[0:4])

#scroll over all the connections
i=0
while (i<num_of_connections):
	time.sleep(1)
	pgsource=browser.page_source # return the source code
	ref=BeautifulSoup(pgsource,'html.parser') #it refers to the soup element /translated element
	selection_all=ref.findAll('li',{'class':"mn-connection-card artdeco-list ember-view"})
	i=len(selection_all)
	browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
	time.sleep(0.1)
	browser.execute_script('window.scrollTo(0,0);')
	time.sleep(0.1)
	
print(len(selection_all))

#Extracting the data.
connection_list=[]
for i in selection_all:
	q=i.find('a',{'class':"ember-view mn-connection-card__link"})
	#q=browser.find_element_by_xpath('//a[@class="ember-view mn-connection-card__link"]')
	profile_link=q.get('href')
	#print(profile_link)
	connection_list.append(profile_link)

url1="https://www.linkedin.com/"
name=[]
CP=[]
CI=[]
c=0
for i in connection_list:
	url=url1+i
	browser.get(url)
	time.sleep(2)
	p=browser.find_element_by_xpath('//li[@class="inline t-24 t-black t-normal break-words"]').text
	name.append(p)
	q=browser.find_element_by_xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]').text
	CP.append(q)
	ci=url+"/detail/contact-info/"
	CI.append(ci)
	c=c+1
	print(c)
dict1={'Name':name,'Current_Position':CP,'Contact_Info':CI}
df=pd.DataFrame(dict1)
df.to_csv("C:\\Users\\Pranati\\linkedin_database.csv")

print("Done")
