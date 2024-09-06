from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

def scrape_random_species_text_dynamic(url, save_dir="images"):
    PC_PROFILE_NAME = "Stefanos"
    userdatadir = f'C:/Users/{PC_PROFILE_NAME}/AppData/Local/Google/Chrome/User Data'
    CHROME_PROFILE_NAME = "Stefanos"
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={userdatadir}")
    options.add_argument(f'--profile-directory={CHROME_PROFILE_NAME}')
    driver = webdriver.Chrome(options=options)

    # Load the webpage
    driver.get(url)

    try:
        # Wait for the species text elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='imageGallery']"))
        )

        # Find all image elements
        image_links = driver.find_elements(By.CSS_SELECTOR, "div.imageGallery a[style*='background-image']")

        for image_link in image_links:
            href = image_link.get_attribute('href')  # Get the href attribute (URL)
            species_name = image_link.text  # Get the text inside the link
            print(f"{href} from family: {species_name}")


        # Ensure species are found
        random_image = random.choice(image_links)
        random_url = random_image.get_attribute('href')
        species_name = random_image.text
        print(f"Randomly selected species: {species_name}")

        driver.get(random_url)

        # Wait for the new page to load after the click
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"img:not([src$='.svg'])"))
        )

        # Now find the large image
        img_tag = driver.find_element(By.CSS_SELECTOR, "img")

        # Get the URL of the large image
        img_url = img_tag.get_attribute('src')

        # Handle relative URLs (starting with //)
        if img_url.startswith('//'):
            img_url = 'https:' + img_url

        print(f"Random large image URL: {img_url}")

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
        print(f"Saved species name: {species_name}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser
        driver.quit()


# Example usage
scrape_random_species_text_dynamic("https://www.gbif.org/occurrence/gallery?taxon_key=9394&occurrence_status=present")