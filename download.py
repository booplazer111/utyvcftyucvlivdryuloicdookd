from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = "https://sites.google.com/view/classroom6x"
driver.get(url)

# Wait for the page to load
time.sleep(3)

# Find the sidebar toggle button and click it to open the sidebar
sidebar_toggle_button = driver.find_element(By.CLASS_NAME, 'DXsoRd')  # Class for the sidebar toggle button
sidebar_toggle_button.click()

# Wait for the sidebar to open
time.sleep(3)

# Find all list items in the sidebar containing the links
links = driver.find_elements(By.XPATH, "//li//a[@href]")

# Open a file in write mode to save the links
with open('links.txt', 'w') as file:
    # Write each link to the file
    for link in links:
        file.write(link.get_attribute('href') + '\n')

# Close the WebDriver
driver.quit()

print("Links have been saved to links.txt.")
