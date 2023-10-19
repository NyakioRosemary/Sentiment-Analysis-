import selenium
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


# Specify the path to the ChromeDriver executable
chrome_driver_path = 'C:\Program Files (x86)\chromedriver-win64\chromedriver.exe'

# Create a Service object
service = Service(chrome_driver_path)

# Initialize the WebDriver using the Service object
driver = webdriver.Chrome(service=service)

# get the page
driver.get('https://www.imdb.com/')

# max the window
driver.maximize_window()

# movie 1 keywords
driver.find_element(By.ID, "suggestion-search").send_keys("The Last of Us TV Series 2023")
driver.find_element(By.ID, "suggestion-search-button").click()
# 2023 last of us movie
driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t").click()
# click to review list comments
driver.find_element(By.XPATH, '//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-274f2729-0 fWkbWT baseAlt"]').click()

# review_date latest
dropdown = driver.find_element(By.CLASS_NAME, 'lister-sort-by')
# working with the select clas
l_ist = Select(dropdown)
l_ist.select_by_visible_text('Review Date')
while True:
    try:
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='load-more-trigger']"))))
        driver.find_element(By.XPATH, "//button[@id='load-more-trigger']").click()
        print("Navigating to Next Page")
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        break
# preview ot list and column structure
# rating
rates_star = driver.find_elements(By.XPATH, "//span[contains(@class,'rating-other-user-rating')]")
# title
titles = driver.find_elements(By.XPATH, '//a[contains(@class,"title")]')
# user name
user_name = driver.find_elements(By.XPATH, "//span[contains(@class,'display-name-link')]")
# date
date_comment = driver.find_elements(By.XPATH, "//span[contains(@class,'review-date')]")

# helpful average comments that were helpful
who_found_comment_helpful = driver.find_elements(By.XPATH, "//div[contains(@class,'actions text-muted')]")
# comment
comments = driver.find_elements(By.XPATH, "//div[contains(@class,'text show-more__control')]")

with open('imd_m_web.csv', 'w', newline='', encoding='utf-8') as file:
    # the header of the file
    file.write("rates_star;titles;user_name;date_comment;who_found_comment_helpful;comments;\n")

    # append and open the columns with ranges
with open('imd_m_web.csv', 'a', newline='', encoding='utf-8') as file:
    for i in range(len(rates_star)):
        # clean the comments text making sure its in 1 column "they were long and had breaks "
        comments_text = comments[i].text.replace('"', '""')  # escape the double quotes
        titles_text = titles[i].text.replace('"', '""')  # escape this incase in the future we have long text

        # write the data inside the columns using a format style
        file.write(
            f'"{rates_star[i].text}";"{titles_text}";"{user_name[i].text}";"{date_comment[i].text}";"{who_found_comment_helpful[i].text}";"{comments_text}"\n'
        )
