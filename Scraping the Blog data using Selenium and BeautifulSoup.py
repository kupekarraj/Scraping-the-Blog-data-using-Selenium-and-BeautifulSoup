#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing the required libraries
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


# In[ ]:


#initialise the web driver
browser = webdriver.Chrome(ChromeDriverManager().install())


# In[ ]:


#importing the input file
linkedIn_urls = pd.read_csv(r"your file path goes here")
tourism_urls=linkedIn_urls["URLs"].tolist()


# In[ ]:


#creating an empty list to append the outputs
Post_Text=[]
Post_URL=[]
Post_Date=[]
Type=[]


# In[ ]:


for tourism_url in tourism_urls:
    browser.get(tourism_url)
    time.sleep(2)
    
    #Check out page source code
    company_page=browser.page_source
    
    #Use Beautiful Soup to get access tags
    linkedin_soup=bs(company_page,'lxml')
    
    #Find the post blocks
    containers = linkedin_soup.find_all("div",{"class":"post-item col-sm-12 col-md-4 col-lg-4"})
    print("The length of the total posts for",tourism_url, "is:",len(containers))
    
    
    #Looping through the posts and appending them to the lists
    for container in range(len(containers)):
        try:
            #post_text=container.find("h3",{"class":"text-limit"}).text
            post_text=browser.find_elements(By.XPATH,"//h3[@class='text-limit']")[container].text
            Post_Text.append(post_text)
        except:
            Post_Text.append("error")
        
        container_=container + 1
        
        try:
            #post_url=container.find("h3",{"class":"text-limit"}).text
            post_url=browser.find_elements(By.XPATH,"//a[@class='more-link']")[container_].get_attribute('href')
            Post_URL.append(post_url)
        except:
            Post_URL.append("error")
        
        try:
            post_date=browser.find_elements(By.XPATH,"//time[@class='date mb-2 d-block']")[container_].text
            Post_Date.append(post_date)
        except:
            Post_Date.append("error")
        
        Type.append(tourism_url)
        print(post_text)
        print(post_date)
        print("Done with",tourism_url)


# In[ ]:


data = {
    "Post Text": Post_Text,
    "Post URL": Post_URL,
    "Post Date": Post_Date,
    "Type": Type
}

df = pd.DataFrame(data)


# In[ ]:


df.head(30)


# In[ ]:


df.to_csv(r'/Users/rajkupekar/Desktop/Scorebuddy_Output5.csv', index=False)

