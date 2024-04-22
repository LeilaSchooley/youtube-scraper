from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

# Function to scrape YouTube videos
def scrape_youtube_videos(search_query):
    if os.name == 'posix':  # Unix/Linux/MacOS
        install_dir = "/snap/firefox/current/usr/lib/firefox"
        driver_loc = os.path.join(install_dir, "geckodriver")
        binary_loc = os.path.join(install_dir, "firefox")
        service = FirefoxService(driver_loc)
        opts = webdriver.FirefoxOptions()
        opts.binary_location = binary_loc
        driver = webdriver.Firefox(service=service, options=opts)
    elif os.name == 'nt':  # Windows
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise OSError("Unsupported operating system")  
    # Open YouTube
    try:
        driver.get("https://www.youtube.com")
        
        # Find the search input field and enter the search query
        search_input = driver.find_element(By.NAME, "search_query")
        search_input.send_keys(search_query)
        search_input.send_keys(Keys.RETURN)
        
        # Wait for search results to load
        time.sleep(5)
        
        # Find all video titles and links
        video_titles = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
        
        # Iterate over the videos and print their titles and links
        for video_title in video_titles:
            print("Title:", video_title.text)
            print("Link:", video_title.get_attribute("href"))
            print()
        
        # Close the WebDriver
        driver.quit()
    except Exception as e:
        print(e)
# Example usage
search_query = "your search query here"
scrape_youtube_videos(search_query)
