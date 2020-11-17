import string
import sys
import random

import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://health.businessweekly.com.tw/event/2020/thoracic/search.html"
REQUEST_PARAMS = {
    "doctor": "ada380f9-bc2c-4912-8745-6a84da2b5bfd"
}

EDGE_DRIVER_PATH = r"F:\Administrator\Downloads\edgedriver_win32\msedgedriver.exe"


def main():
    try:
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("-inprivate")

        driver = Edge(executable_path=EDGE_DRIVER_PATH, options=options)
        driver.get(url_encode())

        wait = WebDriverWait(driver, 60)
        # elem_vote = driver.find_element(By.XPATH, "//a[text()='投票']")
        # elem_vote = wait.until(EC.presence_of_element_located((By.XPATH, r"//a[text()='投票']")))
        # elem_vote.click()
        callback = step()
        elem = wait.until(callback)

        # elem_vote_options = wait.until(get_elem_vote_options)
        # elem_vote_options = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div/div/label[@class='label']")))
        # elem_vote_options = elem_vote.find_elements(By.XPATH, "//div/div/label[@class='label']")
        elem = wait.until(callback)

        # map(lambda e: e.click(), elem_vote_options)
        # elem_vote_btn = wait.until(EC.element_to_be_clickable((By.XPATH, r"//a[text()='確認送出']")))
        # 1elem_vote_btn = driver.find_element(By.XPATH, r"//a[text()='確認送出']")
        # elem_vote_btn.click()
        elem = wait.until(callback)
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        driver.quit()


def step():
    no: int = 0

    def run(driver: WebDriver):
        nonlocal no
        if not no:
            elem = driver.find_element(By.XPATH, "//a[text()='投票']")
            if not elem:
                return None
            elem.click()
            elem_container = driver.find_element_by_class_name("modal__container")
            if elem_container.is_displayed():
                no += 1
                return elem_container
        elif no == 1:
            elem_vote_options = driver.find_elements(By.XPATH, "//div/div/label[@class='label']")
            if not elem_vote_options:
                return None

            for elem in elem_vote_options:
                if not elem.is_displayed():
                    break
                elem.click()
                for_input = driver.find_element_by_id(elem.get_attribute("for"))
                if not for_input.is_selected():
                    break
            else:
                no += 1
                return elem_vote_options
        if no == 2:
            """
            uid_arr = "".join(random.sample((string.digits + string.ascii_lowercase[:6]) * 2, 32))
            uuid = "{}-{}-{}-{}-{}".format(uid_arr[:9], uid_arr[9: 9 + 4], uid_arr[9 + 4: 9 + 4 * 2], uid_arr[9 + 4 * 2:9 + 4 * 3], uid_arr[9 + 4 * 3:])
            """
            uuid = "f4063380-28b9-11eb-9f0b-" + "".join(random.sample(string.digits + string.ascii_lowercase[:6], 12))
            driver.add_cookie({
                "name": "uuid",
                "value":  uuid,  # "f4063380-28b9-11eb-9f0b-2b79135cf9a3",
                "domain": ".businessweekly.com.tw",
                "size": 40,
            })
            elem = driver.find_element(By.XPATH, r"//a[text()='確認送出']")
            if elem and elem.is_enabled():
                try:
                    elem.click()
                except Exception as e:
                    if driver.find_element_by_id("gdrp-el"):
                        driver.execute_script("""document.getElementById("gdrp-el").remove();""")

                    return None

                if "投票完成" in driver.page_source:
                    no += 1
                    return elem
        return None

    return run


def url_encode():
    if not REQUEST_PARAMS:
        return BASE_URL
    else:
        params_url = "&".join(["{}={}".format(k, v) for k, v in REQUEST_PARAMS.items() if v])
        return "{}?{}".format(BASE_URL, params_url)


if __name__ == '__main__':
    main()
