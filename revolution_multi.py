from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
from datetime import datetime
from dotenv import dotenv_values
import time
import multiprocessing

# sudo service cron start

secrets = dotenv_values(".env")

start = datetime.now()
date_string = start.strftime("%Y%m%d")

# Create and configure logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[
                        logging.FileHandler(
                            "logs/revolution_" + date_string + ".log"),
                        logging.StreamHandler()
                    ]
                    )

# Creating an object
logger = logging.getLogger()


def get_session_token(user, pw):
    try:
        # create a new Chrome driver instance
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)

        # navigate to webpage and login
        driver.get('https://www.revolution.com.sg/reserve/#/account')
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))

        username_textbox = driver.find_element(By.NAME, 'username')
        username_textbox.send_keys(user)
        password_textbox = driver.find_element(By.NAME, 'password')
        password_textbox.send_keys(pw)
        driver.find_element(By.CLASS_NAME, 'btn').click()

        url = driver.current_url
        l = url.split('/')
        for i in range(len(l)-1, -1, -1):
            if l[i] == "st":
                session_token = l[i+1]
                break
        driver.quit()
        return session_token
    except Exception as e:
        logger.info("Exception: " + str(e))
        get_session_token()


def book_class(session_token, seat_id):
    import subprocess

    # curl command to get the content of a webpage
    for i in seat_id:
        # curl command to get the redirected URL
        curl_command = f"curl -L -w %{{url_effective}} -o /dev/null  https://rhythmstudios.zingfit.com/reserve/index.cfm?action=Reserve.book&classid={class_id}&spotid={i}&st={session_token}&site=3"

        # call the curl command using subprocess
        output = subprocess.check_output(curl_command.split())

        # extract the redirected URL from the output
        redirected_url = output.decode('utf-8').strip()

        # print the redirected URL
        logger.info(redirected_url)
        if 'booksuccess' in redirected_url:
            break


def main(user, pw, seat_id):
    session_token = get_session_token(user, pw)
    book_class(session_token, seat_id)


if __name__ == "__main__":
    logger.info(f"---Starting program---")
    time.sleep(50)
    # Set Inputs
    class_id = '1933915777803487227'
    hw_seat_id = range(1, 57, 2)
    iv_seat_id = range(2, 57, 2)

    # Create two processes, one for each program
    p1 = multiprocessing.Process(target=main, args=(
        secrets['hw_user'], secrets['hw_pw'], hw_seat_id))
    p2 = multiprocessing.Process(target=main, args=(
        secrets['iv_user'], secrets['iv_pw'], iv_seat_id))

    # Start both processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()

    logger.info(f"---Both programs finished---")
