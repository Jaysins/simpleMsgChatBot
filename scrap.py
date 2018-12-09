from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.support.ui import WebDriverWait

chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chromeOptions)


def index():
	driver.get('https://genesiscinemas.com/')

	source = driver.page_source

	soup = BeautifulSoup(source, 'lxml')

	images = []
	titles = []
	info = []

	movies = soup.findAll("div", {'class': ["iheu-data", "iheu-img"]})

	for movie in movies:
		if movie.img:		
			images.append(movie.img['src'])
		else:
			titles.append(movie.h3.text.strip())
			info.append(movie.p.text.strip())
	return images, info, titles

