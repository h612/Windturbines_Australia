from splinter import Browser
# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import time
from webdriver_manager.chrome import ChromeDriverManager
import re
from urllib.parse import urlparse


def ddm2dec(dms_str):

    sign = -1 if re.search('[swSW]', dms_str) else 1
    res = re.sub(r"°S|°W|°E|°N", "", dms_str)

    return sign * float(res)

def scrape():
# Dependencies


    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # def scrape():
    scraped_dict={}
    #---------------------------------------------------WORK ON THE NEWS----------------------------------------------------------------
    WT_news_site_url ="https://arena.gov.au/news/"    
    browser.visit(WT_news_site_url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')    
    uls=soup.find('section',role="main")
    top_news=[]
    top_news_p=[]
    if uls is not None:
                ul = uls.find_next('ul')
                for li in ul.findAll('li')[0:4]:#findAll
                    if(li is not None):
                        # print(li.text)
                        if  li.find("a") is not None:
                            news_title = li.find("a").get_text(strip=True)
                            print("--",news_title)
                            # name2 = li.find("h2").get_text(strip=True)
                            # print("-#-",name2)
                        if  li.find("p") is not None:
                            news_p = li.find("p").get_text(strip=True)
                            print("-$-",news_p)
                        else:
                            news_p=""

                        # news_p=li.find("p").text
                        # print(news_p)
                        top_news.append(news_title)
                        top_news_p.append(news_p)
                    print("news_title: ",news_title)
                scraped_dict['news_p']=top_news_p
                scraped_dict['news_title']=top_news

    #---------------------------------------------------WORK ON THE FEATURE IMAGE----------------------------------------------------------------
    Featured_WT_Image_site_url ="https://arena.gov.au/renewable-energy/wind/"    
    response_Featured_Img=requests.get(Featured_WT_Image_site_url)
    soup2=BeautifulSoup(response_Featured_Img.text,'html.parser')    
    featured_image_url=soup2.find('div',class_="bg-stretch")['style']
    Featured_WT_Image_unclean=featured_image_url
    #Featured_WT_Image=Featured_WT_Image_site_url+featured_image_url

    path = urlparse(Featured_WT_Image_unclean).path  # get the path from the URL ("/washingmachine-dawlnace/")
    path = path[path.index("//"):]  # remove everything after the '-' including itself
    path = path[2:]  # remove the '/' at the starting of the path (just before 'washing')
    Featured_WT_Image =path[:len(path)-2]
    path
    scraped_dict['Featured_WT_Image']="https://"+Featured_WT_Image
    print("img url:========================= ",Featured_WT_Image)

    #---------------------------------------------------WORK ON THE LOCATION TABLE----------------------------------------------------------------
    # URL of page to be scraped
    import pandas as pd

    url = 'https://en.wikipedia.org/wiki/List_of_wind_farms_in_Australia'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('table', class_='wikitable')
    # results
    df=pd.read_html(str(results))[0]
    # convert list to dataframe
    # df=pd.DataFrame(df[0])
    df.head(15)
    import re
    row1=df['Coordinates'][0]
    r=row1[row1.find("37.2"):]
    df['Coordinates'][0]=r.replace("/ ",'')
    df['Coordinates']=df['Coordinates'].apply(lambda x: re.sub(" \ufeff","",x))
    df_split=df['Coordinates'][1:len(df['Coordinates'])-1].apply(lambda x: pd.Series(x.split("/")))
    # [1].apply(lambda x: pd.Series(x.split(" ")))
    # df['Coordinates']=
    df_split[1]
    df['Coordinates'][1:len(df['Coordinates'])-1]=df_split[1]
    # df
    rowLast=df['Coordinates'][len(df['Coordinates'])-1]
    r=rowLast[rowLast.find("/")+1:]
    df['Coordinates'][len(df['Coordinates'])-1]=r
    df['Coordinates'][len(df['Coordinates'])-1]


    df_split=df['Coordinates'].apply(lambda x: pd.Series(x.split(" ")))

    Longitude=df_split[1].apply(lambda x: ddm2dec(x))
    Latitude=df_split[0].apply(lambda x: ddm2dec(x))
    df['Latitude']=Latitude
    df['Longitude']=Longitude

    co_dict={"lat":df['Latitude'].tolist(),
    "long":df['Longitude'].tolist()}
    df['Coordinates_format']=df['Latitude'].astype(str)+','+df['Longitude'].astype(str)
    facts_html=df.to_html(classes='data')
    # print(facts_html)
    scraped_dict['facts_html']=facts_html
    import json
    jd=df[['Latitude','Longitude']].to_json(orient='records')
    
    scraped_dict['json_facts_html']=co_dict
    return scraped_dict