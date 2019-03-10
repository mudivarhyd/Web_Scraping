#!/usr/bin/env python
# coding: utf-8

# In[24]:


# Import Beautiful Soup and splinter
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


# In[25]:


# Choose executable path to driver for Mac
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# In[3]:


# Vist NASA Site
def scrape():
    browser = init_browser()
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)


    # In[4]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[5]:


    #print(soup.prettify())


    # In[6]:


    # Recent mars news article, title

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    news_date = soup.find("div", class_="list_date").text

    print(f"Article Date:  {news_date}")
    print(f"Article Title:  {news_title}")
    print(f"Article Body:  {news_p}")


    # # JPL Mars Space Images - Featured Image

    # In[7]:


    # Vist Jet Propulsion Laboratory web site to get mars images

    image_url_featured = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url_featured)


    # In[8]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')

    # Get background image url
    image_url = soup.find("article")["style"].replace("background-image: url('","").replace("');", "")
    print(image_url)

    # Get Main URL
    JPL_url = "https://www.jpl.nasa.gov"
    print(JPL_url)

    # Full path url with image
    full_image_url = JPL_url + image_url
    print(full_image_url)


    # # Mars Weather with Twitter

    # In[9]:


    # Mars weather twitter through splinter
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)


    # In[10]:


    # Create BeautifulSoup object; parse with 'html.parser'
    twitter_html = browser.html
    soup = BeautifulSoup(twitter_html, 'html.parser')

    # Elements that contain tweets
    mars_weather = soup.find("div", class_="js-tweet-text-container").text.replace("pic.twitter.com/Q9QivIo4ls","")
    print(mars_weather)


    # # Mars Facts

    # In[11]:


    # Mars facts url
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)


    # In[12]:


    # Use pandas to parse the url
    mars_facts_pd = pd.read_html(mars_facts_url)
    #print(mars_facts_pd)

    # Mars data frame
    mars_facts_df = mars_facts_pd[0]

    # Assign columns to data frame
    mars_facts_df.columns = ["Mars_Description", "Values"]
    mars_facts_df.set_index("Mars_Description", inplace=True)


    # Convert to html table
    mars_fact_html = mars_facts_df.to_html()
    mars_facts_df


    # # Mars Hemispheres

    # In[86]:


    # Mars Hemispheres url
    mars_hems_url1 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hems_url1)


    # In[87]:


    # Create BeautifulSoup object; parse with 'html.parser'
    mars_hems_html1 = browser.html
    soup = BeautifulSoup(mars_hems_html1, "html.parser")

    # Main url to add to the front
    main_url = "https://astrogeology.usgs.gov"

    # Pick all items to pic 4 pictures form list
    item_list = soup.find_all("div", class_="item")

    # List of dictonaries for empty urls
    mars_hems_list = []

    # Loop through to collect 4 urls
    for i in item_list:
        mars_title = i.find(class_="description").find("h3").text
        mars_image = i.find(class_="description").find("a")["href"]
        mars_hems_url2 = main_url + mars_image
        # Vist the mars_hems_url2 link for larger image
        browser.visit(mars_hems_url2)
        mars_hems_html2 = browser.html
        soup = BeautifulSoup(mars_hems_html2, "html.parser")
        mars_image2 = soup.find("img", class_ = "wide-image")["src"]
        large_img_url = main_url + mars_image2
        mars_hems_list.append({"title": mars_title, "img_url": large_img_url})

    mars_dict = {
        "mars_title": news_title,
        "mars_p": news_p,
        "mars_date": news_date,
        "feat_img_url": full_image_url,
        "mars_weather": mars_weather,
        "facts_table": mars_fact_html,
        "hemi_images": mars_hems_list
    }
    return mars_dict
    print("*******************************************************************")
    print(mars_dict)
        
if __name__  ==  "__main__":
    print(scrape())