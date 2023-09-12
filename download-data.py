import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def login_and_save_cookies(driver, username, password):
    driver.get("https://accounts.google.com/ServiceLogin")

    driver.find_element(By.ID, "identifierId").send_keys(username)

    driver.find_element(By.ID, "identifierNext").click()

    time.sleep(3)  # Wait for next page to load

    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.ID, "passwordNext").click()

    time.sleep(3)  # Wait for next page to load

    # Save cookies to file
    with open("cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver):
    # Load cookies from file
    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def download_csv_with_selenium(year, position, folder_path):
    base_url = f"https://www.fantasypros.com/nfl/stats/{position}.php?year={year}"

    # Configure the options for headless download
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    userdatadir = '/Users/anishdevineni/Desktop/projects/fantasy-football-wizard/C:/Users/anishdevineni/AppData/Local/Google/Chrome/User Data'
    options.add_argument(f"--user-data-dir={userdatadir}")
    options.add_experimental_option("prefs", {"download.default_directory": folder_path, 
                                              "download.prompt_for_download": True,
                                              "download.directory_upgrade": True,
                                              "safebrowsing_for_trusted_sources_enabled": False,
                                              "safebrowsing.enabled": False})

    # Initialize the WebDriver with the options and the correct path to the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Send a GET request to the URL
    driver.get(base_url)

    # Find the download link element using its aria-label attribute
    print(driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Download data"]'))
    driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Download data"]').click()

    print("Downloading")

    # Wait for a short time to ensure the download is complete
    time.sleep(10)

    print("Finished")

    # Close the WebDriver
    driver.quit()

def main():
    # Years and positions for which you want to download the CSV files
    years = [2021]  # Add more years if needed
    positions = ['qb', 'rb', 'wr', 'te']  # Add more positions if needed

    # Specify the folder path where you want to save the CSV files
    folder_path = '/Users/anishdevineni/Desktop/projects/fantasy-football-wizard/data'

    for year in years:
        for position in positions:
            download_csv_with_selenium(year, position, folder_path)

    print("All Finished!")

if __name__ == "__main__":
    main()
