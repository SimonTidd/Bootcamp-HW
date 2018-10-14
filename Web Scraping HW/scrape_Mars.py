from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    Mars_data = {}

    url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #### syntax to pull data back in ####
    #### Have figured out the building the overall dictionary piece the end ####
    #### basic code pasted here ####

    

# In[2]:


# URL of page to be scraped
url_mars = 'https://mars.nasa.gov/news/'
url_JPL='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
url_Mars_weather='https://twitter.com/marswxreport?lang=en'
url_Mars_facts='https://space-facts.com/mars/'
url_Mars_hemi_photos='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[3]:


# Retrieve page with the requests module
response_mars = requests.get(url_mars)


# In[4]:


# Create BeautifulSoup object; parse with 'html.parser'
soup_mars = BeautifulSoup(response_mars.text, 'html.parser')
# Examine the results, then determine element that contains sought info
print(soup_mars.prettify())


# In[5]:


story_title = soup_mars.find('div', class_= 'content_title').text
story_blurb = soup_mars.find('div', class_='rollover_description_inner').text


# In[6]:


print(len(story_title))


# In[7]:


print(len(story_blurb))


# In[8]:


print(story_title)


# In[9]:


print(story_blurb)


# In[10]:


#Get JPL result
response_JPL = requests.get(url_JPL)
soup_JPL = BeautifulSoup(response_JPL.text, 'html.parser')
print(soup_JPL.prettify())


# In[11]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url_JPL)


# In[12]:


browser.find_by_id('full_image').click()


# In[14]:


browser.find_by_text('more info     ').click()


# In[15]:


feature_img_link = browser.find_link_by_partial_href('photojournal.jpl.nasa.gov/jpeg')
print(feature_img_link)


# In[16]:


feature_img_link=feature_img_link['href']
print(feature_img_link)


# In[17]:


# Retrieve page with the requests module
response_mars_weather = requests.get(url_Mars_weather)


# In[18]:


# Create BeautifulSoup object; parse with 'html.parser'
soup_mars_weather = BeautifulSoup(response_mars_weather.text, 'html.parser')
# Examine the results, then determine element that contains sought info
print(soup_mars_weather.prettify())


# In[19]:


content_stream=soup_mars_weather.find_all(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")


# In[20]:


print(content_stream)


# In[21]:


tweets = [tweet.get_text() for tweet in content_stream]
tweets


# In[22]:


twitter_handles=soup_mars_weather.select(".stream .username")
twitter_handles


# In[23]:


handles = [handle.get_text() for handle in twitter_handles]
handles


# In[24]:


counter=0
mars_weather=tweets[0]
for handle in handles:
    while handles[counter]!="@MarsWxReport":
        counter=counter+1
        mars_weather=tweets[counter]
print(mars_weather)


# In[25]:


# Retrieve page with the requests module
response_mars_facts = requests.get(url_Mars_facts)
# Create BeautifulSoup object; parse with 'html.parser'
soup_mars_facts = BeautifulSoup(response_mars_facts.text, 'html.parser')
# Examine the results, then determine element that contains sought info
print(soup_mars_facts.prettify())


# In[26]:


#summary = soup.find('table',attrs = {'class':'tablehead'})
#tables = summary.find_all('table')
Mars_facts_table = soup_mars_facts.find('table',attrs={'class':'tablepress tablepress-id-mars'})


# In[27]:


print(Mars_facts_table)


# In[28]:


Mars_tables = pd.read_html(url_Mars_facts)


# In[29]:


Mars_tables


# In[30]:


Mars_facts = Mars_tables[0]
Mars_facts.columns = ['','A']
Mars_facts.head()


# In[31]:


Mars_facts.set_index('', inplace=True)
Mars_facts.rename(columns = {'A':''}, inplace=True)
Mars_facts.head()


# In[32]:


html_Mars_facts = Mars_facts.to_html()
html_Mars_facts.replace('\n', '')
html_Mars_facts


# In[33]:


url_Mars_hemi_photos
# Retrieve page with the requests module
response_mars_pics = requests.get(url_Mars_hemi_photos)
# Create BeautifulSoup object; parse with 'html.parser'
soup_mars_pics = BeautifulSoup(response_mars_pics.text, 'html.parser')
# Examine the results, then determine element that contains sought info
print(soup_mars_pics.prettify())


# In[34]:


titles = soup_mars_pics.find_all('h3')
print(titles)


# In[35]:


title_array=[title.get_text() for title in titles]

title_array


# In[36]:


title_array


# In[37]:


list_image_urls=[]
browser.visit(url_Mars_hemi_photos)
for title in title_array:
    browser.click_link_by_partial_text(title)
    hemi_image_link=browser.find_link_by_partial_href('enhanced.tif')
    hemi_image_link_text=hemi_image_link['href']
    list_image_urls.append(hemi_image_link_text)
    browser.back()

list_image_urls


    


# In[38]:


length_loop=len(title_array)
hemisphere_image_urls=[]
for marker in range(length_loop):
    temp_dict={'title': title_array[marker], 'img_url':list_image_urls[marker]}
    hemisphere_image_urls.append(temp_dict)


# In[39]:


hemisphere_image_urls


# In[40]:


links_found = browser.find_link_by_text('Link for Example.com')






    return Mars_data
