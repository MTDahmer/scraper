from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    scrapedata = {'article': article(browser), 'images': images(browser), 'weather' : weather(browser), 'hemisphere' : hemisphere(browser)}
    print(scrapedata)
    return scrapedata

def article(browser):
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    stuff =[]
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    #stuff = soup.find_all('li', class_ = 'slide')
    #stuff1 = stuff[0]
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text
    return news_title,news_p

def images(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_block = soup.find('a', class_ = 'button fancybox')
    img_url = img_block['data-fancybox-href']
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + img_url
    return featured_image_url

def weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    all_tweets = []
    timeline = soup.select('#timeline li.stream-item')
    for tweet in timeline:
        tweet_id = tweet['data-item-id']
        tweet_text = tweet.select('p.tweet-text')[0].get_text()
        all_tweets.append({"text": tweet_text})
    mars_weather = all_tweets[0] 
    return mars_weather

def facts(browser):
    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)
    return mars_facts

def hemisphere(browser):
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url1": "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url1": "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url3": "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url4": "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    ]
    return hemisphere_image_urls



