from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import parameters
from parsel import Selector
import csv

writer = csv.writer(open(parameters.output_file, 'w'))
writer.writerow(['name', 'job_title', 'location', 'linkedin_url'])

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
    if 'translate.google.com' in profile:
        continue
    driver.get(profile)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//h1/text()').extract_first()
    job_title = sel.xpath('//*[contains(@class,"text-body-medium break-words")]/text()').extract_first()
    if job_title:
        job_title = job_title.strip()
    # about = sel.xpath("//section[contains(@class,'artdeco-card ember-view break-words pb3')][1]//span[2]/text()").extract()[1]
    location = sel.xpath("//span[@class='text-body-small inline t-black--light break-words']//text()").extract_first()
    if location:
        location = location.strip()
    linkedin_url = driver.current_url
    # experiences = sel.xpath("//section[contains(@class,'artdeco-card ember-view break-words pb3')][4]//div[@class='pvs-list__outer-container']").extract()

    print('\n')
    print(name)
    print(job_title)
    print(location)
    print(linkedin_url)
    print('\n')

    writer.writerow([name, job_title, location, linkedin_url])

driver.quit()
