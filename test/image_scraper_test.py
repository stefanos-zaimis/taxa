from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import os
import time

def scrape_first_thumbnail_image_dynamic(url, save_dir="images"):
    PC_PROFILE_NAME = "Stefanos"
    userdatadir = f'C:/Users/{PC_PROFILE_NAME}/AppData/Local/Google/Chrome/User Data'
    CHROME_PROFILE_NAME = "Stefanos"
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={userdatadir}")
    options.add_argument(f'--profile-directory={CHROME_PROFILE_NAME}')
    driver = webdriver.Chrome(options=options)

    # Load the webpage
    driver.get(url)

    # Wait for the page to load
    driver.implicitly_wait(5)

    try:
        # Find the first <a> tag with the background image (thumbnail) and click it
        a_tag = driver.find_element(By.CSS_SELECTOR, "a[style*='background-image']")
        a_tag.click()

        # Give some time for the new page to load after the click
        time.sleep(5)

        # Now that the new page is loaded, find the large image element
        img_tag = driver.find_element(By.CSS_SELECTOR, "img")

        # Get the URL of the larger image
        img_url = img_tag.get_attribute('src')

        # Handle relative URLs (starting with //) by adding https:
        if img_url.startswith('//'):
            img_url = 'https:' + img_url

        print(f"Larger image URL found: {img_url}")

        # Create the directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Get the image file name
        img_name = os.path.join(save_dir, img_url.split('/')[-1].split('.')[0] + ".png")

        # Download and save the larger image
        img_data = requests.get(img_url).content
        with open(img_name, 'wb') as f:
            f.write(img_data)
        print(f"Downloaded larger image: {img_name}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser
        driver.quit()


# Example usage
scrape_first_thumbnail_image_dynamic("https://www.gbif.org/occurrence/gallery?taxon_key=1712343")
