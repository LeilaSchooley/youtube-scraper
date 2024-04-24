from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

num_videos_to_scrape = 500  # Adjust as needed

def scroll_down_to_load_more(driver):
    # Scroll down the page using the END key
    element = driver.find_element(By.TAG_NAME,"body")
    element.send_keys(Keys.END)
    time.sleep(2)  # Wait for the page to load

def click_element_by_class_and_text(driver, class_name, text):
    xpath = f"//span[@class='{class_name}' and text()='{text}']"
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    # Scroll to the element
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    
    # Click on the element
    element.click()
def slow_type(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def bypass_popup(driver):

    consent_button_xpath = "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"
    consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
        (By.XPATH, consent_button_xpath)))

    consent = driver.find_element(By.XPATH, consent_button_xpath)
    consent.click()
# Function to scrape YouTube videos
def scrape_youtube_videos(search_query, num_videos_to_scrape):


    if os.name == 'posix':  # Unix/Linux/MacOS
        install_dir = "/snap/firefox/current/usr/lib/firefox"
        driver_loc = os.path.join(install_dir, "geckodriver")
        binary_loc = os.path.join(install_dir, "firefox")
        service = FirefoxService(driver_loc)
        opts = webdriver.FirefoxOptions()
        opts.binary_location = binary_loc
        driver = webdriver.Firefox(service=service, options=opts)
    else:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    # Open YouTube
    try:
        driver.get("https://www.youtube.com")

        #click_element_by_class_and_text("yt-core-attributed-string yt-core-attributed-string--white-space-no-wrap", "Accept all")
        bypass_popup(driver)
        time.sleep(5)
        print("Searching")
        # Find the search input field and enter the search query
        # Find the search input field
        search_input = driver.find_element(By.NAME, "search_query")
        
        # Slowly type each word of the search query
        words = search_query.split()
        for word in words:
            slow_type(search_input, word + " ")
        search_input.send_keys(Keys.RETURN)
        print("Done search")
           # Scroll down to load more videos
        while True:
            # Scroll down
            scroll_down_to_load_more(driver)
            
            # Count the number of videos scraped so far
            video_elements = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
            num_videos_scraped = len(video_elements)
            
            # Check if enough videos are scraped
            if num_videos_scraped >= num_videos_to_scrape:
                break
        # Wait for search results to load
        time.sleep(5)
        
        # Find all video titles and links
        video_data = []
        for video_element in video_elements[:num_videos_to_scrape]:
            title = video_element.text
            link = video_element.get_attribute("href")
            video_data.append({"Title": title, "Link": link})

        # Create DataFrame
        df = pd.DataFrame(video_data)

        # Write DataFrame to CSV
        df.to_csv("youtube_videos.csv", index=False)

        driver.quit()

        # Close the WebDriver
        driver.quit()
    except Exception as e:
        print(e)
# Example usage
search_query = "self development"
num_videos_to_scrape = 200  # Adjust as needed
scrape_youtube_videos(search_query, num_videos_to_scrape)