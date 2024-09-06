from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

def scrape_random_species_text_dynamic(url_queue, species_queue, save_dir="images"):

    # Set up browser
    PC_PROFILE_NAME = "Stefanos"
    userdatadir = f'C:/Users/{PC_PROFILE_NAME}/AppData/Local/Google/Chrome/User Data'
    CHROME_PROFILE_NAME = "Stefanos"
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={userdatadir}")
    options.add_argument(f'--profile-directory={CHROME_PROFILE_NAME}')


    driver = webdriver.Chrome(options=options)

    while True:
        # Wait for url
        url = url_queue.get()

        try:
            species_name = ""

            # Load the webpage
            driver.get(url)

            retry_attempts = 10  # Set number of retries for random selection
            for attempt in range(retry_attempts):
                try:
                    # Wait for the species text elements to be present
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_elements(By.CSS_SELECTOR, "div[class*='imageGallery']") or 
                                    d.find_element(By.XPATH, "//h3[contains(text(), 'No occurrences with images')]")
                    )

                    # Check if "No occurrences with images" text is found
                    no_images_text = driver.find_elements(By.XPATH, "//h3[contains(text(), 'No occurrences with images')]")
                    if no_images_text:
                        print("No occurrences with images found. Restarting process...")
                        species_queue.put("")  # Notify the main process that no images were found
                        break  # Break the inner retry loop and return to waiting for a new URL

                    # Find all image elements
                    image_links = driver.find_elements(By.CSS_SELECTOR, "div.imageGallery a[style*='background-image']")

                    # Select a random image
                    random_image = random.choice(image_links)
                    random_url = random_image.get_attribute('href')
                    species_name = random_image.text
                    print(f"Randomly selected species: {species_name}")

                    # Navigate to the selected URL
                    driver.get(random_url)
                    break  # If successful, exit the retry loop

                except Exception as e:
                    print(f"Attempt {attempt + 1}/{retry_attempts} failed: {e}")
                    if attempt == retry_attempts - 1:
                        raise  # Re-raise error if max retries reached
                    time.sleep(0.5)  # Wait before retrying

            # If the loop was broken because of "No occurrences with images" or no image links, restart the process
            if not species_name:
                continue  # Restart the while True loop and wait for a new URL

            # In case we somehow miss images
            retry_attempts = 3
            for attempt in range(retry_attempts):
                try:
                    # Wait for an image that isn't a .svg icon
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img:not([src$='.svg'])"))
                    )
                    break  # If successful, exit loop
                except Exception as e:
                    print(f"Retry attempt {attempt + 1}/{retry_attempts} failed: {e}")
                    if attempt == retry_attempts - 1:
                        raise  # Re-raise error if max attempts reached
                    time.sleep(0.5)  # Wait before retrying

            # Now find the large image
            img_tag = driver.find_element(By.CSS_SELECTOR, "img")

            # Get the URL of the large image
            img_url = img_tag.get_attribute('src')

            # Handle relative URLs (starting with //)
            if img_url.startswith('//'):
                img_url = 'https:' + img_url

            # Create the directory if it doesn't exist
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Get the image file name
            img_name = os.path.join(save_dir, species_name + ".png")

            # Download and save the larger image
            img_data = requests.get(img_url).content
            with open(img_name, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded larger image: {img_name}")
            species_queue.put(species_name)
            print("Put the species name in the queue")
            driver.quit()
            break

        except Exception as e:
            print(f"Scraper failed: {e}")
            species_queue.put("")
            continue  # Restart process after failure