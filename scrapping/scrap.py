import csv #This package lets us save data to a csv file
from selenium import webdriver #The Selenium package we'll need
from selenium.webdriver.common.keys import Keys
import time #This package lets us pause execution for a bit

path_to_file = "./reviews.csv"

pages_to_scrape = 3

url = "https://www.tripadvisor.com/Attraction_Review-g297698-d939620-Reviews-Nusa_Dua_Beach-Nusa_Dua_Nusa_Dua_Peninsula_Bali.html"

# import the webdriver
driver = webdriver.Chrome('./chromedriver.exe')
driver.get(url)

# open the file to save the review
csvFile = open(path_to_file, 'a', encoding="utf-8")
csvWriter = csv.writer(csvFile)

# change the value inside the range to save the number of reviews we're going to grab
for i in range(0, pages_to_scrape):

    # give the DOM time to load
    time.sleep(2) 

    # Click the "expand review" link to reveal the entire review.
    driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

    # Now we'll ask Selenium to look for elements in the page and save them to a variable. First lets define a  container that will hold all the reviews on the page. In a moment we'll parse these and save them:
    container = driver.find_elements_by_xpath("//div[@data-reviewid]")

    # Next we'll grab the date of the review:
    dates = driver.find_elements_by_xpath(".//div[@class='_2fxQ4TOx']")
    
   # Now we'll look at the reviews in the container and parse them out

    for j in range(len(container)): # A loop defined by the number of reviews

        # Grab the rating
        rating = container[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
        # Grab the title
        title = container[j].find_element_by_xpath(".//div[contains(@data-test-target, 'review-title')]").text
        #Grab the review
        review = container[j].find_element_by_xpath(".//q[@class='NejBf']").text.replace("\n", "  ")
        #Grab the data
        date = " ".join(dates[j].text.split(" ")[-2:])
        
        #Save that data in the csv and then continue to process the next review
        csvWriter.writerow([date, rating, title, review]) 
        
    # When all the reviews in the container have been processed, change the page and repeat            
    driver.find_element_by_xpath('.//a[@class="ui_button nav next primary "]').click()

# When all pages have been processed, quit the driver
driver.quit()