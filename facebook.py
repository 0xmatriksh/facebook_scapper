# import imp
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(options=options)
driver.get('https://www.facebook.com/')

name_list = []
content_list = []
image_list = []
time_list = []

driver.maximize_window()

email = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'email']")))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'pass']")))

email.send_keys("YOUR_FACEBOOK_LOGIN_EMAIL")  # login email
password.send_keys("YOUR_PASSWORD HERE")  # login password

WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "button[type = 'submit']"))).click()

sleep(3)

# give your group id here
driver.get('https://www.facebook.com/groups/YOUR_GROUP_ID/posts')
sleep(5)

# code to scrape posts in from group with scrolling down
prev_length = 0
while True:

    soup = BeautifulSoup(driver.page_source, "html.parser")
    all_posts = soup.find_all(
        "div", {"class": "du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"})
    i = 0
    # logic to discard the previous added posts in the lists of name,content,image and time
    posts = all_posts[prev_length:]

    for post in posts:
        i = i + 1
        try:
            name = (post.find("a", {"class": "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p"})).get_text()
        except:
            name = 'not found'

        try:
            content = (post.find("span", {
                "class": "d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id hzawbc8m"})).get_text()
        except:
            content = 'not found'

        try:
            image = (post.find("a", {
                "class": "oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql btwxx1t3 abiwlrkh p8dawk7l lzcic4wl a8c37x1j tm8avpzi"}))['href']
        except:
            image = 'no image'

        try:
            time = (post.find("a", {
                    "class": "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"})).find('span').get_text()
        except:
            time = 'no image'

        name_list.append(name)  # add this post's name
        content_list.append(content)  # add this post's content
        image_list.append(image)  # add this post's image link
        time_list.append(time)  # add this post's time

        prev_length = i
        sleep(2)

        # to break the loop if we get 10 posts [ NUMBER 10 HERE IS THE NUMBER OF POSTS TO SCRAPE YOU CAN CHANGE ]
        if(len(name_list) > 10):
            break

    # scroll the page down to parse more posts from the page
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    # [ NUMBER 10 HERE IS THE NUMBER OF POSTS TO SCRAPE YOU CAN CHANGE ]
    if(len(name_list) > 10):
        break

df = pd.DataFrame({'name': name_list, "content": content_list,
                   "image": image_list, "time": time_list})
df.to_csv('facebook.csv')  # save as csv file in this same directory
