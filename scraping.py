#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #initiate headless driver for deployment
    executable_path={'executable_path' : ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph=mars_news(browser)

    #Run all scraping functions and store results in dictionary
    data={
        "news_title":news_title,
        "news_paragraph":news_paragraph, 
        "featured_image":featured_image(browser),
        "facts":mars_facts(), 
        "last_modified":dt.datetime.now()
    }

    #stop web driver and return data
    browser.quit()
    return data

##news title and summary scrape

def mars_news(browser):

    #Visit mars website
    url= 'https://redplanetscience.com'
    browser.visit(url)

    #Optional Delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #HTML Parser
    html=browser.html
    news_soup=soup(html, 'html.parser')

    #Add try/except
    try:
        slide_elem=news_soup.select_one('div.list_text')

        #Use parent element to find the first 'a' tag and save it as 'news_title'
        news_title=slide_elem.find('div' , class_='content_title').get_text()

        #Use parent element to find paragraph text
        news_p=slide_elem.find('div' , class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p




# ## Featured Images

def featured_image(browser):
    #Visit URL
    url='https://spaceimages-mars.com'
    browser.visit(url)

    #Finda nd click full image button
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Prase resulting html with soup
    html=browser.html
    img_soup=soup(html, 'html.parser')

    #add try/except
    try:

        #Find relative image URL
        img_url_rel=img_soup.find('img' , class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    #Use basre URL to create absolute URL
    img_url=f'https://spaceimages-mars.com/{img_url_rel}'

    
    return img_url



### Mars Facts

def mars_facts():

    try:
        #use 'read html' to scrape factss table into a df
        df=pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #Assign columns and set index
    df.columns=['Description' , 'Mars' , 'Earth']
    df.set_index('Description' , inplace=True)

    #convert DF to HTML add bootstrap
    return df.to_html()

if __name__ == "__main__":
    #if running as script, print scraped data
    print(scrape_all())