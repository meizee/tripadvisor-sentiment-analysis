from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import pandas as pd
from time import sleep
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)
# https://www.tripadvisor.com/Attractions-g297698-Activities-Nusa_Dua_Nusa_Dua_Peninsula_Bali.html
url = "https://www.tripadvisor.com/Attractions-g297698-Activities-oa*-place_state.html" 
# Nusa_Dua_Nusa_Dua_Peninsula_Bali
place="Nusa_Dua" #You can replace your place here.
state="Nusa_Dua_Peninsula_Bali"       #You can replace your state here.
url = url.replace("place",place)
url = url.replace("state",state)
links=[]
location_names=[]
for i in range(0,15,10):
    target_url=url.replace("*",str(i))
    driver.get(target_url)
    bsobj = BeautifulSoup(driver.page_source, 'html.parser')
    print("start")
    place_div=bsobj.find('div',{'class':'fVbwn cdAAV cagLQ eZTON dofsx'})
    if place_div is None:
            break
    for div in bsobj.findAll('div',{'class':'fVbwn cdAAV cagLQ eZTON dofsx'}):
        #print(review)
        links_div=div.findChildren("a" , recursive=False)
        if len(links_div)<2:
            continue
        a = links_div[1]['href']
        #print(a)
        location_names.append(a.split('-')[-2])
        a = 'https://www.tripadvisor.com'+ a
        a = a[:(a.find('Reviews')+7)] + '-or{}' + a[(a.find('Reviews')+7):]
        #print(a)
        links.append(a)

reviews_list = []
reviews_location=[]
rating_list = []
date_list = []
target_links = []
count=0
for link in links:
    location=location_names[count]
    count=count+1
    flag=0
    maks=0
    
    # if link == 'https://www.tripadvisor.com/Attraction_Review-g297698-d939620-Reviews-or{}-Nusa_Dua_Beach-Nusa_Dua_Nusa_Dua_Peninsula_Bali.html#REVIEWS':
    #     maks= 30
    # elif link == 'https://www.tripadvisor.com/Attraction_Review-g297698-d939620-Reviews-or{}-Nusa_Dua_Beach-Nusa_Dua_Nusa_Dua_Peninsula_Bali.html#REVIEWS':
    #     maks= 20
    # elif link == 'https://www.tripadvisor.com/Attraction_Review-g297698-d939620-Reviews-or{}-Nusa_Dua_Beach-Nusa_Dua_Nusa_Dua_Peninsula_Bali.html#REVIEWS':
    #     maks= 20
    # elif link == 'https://www.tripadvisor.com/Attraction_Review-g297698-d939620-Reviews-or{}-Nusa_Dua_Beach-Nusa_Dua_Nusa_Dua_Peninsula_Bali.html#REVIEWS':
    #     maks= 20

    for i in range(0,50,10):
        target_link=link.format(i)
        target_links.append(target_link)
        html2 = driver.get(target_link)
        bsobj2 = BeautifulSoup(driver.page_source,'html.parser')    
        reviews_section=bsobj2.find('div',{'class':'dHjBB'})
        if reviews_section is None:
            break
        reviews_div=reviews_section.findChildren("div",{'class':'WlYyy diXIH dDKKM'} , recursive=True)
        rating_svg = reviews_section.findChildren("svg", {'class':'RWYkj d H0'}, recursive=True)
        date_div=reviews_section.findChildren("div", {'class':'WlYyy diXIH cspKb bQCoY'}, recursive=True)

        if(len(reviews_div)==0 or 1==flag):
            flag=0
            break
      
        for r, rs, d in zip(reviews_div, rating_svg, date_div):
            # print(rs['aria-label'])
            if r.span is None or rs is None or d is None:
                flag=1
                break
            reviews_list.append(str(r.span.text.strip()))
            reviews_location.append(location)
            rating_list.append(rs['title'])
            # print(d.text.strip())
            date_list.append(d.text.strip())
            #sleep(1)
            # print(str(r.span.text.strip()))
            # print(rs['title'])
        
        dataframe = pd.DataFrame({'location':reviews_location,'content':reviews_list, 'rating':rating_list, 'date':date_list})
        dataframe.to_csv("./tripadvisor_reviews_nusadua.csv",index=True)#saving to the csv, you can change the name
    
    # print(target_links)