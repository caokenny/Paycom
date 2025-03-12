from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
import time
import datetime
import os
import warnings

# Configuration
warnings.filterwarnings("ignore")

'''
    FILL THIS IN WITH YOUR PAYCOM LOG IN CREDENTIALS
'''
username = ""
password = ""
userpin = ""

login_url = "https://www.paycomonline.net/v4/ee/web.php/app/login"
punches_url = [
    'https://www.paycomonline.net/v4/ee/web.php/timeclock/WEB04/punch/in-day',
    'https://www.paycomonline.net/v4/ee/web.php/timeclock/WEB04/punch/out-lunch',
    'https://www.paycomonline.net/v4/ee/web.php/timeclock/WEB04/punch/in-lunch',
    'https://www.paycomonline.net/v4/ee/web.php/timeclock/WEB04/punch/out-day'
]
# 12:00 Out Lunch, 1:00 In Lunch
clock_times_seconds = [32400, 43200, 46800, 64800]
clock_times_string = ['9:00', '12:00', '1:00', '6:00']
punch_label = ['In Day', 'Out Lunch', 'In Lunch', 'Out Day']

# 12:30 Out Lunch, 1:30 In Lunch
# clock_times_seconds = [32400, 45000, 48600, 64800]
# clock_times_string = ['9:00', '12:30', '1:30', '6:00']

# Set to True to log in initially with 2FA.
login2FA = False


def initialize_driver():
    options = Options()
    '''
        COMMENT THIS LINE TO LOG IN INITIALLY WITH 2FA.
    '''
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("log-level=1")
    options.add_argument("silent")
    home_dir = os.path.expandvars("%USERPROFILE%")
    options.add_argument(f"user-data-dir={home_dir}\\AppData\\Local\\Google\\Chrome")
    options.add_argument("profile-directory=Selenium")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service("chromedriver-win64\\chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)

def login(driver):
    driver.find_element(By.ID, "txtlogin").send_keys(username)
    driver.find_element(By.ID, "txtpass").send_keys(password)
    driver.find_element(By.ID, "userpinid").send_keys(userpin)
    driver.find_element(By.ID, "btnSubmit").click()
    time.sleep(5)

def clock_in_out(driver, punch_index):
    while not driver.find_element(By.ID, 'clock').text.startswith(clock_times_string[punch_index]):
        time.sleep(30) # Check every 30 seconds
    
    print(f'[{driver.find_element(By.ID, "clock").text}] {punch_label[punch_index]}')
    driver.get(punches_url[punch_index])
    time.sleep(2)

def calculate_time_sleep():
    time_now = datetime.datetime.now().strftime('%H:%M:%S')
    time_split = time_now.split(':')
    time_seconds = (int(time_split[0]) * 60 * 60) + (int(time_split[1]) * 60) + int(time_split[2])

    index = 0
    while index < 4 and clock_times_seconds[index] - time_seconds < 0:
        index += 1

    if index == 4:
        print('All punches completed, exiting.')
        exit(0)

    time_until_punch = clock_times_seconds[index] - time_seconds
    time_until_punch -= 60

    return (0, index) if time_until_punch < 0 else (time_until_punch, index)


def main():
    while True:
        if not login2FA:
            punch_info = calculate_time_sleep()
            print(f'Time until next punch: {str(datetime.timedelta(seconds=punch_info[0]))[:-3]}')
            time.sleep(punch_info[0])
        driver = initialize_driver()
        print('Driver initialized')
        driver.get(login_url)
        login(driver)
        if login2FA:
            time.sleep(60)
            driver.quit()
            break
        else:
            try:
                driver.find_element(By.ID, 'clock')
                print('Login successful')
            except:
                print('Login failed, exiting.')
                driver.quit()
                exit(1)
            clock_in_out(driver, punch_info[1])
            time.sleep(30)

            driver.quit()

            if punch_info[1] == 3:
                print('All punches completed, exiting.')
                break

if __name__ == '__main__':
    main()