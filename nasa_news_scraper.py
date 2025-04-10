# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# import time

# driver = webdriver.Chrome()
# url = 'https://www.nasa.gov/news/recently-published/'

# driver.get(url)

# time.sleep(3)

# articles = driver.find_elements(By.CLASS_NAME, 'hds-content-item-inner')


# def extract_data(articles):
#     for article in articles:
#         print(article.text)
#         link_element = article.find_element(By.CSS_SELECTOR, 'a')
#         url = link_element.get_attribute('href')
#         print(url)
#         break




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.nasa.gov/news/recently-published/")

time.sleep(3)

# page_number_spans = driver.find_elements(By.CLASS_NAME, "page-numbers")

# for page in page_number_spans[1:]:
#     print(page.text)  # Zum Überprüfen des Textes jedes span-Elements
#     page.click()  # Klicken, um weitere Inhalte zu laden
#     time.sleep(3)  # Warten auf das Nachladen der Inhalte





# spans = driver.find_elements(By.XPATH, "//a[contains(@class, 'page-numbers')]")


# for span in spans:
#     print(span)
#     print(span.text)
#     span.click()  # Klicken, um weitere Inhalte zu laden
#     time.sleep(3)  # Warten auf das Nachladen der Inhalte



spans = driver.find_elements(By.XPATH, "//nav[contains(@class, 'hds-pagination')]//a")

# spans = driver.find_elements(By.XPATH, "//a[contains(@class, 'next')]")

print(spans[0].text)  # Zum Überprüfen des Textes jedes span-Elements
spans[0].click()  # Klicken, um weitere Inhalte zu laden
time.sleep(3)  # Warten auf das Nachladen der Inhalte