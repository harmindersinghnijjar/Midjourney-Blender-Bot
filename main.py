# Description: An open-source Python program to automate generating images using the Midjourney bot on Discord. 
# Author: harmindesinghnijjar
# Edit by: SandalBandit
# Date: 2023-05-26
# Version: 1.0.0
# Usage: python main.py

# Import modules.
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import getpass
import os
import time

CHANNEL_URL = ""
COMMAND = "/blend"

# def get_channel_url():
#     """Gets the channel URL from user input."""
#     channel_url = input("Enter the discord channel URL: ")
#     return channel_url

# def get_command():
#     # Gets the command from the user input.
#     command = input("Enter the command: ")
#     return command

# Set username.
user = getpass.getuser()


class Selenium:
    def __init__(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # Add a user data directory as an argument for options.
        options.add_argument(f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument("profile-directory=Default")
        # In order to prevent the "Timed out receiving message from renderer: 20.000" error, add the following options.
        options.add_experimental_option('extensionLoadTimeout', 60000)
        # Instantiate Google Chrome with the above options.
        chrome_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=options)

    def open_channel(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Error occurred: {e}")

    def bot_command(self, command):
        try:
            chat_bar = self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div').click()
        except NoSuchElementException:
            print("Could not find chat bar on the page.")
            return
        except Exception as e:
            print("An error occurred while clicking the chat bar:", e)
            return

        time.sleep(5)

        try:
            chat_bar = self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div')
            chat_bar.send_keys(command)
        except Exception as e:
            print(f"An error, {e}, occurred while entering {command} into the chat bar.")

        try:
            prompt_div = self.driver.find_element(By.XPATH, '//*[@id="autocomplete-0"]/div')
            prompt_div.click()
        except Exception as e:
            print(f"An error, {e}, occurred while clicking on prompt option.")

        # TODO
        try:
            pillValue = self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]')
            url1 = "https://cdn.midjourney.com/b2397cc7-f57e-4642-8bc8-8d15ece93f75/0_3.png"  # Replace this URL with your image URL
            url2 = "https://cdn.midjourney.com/485b7324-6b67-49dd-9269-522592cf2cd1/0_0.png"  # Replace this URL with your image URL
            pillValue.send_keys(url1, url2)
            time.sleep(10)
            pillValue.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"An error, {e}, occurred while filling in image URL.")

        time.sleep(60)

        try:
            last_image = self.driver.find_elements(By.CLASS_NAME, 'originalLink-Azwuo9')[-1]
            time.sleep(5)
            src = last_image.get_attribute('href')
            print(src)
            url = src

            r = requests.get(url, stream=True)
            with open(f'img_{+1}.png', 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            del r

        except Exception as e:
            print(f"An error, {e}, occurred while downloading the image.")

    def close_browser(self):
        self.driver.quit()

    def setup(self):
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(20)


if __name__ == '__main__':
    os_command = 'taskkill /im chrome.exe /f'
    os.system(os_command)

    selenium_client = Selenium()

    while True:
        selenium_client.open_channel(CHANNEL_URL)
        time.sleep(5)
        selenium_client.bot_command(COMMAND)
        time.sleep(5)

        selenium_client.close_browser()
