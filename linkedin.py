from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import parameters
from parsel import Selector

username = parameters.username
password = parameters.password
driver = webdriver.Firefox()
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com/')
sleep(5)

driver.find_element_by_xpath('//a[contains(.,"Iniciar sesión")]').click()
sleep(5)

driver.find_element_by_xpath('//input[@id="username"]').send_keys(username)
sleep(0.5)
driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)
sleep(0.5)
driver.find_element_by_xpath("//button[text()='Iniciar sesión']").click()
sleep(5)

driver.get("https://www.google.com/")
sleep(3)
search_input = driver.find_element_by_name("q")
search_input.send_keys(parameters.google_search)
sleep(1)

search_input.send_keys(Keys.RETURN)
sleep(3)

profiles_links = driver.find_elements_by_xpath("//div[@id='search']//a[1]")
profiles_links = [profile.get_attribute('href') for profile in profiles_links]

for profile in profiles_links:
    driver.get(profile)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//h1/text()').extract_first()
    job_title = sel.xpath('//*[contains(@class,"text-body-medium break-words")]/text()').extract_first().strip()
    experience = sel.xpath('//section[@id="ember66"]//ul/li/div/div//span[1]/text()').extract()

driver.quit()
