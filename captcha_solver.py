import time
from selenium import webdriver
import warnings
import keyboard
import random
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore", category=DeprecationWarning)
from selenium.webdriver.common.by import By
import io
import os
from PIL import Image

" Please give url and xpath of captcha image as parameter to solve function of this class "


class CaptchaCracker:
    def __init__(self):
        self.start_time = time.time()
        self.driver = self.__get_driver()
        self.attempts = 1

    @staticmethod
    def __get_driver(incognito=False, port_rotate=False):
        chrome_options = webdriver.ChromeOptions()

        if port_rotate is True:
            port_no = random.randint(8081, 9999)
        else:
            port_no = 8080
        if incognito is True:
            chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            chrome_options=chrome_options, port=port_no)
        return driver

    def __google_lens(self):
        driver = self.__get_driver(incognito=True, port_rotate=True)
        sleep_time = 1.25
        driver.get('https://images.google.com/')
        try:
            accpt = driver.find_element(By.XPATH, '//*[@id="L2AGLb"]/div')
            driver.execute_script('arguments[0].click()', accpt)
        except Exception:
            pass
        time.sleep(sleep_time)
        lens = driver.find_element(By.XPATH, '//div[@class="nDcEnd"]')
        driver.execute_script('arguments[0].click();', lens)
        time.sleep(sleep_time)

        # Upload button
        driver.find_element(By.XPATH, '//span[@class="DV7the"]').click()
        time.sleep(sleep_time)
        keyboard.write(
            os.path.join(os.getcwd() + "\captcha_ss.png"))
        keyboard.press_and_release('return')
        time.sleep(2)

        # Text button
        driver.find_element(By.XPATH, '//*[@id="ucj-4"]/span[1]').click()
        time.sleep(1)
        try:
            driver.find_element(By.XPATH,
                                '//*[@id="yDmH0d"]/div[3]/c-wiz/div/c-wiz/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/button/span').click()
            answer = ''.join(driver.find_element(By.XPATH,
                                                 '//*[@id="yDmH0d"]/div[3]/c-wiz/div/c-wiz/div/div[2]/div/div/span/div/div[2]').get_attribute(
                'innerHTML').replace('"', '').split())
            return answer
        except Exception:
            driver.quit()
            return None

    def solve(self, url, captcha_xpath):
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(5)

        # captcha screenshot and save
        captcha_elem = self.driver.find_element(By.XPATH, captcha_xpath)

        # Scroll to that element
        self.driver.execute_script("arguments[0].scrollIntoView();", captcha_elem)
        time.sleep(0.25)
        screenshot = captcha_elem.screenshot_as_png
        imageStream = io.BytesIO(screenshot)
        image = Image.open(imageStream)
        image.save('captcha_ss.png')
        answer = self.__google_lens()

        # Your code (Data Extraction etc.) starts here

        " You can add your logic here to take the result from Google lens and try it in the webpage until a condition satisfies" \
        " I am doing it this way just as an example "

        if answer is not None:
            print(f"Captcha Answer from Google Lens ----> {answer}")
            user_answer = input("Please enter you answer (Y/N) ----> ")
            if user_answer == 'Y':
                print("Google lens gave correct answer. Quit Program.")
                total_time = round(time.time() - self.start_time, 2)
                print(f"Attempts made ---> {self.attempts}")
                print(f"Total Time Taken ---> {total_time}")
                self.driver.quit()
            else:
                print('Google Lens did not give correct answer, Retrying')
                self.attempts += 1
                self.solve(url, captcha_xpath)

        else:
            print('Google Lens could not get answer, Retrying')
            self.attempts += 1

            self.solve(url, captcha_xpath)


# Read Test Url Excel file
df = pd.read_excel("urls_testing.xlsx")

# Use the attached Excel sheet for testing
for url in df['URL (Text captcha)']:
    print("URL ---->", url)
    captcha_xpath = input("Please enter captcha xpath and press Enter ----> ")
    if captcha_xpath == 'Pass':
        continue
    crack = CaptchaCracker()
    crack.solve(
        url=url,
        captcha_xpath=captcha_xpath
    )
