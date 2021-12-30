from selenium import webdriver
import pandas as pd
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

start_index = 153

# read csv file with song links
df = pd.read_csv("Scrape/youtube/2_round/youtube.csv")

# run firefox without head
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument('--disable-application-cache')
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

# start firefox
print("----starting firefox----")
driver = webdriver.Firefox(options=options)
print("----firefox started----")


# iterate through each video id and extract the viewcount
try:
	for counter, id in enumerate(df.video_id):
		if counter >= start_index:
			print(counter, end=" ")
			print(id, end=" ")

			try:
				driver.get("https://www.youtube.com/watch?v={}".format(id))
				element = WebDriverWait(driver, 30).until(
					EC.presence_of_element_located((By.CLASS_NAME, "view-count.style-scope.ytd-video-view-count-renderer")))
				
				view = element.text
				print(view)
				view = view.split()[0]

				with open("Scrape/youtube/2_round/view.tsv", "a") as f:
					f.write("{}\t{}\n".format(id, view))
			except Exception as e:
				print("----Failed----")
				with open("Scrape/youtube/2_round/view_failed", 'a') as f:
					f.write("failed at {}\nError:\n{}\n".format(id, e))
			
			# time.sleep(2)

finally:
	driver.quit()
