from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.youtube.com/c/MakeDataUseful/videos")
for _ in range(2):
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(4)
html = driver.page_source
soup = bs(html, 'html.parser')
vedios = soup.find_all("div", {'id': 'dismissible'})
master_list = []
for vedio in vedios:
    data_dict = {}
    data_dict["title"] = vedio.find('a', {'id': 'video-title'}).text
    meta = vedio.find('div', {'id': "metadata-line"}).find_all('span')
    views = meta[0].text
    date = meta[1].text
    link = "https://www.youtube.com/" + vedio.find('a', {'id': 'thumbnail'})["href"]
    data_dict["link"] = link
    driver.get(link)
    time.sleep(5)
    html = driver.page_source
    soup2 = bs(html, 'html.parser')
    try:
        str_date = soup2.find('div', {"id": "date"}).text.replace("•", "")
        str_date = str_date.replace(",", "")
        date_date = datetime.datetime.strptime(str_date, '%b %d %Y')
        str_date = date_date.strftime('%d %b %Y')
    except:
        str_date = date
    try:
        a_views = soup2.find(
            'span', {'class': "view-count style-scope ytd-video-view-count-renderer"}).text
    except:
        a_views = views
    likesanddislikes = soup2.find_all("a", class_="yt-simple-endpoint style-scope ytd-toggle-button-renderer")
    try:
        data_dict["Likes"] = likesanddislikes[0].text
        data_dict["Dislikes"] = likesanddislikes[1].text
    except:
        pass
    data_dict["Total Views"] = a_views
    data_dict["views"] = views
    data_dict["date"] = str_date
    master_list.append(data_dict)
yt_df = pd.DataFrame(master_list)
yt_df.to_csv("YouTube_Scrape.csv")
