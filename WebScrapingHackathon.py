# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:42:15 2022

@author: R
"""

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

def get_url(search,i):
    #temp='https://www.amazon.in/s?k={}&crid=1YJSNNU54AGDR&sprefix=laptop%2Caps%2C451&ref=nb_sb_noss_1'
    temp='https://www.amazon.in/s?k={}&page={}&qid=1651923885&ref=sr_pg_2'
    search=search.replace(" ", "+")
    return temp.format(search,i)

def extract(item,pages):
    record=[]
    for i in range(1,pages+1):
        url=get_url(item,i)
        print("")
        print(url)
        driver.get(url)
        #https://www.amazon.in/s?k=laptops&page=2&qid=1651923885&ref=sr_pg_2
        laptop_container=BeautifulSoup(driver.page_source,'html.parser')
        result=laptop_container.find_all('div',{'data-component-type':'s-search-result'})
        total_item=len(result)
        
        for j in range(total_item):
            url2="http://www.amazon.in"+result[j].h2.a.get('href')
            driver.get(url2)
            laptop=BeautifulSoup(driver.page_source,'html.parser')
            #print(laptop)
            print(j+1,end=" ")
            ###
            name=laptop.find('span',class_='a-size-large product-title-word-break')
            product=name.text
            ASIN=laptop.find(id='productDetails_detailBullets_sections1').text.strip()
            ASIN_no=ASIN[7:17]
            p_name=product.split(',')[0].strip()
            try:
                was_price=laptop.find('span',class_='a-price a-text-price a-size-base').text
                pp=len(was_price)
                was_price=was_price[:pp//2][1:]
                now_price=laptop.find('span', class_="a-offscreen").text[1:]
            except:
                was_price='N/A'
                now_price='N/A'
            
            try:
                review_count=laptop.find(id='acrCustomerReviewText').text
                rating=laptop.find('span', class_='a-size-medium a-color-base').text
            except AttributeError:
                review_count='N/A'
                rating='N/A'
            ########
            desc=laptop.find(id='productDetails_techSpec_section_1').text
            
            
            rec=(p_name,rating,review_count,was_price,now_price,desc,ASIN_no,url2)
            record.append(rec)
    
    with open(f'{item}.csv','w',newline="",encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['Product Name', 'Star rating', 'Review Rating','Was Price','Current price','Product Description', 'ASIN Number',' product URL'])
        writer.writerows(record)


if __name__=="__main__":
    item=input('Search: ')
    pages=int(input("How Many pages?: "))
    extract(item,pages)
    driver.close()
    
