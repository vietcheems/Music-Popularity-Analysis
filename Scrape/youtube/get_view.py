import requests
import bs4
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# r = requests.get("https://www.youtube.com/watch?v=kJQP7kiw5Fk")


# binary = FirefoxBinary("/home/viet/OneDrive/Studying Materials/Introduction to Data Science/EDA Project/geckodriver-v0.30.0-linux64/geckodriver")
# browser = webdriver.Firefox(firefox_binary=binary)


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--ignore-ssl-errors=yes')
# chrome_options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome("/home/viet/OneDrive/Studying Materials/Introduction to Data Science/EDA Project/chromedriver_linux64/chromedriver", options=chrome_options)
browser = webdriver.Firefox()
print("firefox started")
start = time.time()
browser.get("http://www.python.org")
# driver.get("https://www.youtube.com/watch?v=kJQP7kiw5Fk")
print(time.time() - start)
