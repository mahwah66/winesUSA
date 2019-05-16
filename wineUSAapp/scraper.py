import time
from datetime import datetime
import re

import pandas as pd 
import pymongo
import json

from splinter import Browser
from bs4 import BeautifulSoup
import requests



def trim_all_columns(df):
    # Trim whitespace from ends of each value across all series in dataframe
    trim_strings = lambda x: x.strip() if type(x) is str else x
    return df.applymap(trim_strings)


# function to save dataframe to collection_name in MongoDB 'wines'    
def saveMongo(df, collection_name, replace=False):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['wines'] 
    if replace:
        mng_db[collection_name].drop() 
    db_cm = mng_db[collection_name]
    data = df
    data_json = json.loads(data.to_json(orient='records', date_unit='ns'))
    db_cm.insert_many(data_json)


def scrapeNew(maxpages=1):
    # maxpages is number of winemag listing pages to scrape from
    # set maxpages<=0 to scrape all new
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['wines'] 

    # does this collection exist
    if ("winesall" not in mng_db.list_collection_names()):
        # give default start date
        new_date_str = "2019,2019-02-01"
    else:
        # get last published date in database, increment one month for new date query str
        wlist = mng_db.winesall.find().sort([("dt_published", -1)])
        lastpub = wlist[0]['dt_published']
        dblast = datetime.strptime(lastpub, '%m/%d/%Y')
        nyear = int(dblast.strftime('%Y'))
        nmonth = int(dblast.strftime('%m'))+1
        if nmonth>12:
            nmonth-=12
            nyear+=1
        new_date=datetime.strptime(f'{nmonth}/1/{nyear}', '%m/%d/%Y')
        new_date_str = new_date.strftime('%Y-%m-%d')

    # set up for scrape
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # begin and end url/query string, new date goes in the middle
    urlstart ='https://www.winemag.com/?s=&drink_type=wine&country=US&pub_date_web='
    qend = '&page=1&sort_by=pub_date_web&sort_dir=desc&search_type=reviews'

    url = urlstart + new_date_str + qend
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print("-----------------------------------------")
    noresults = soup.find('div','no-results-wrapper')
    # no new results
    if noresults!=None:
        return

    # get page range, last page
    pagediv = soup.find('div','pagination')
    lis = pagediv.find_all('li')
    lastli = lis[-1]
    lastpage = int(lastli.find('a')["data-page-number"])

    if maxpages>0:
        if maxpages < lastpage:
            lastpage=maxpages
    
    # Grab a list of links for each wine's review page from the results page of WineMag reviews
    cpage = 1

    wines_url_list=[]

    while cpage<=lastpage:

        wines_ls = soup.find_all('a', class_="review-listing row" )

        for link in wines_ls: 
            href=link['href']
            wines_url_list.append(href.strip())
    
    
        cpage+=1
    
        url = urlstart + new_date_str + "&page=" + str(cpage) + "&sort_by=pub_date_web&sort_dir=desc&search_type=reviews"
        url = "https://www.winemag.com/?s=&drink_type=wine&country=US&pub_date_web=2019,2019-02-01&page="+str(cpage)+"&sort_by=pub_date_web&sort_dir=desc&search_type=reviews"
        browser.visit(url)
        time.sleep(1)
        print(f"page {cpage}")
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
    print(f"list length {len(wines_url_list)}, and cpage = {cpage}")


    # Visit each link in list of URLs and save wine info to df

    wine_list=[]

    columns = ['title', 'wine', 'vintage', 'vinyard', 'variety', 'ava', 'region', 'state',
           'alcohol_content', 'size', 'winetype', 'price', 'score','dt_published', 'taster']

    wines_df = pd.DataFrame(wine_list, columns = columns)
    index = 0

    # Follow each link and scrape the wine's review

    for link in wines_url_list:
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        wine_elements=[]

        title=soup.find('div', class_="article-title" ).text.split('(')[0]
        score=soup.find('div', class_='rating').text.split()[0]

        primary_info=soup.find('ul', 'primary-info')
        lis = primary_info.find_all('li','row')
        for li in lis:
            labeldiv = li.find('div','info-label')
            label = labeldiv.text.lower()
            infodiv = li.find('div','info')
            info = infodiv.text.strip()
        
            if "price" in label:
                prices=info.split(',')
                price=prices[0]
            elif "designation" in label:
                vinyard=info
            elif "variety" in label:
                variety=info
            elif "appellation" in label:
                appL = info.split(',')
                alen = len(appL)
                # assume country is last
                state = appL[-2]
                region=""
                ava=""
                if alen>2:
                    region = appL[-3]
                    if alen>3:
                        ava = appL[-4]
            elif "winery" in label:
                wine=info
    
        secondary_info=soup.find('ul', 'secondary-info')
        lis = secondary_info.find_all('li','row')
        for li in lis:
            labeldiv = li.find('div','info-label')
            label = labeldiv.text.lower()
            infodiv = li.find('div','info')
            info = infodiv.text.strip()
        
            if "alcohol" in label:
                alcohol = info
            elif "size" in label:
                size = info
            elif "category" in label:
                winetype = info
            elif "date" in label:
                dt_published = info
            
        taster=soup.find('div', class_='name').text
        checkvin = re.findall('\d\d\d\d', title)
        if (len(checkvin)>0):
            vintage = re.findall('\d\d\d\d', title)[0]
        else:
            vintage = 'NV'

        wines_df.at[index, "title"] = title
        wines_df.at[index, "wine"] = wine
        wines_df.at[index, "vintage"] = vintage    
        wines_df.at[index, "vinyard"] = vinyard
        wines_df.at[index, "variety"] = variety
        wines_df.at[index, "ava"] = ava
        wines_df.at[index, "region"] = region
        wines_df.at[index, "state"] = state
        wines_df.at[index, "alcohol_content"] = alcohol
        wines_df.at[index, "size"] = size
        wines_df.at[index, "winetype"] = winetype
        wines_df.at[index, "score"] = score   
        wines_df.at[index, "price"] = price
        wines_df.at[index, "dt_published"] = dt_published
        wines_df.at[index, "taster"] = taster
    
        print(index)
        index += 1


    # trim white space around strings in df
    wines_df = trim_all_columns(wines_df)

    # convert price to numeric/ nearest dollar
    wines_df['price'] = wines_df['price'].str.replace('$', '')
    wines_df['price'] =  pd.to_numeric(wines_df['price'].fillna(0))
    wines_df['price'] = wines_df['price'].round(0).astype(int)

    saveMongo(wines_df, "winesall", replace=False)


