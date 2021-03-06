import string
import sys
import random
import traceback

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


def main(driver: WebDriver = None):
    try:
        if not driver:
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument("-inprivate")

            driver = Edge(executable_path=EDGE_DRIVER_PATH, options=options)
            driver.get(url_encode())

        wait = WebDriverWait(driver, 30, 1)
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
        traceback.print_exc(4, sys.stderr)
    finally:
        driver.delete_all_cookies()
        driver.refresh()
        main(driver)

    driver.quit()


def step():
    no: int = 0

    def run(driver: WebDriver):
        nonlocal no
        if not no:
            elem = driver.find_element(By.XPATH, "//a[text()='投票']")
            if not elem:
                elem = driver.find_element(By.XPATH, "//a[text()='今日已投票']")
                if elem:
                    driver.delete_all_cookies()
                    driver.refresh()
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


            driver.add_cookie({
                "name": "uuid",
                "value":  generate_uuid(),
                "domain": ".businessweekly.com.tw",
                "size": 40,
            })
            elem = None
            try:
                elem = driver.find_element(By.XPATH, r"//a[text()='確認送出']")
                if elem and elem.is_enabled():
                    elem.click()
            except Exception as e:
                if driver.find_element_by_id("gdrp-el"):
                    driver.execute_script("""document.getElementById("gdrp-el").remove();""")
            finally:
                elem_container = driver.find_element_by_class_name("modal__container")
                if elem_container and elem_container.find_element(By.XPATH, "//img[@alt='投票完成']"):
                    no += 1
                    return True
                if "投票完成" in driver.page_source:
                    no += 1
                    return True

        return None

    return run


def url_encode():
    if not REQUEST_PARAMS:
        return BASE_URL
    else:
        params_url = "&".join(["{}={}".format(k, v) for k, v in REQUEST_PARAMS.items() if v])
        return "{}?{}".format(BASE_URL, params_url)


def generate_ip():
    rand = random.randint(0, len(IP_RANGE))
    begin, end = IP_RANGE[rand]
    a, b = begin.split("."), end.split(".")
    ip = [a[i] if a[i] == b[i] else str(random.randint(int(a[i]), int(b[i]))) for i in range(0, len(a))]
    return ".".join(ip)


def generate_uuid(prefix: str = None):
    """
    uid_arr = "".join(random.sample((string.digits + string.ascii_lowercase[:6]) * 2, 32))
    uuid = "{}-{}-{}-{}-{}".format(uid_arr[:9], uid_arr[9: 9 + 4], uid_arr[9 + 4: 9 + 4 * 2], uid_arr[9 + 4 * 2:9 + 4 * 3], uid_arr[9 + 4 * 3:])
    """
    "54f59d20-2a13-11eb-abcc-71ed92458739"
    if not prefix:
        prefix = "f4063380-28b9-11eb-9f0b-"
    elif not prefix.endswith("-"):
        prefix += "-"

    return prefix + "".join(random.sample(string.digits + string.ascii_lowercase[:6], 12))


IP_RANGE = [("1.32.202.0", "1.32.202.127"), ("1.32.203.0", "1.32.203.127"), ("1.32.204.0", "1.32.204.127"), ("1.34.0.0", "1.35.255.255"), ("1.160.0.0", "1.174.206.255"), ("5.253.85.0", "5.253.85.255"), ("8.39.126.0", "8.39.126.255"), ("13.33.189.0", "13.33.189.255"), ("13.35.11.0", "13.35.11.255"), ("13.35.24.0", "13.35.26.255"), ("17.253.116.0", "17.253.117.255"), ("23.48.148.0", "23.48.149.255"), ("23.61.204.0", "23.61.204.255"), ("23.61.246.0", "23.61.246.255"), ("23.73.24.0", "23.73.25.255"), ("23.199.34.0", "23.199.34.255"), ("23.205.113.0", "23.205.114.255"), ("23.205.172.0", "23.205.173.255"), ("23.210.215.0", "23.210.215.255"), ("23.212.60.0", "23.212.60.255"), ("23.248.176.0", "23.248.177.255"), ("27.51.0.0", "27.53.255.255"), ("27.100.19.0", "27.100.19.255"), ("27.123.40.0", "27.123.41.255"), ("27.123.51.0", "27.123.51.255"), ("27.123.55.0", "27.123.55.255"), ("27.123.194.0", "27.123.195.255"), ("27.124.13.0", "27.124.14.255"), ("27.240.0.0", "27.247.255.255"), ("31.13.87.0", "31.13.87.255"), ("34.80.0.0", "34.81.255.255"), ("35.203.226.0", "35.203.227.255"), ("36.255.96.0", "36.255.96.255"), ("37.252.243.0", "37.252.243.255"), ("39.8.0.0", "39.15.255.255"), ("42.99.167.0", "42.99.167.255"), ("42.99.216.0", "42.99.217.255"), ("43.231.189.0", "43.231.189.255"), ("43.246.131.0", "43.246.131.255"), ("43.249.212.0", "43.249.214.255"), ("43.251.68.0", "43.251.70.255"), ("43.254.197.0", "43.254.198.255"), ("45.10.214.0", "45.10.214.255"), ("45.43.55.0", "45.43.55.255"), ("45.43.59.0", "45.43.59.255"), ("45.43.61.0", "45.43.61.255"), ("45.65.45.0", "45.65.45.255"), ("45.116.168.0", "45.116.169.255"), ("45.116.177.0", "45.116.177.255"), ("45.120.201.0", "45.120.201.255"), ("45.121.180.0", "45.121.180.255"), ("45.126.86.1", "45.126.86.255"), ("45.126.148.0", "45.126.149.255"), ("45.129.77.0", "45.129.78.255"), ("45.158.181.0", "45.158.181.255"), ("45.254.255.0", "45.254.255.255"), ("46.8.118.0", "46.8.119.255"), ("47.89.64.0", "47.89.64.255"), ("47.246.36.0", "47.246.38.255"), ("49.158.0.0", "49.159.255.255"), ("49.213.128.0", "49.219.255.255"), ("52.46.57.0", "52.46.57.255"), ("52.46.62.0", "52.46.62.255"), ("52.84.248.0", "52.84.250.255"), ("52.124.196.0", "52.124.196.255"), ("52.124.240.0", "52.124.240.255"), ("52.124.243.0", "52.124.243.255"), ("54.239.176.0", "54.239.177.255"), ("54.239.179.0", "54.239.179.255"), ("58.114.0.0", "58.115.255.255"), ("59.104.0.0", "59.105.255.255"), ("59.152.45.0", "59.152.45.255"), ("59.152.47.96", "59.152.47.255"), ("60.198.0.0", "60.199.255.255"), ("60.248.0.0", "60.251.255.255"), ("61.4.126.0", "61.4.126.255"), ("61.8.34.16", "61.8.34.255"), ("61.8.45.0", "61.8.46.255"), ("61.14.150.0", "61.14.151.255"), ("61.14.164.0", "61.14.165.255"), ("61.14.172.0", "61.14.172.255"), ("61.14.176.0", "61.14.176.143"), ("61.14.179.0", "61.14.179.127"), ("61.14.180.0", "61.14.180.127"), ("61.14.188.0", "61.14.188.191"), ("61.14.189.240", "61.14.190.127"), ("61.14.191.48", "61.14.191.159"), ("61.30.0.0", "61.31.255.255"), ("61.56.0.0", "61.67.255.255"), ("61.70.0.0", "61.71.255.255"), ("63.217.71.0", "63.217.71.255"), ("63.218.17.0", "63.218.17.255"), ("63.218.79.0", "63.218.79.255"), ("63.218.244.0", "63.218.244.255"), ("63.218.247.0", "63.218.247.255"), ("63.222.12.0", "63.222.12.255"), ("63.222.40.0", "63.222.40.255"), ("66.159.198.0", "66.159.198.255"), ("66.171.112.0", "66.171.113.255"), ("66.171.116.0", "66.171.117.255"), ("70.132.27.0", "70.132.27.255"), ("71.152.15.0", "71.152.15.255"), ("74.125.41.0", "74.125.41.255"), ("77.67.84.0", "77.67.84.255"), ("93.90.73.0", "93.90.73.255"), ("94.190.152.0", "94.190.152.255"), ("94.190.154.0", "94.190.155.255"), ("101.8.0.0", "101.15.255.255"), ("101.101.101.0", "101.101.101.255"), ("101.102.103.0", "101.102.103.255"), ("101.136.0.0", "101.139.255.255"), ("102.165.40.0", "102.165.42.255"), ("103.4.105.255", "103.4.107.255"), ("103.11.36.0", "103.11.37.255"), ("103.17.95.0", "103.17.95.255"), ("103.27.181.0", "103.27.181.255"), ("103.28.200.0", "103.28.201.255"), ("103.35.204.0", "103.35.204.239"), ("103.35.205.0", "103.35.206.255"), ("103.38.146.0", "103.38.147.255"), ("103.47.26.0", "103.47.26.255"), ("103.49.133.0", "103.49.134.255"), ("103.67.227.0", "103.67.227.255"), ("103.68.138.0", "103.68.138.255"), ("103.69.204.0", "103.69.205.255"), ("103.74.201.0", "103.74.203.255"), ("103.81.128.0", "103.81.128.255"), ("103.81.185.0", "103.81.185.255"), ("103.89.21.0", "103.89.23.255"), ("103.96.120.1", "103.96.120.254"), ("103.96.121.1", "103.96.121.254"), ("103.96.122.1", "103.96.122.254"), ("103.96.123.1", "103.96.123.254"), ("103.98.16.0", "103.98.17.255"), ("103.99.228.0", "103.99.228.255"), ("103.105.134.0", "103.105.134.255"), ("103.114.133.0", "103.114.133.255"), ("103.114.135.0", "103.114.135.255"), ("103.117.106.0", "103.117.106.255"), ("103.126.189.0", "103.126.189.255"), ("103.126.191.0", "103.126.191.255"), ("103.136.60.0", "103.136.61.255"), ("103.136.224.0", "103.136.225.255"), ("103.136.250.0", "103.136.250.255"), ("103.137.22.0", "103.137.23.255"), ("103.137.98.0", "103.137.99.255"), ("103.137.166.0", "103.137.167.255"), ("103.137.188.0", "103.137.189.255"), ("103.137.246.0", "103.137.247.255"), ("103.138.92.0", "103.138.93.255"), ("103.138.106.0", "103.138.107.255"), ("103.138.194.0", "103.138.195.255"), ("103.138.254.0", "103.138.255.255"), ("103.139.64.0", "103.139.65.255"), ("103.139.92.0", "103.139.93.255"), ("103.139.96.0", "103.139.97.255"), ("103.139.126.0", "103.139.127.255"), ("103.139.240.0", "103.139.241.255"), ("103.140.110.0", "103.140.111.255"), ("103.140.169.0", "103.140.169.255"), ("103.140.232.0", "103.140.233.255"), ("103.141.76.0", "103.141.76.255"), ("103.142.176.0", "103.142.177.255"), ("103.143.56.0", "103.143.57.255"), ("103.143.86.0", "103.143.86.255"), ("103.144.248.0", "103.144.249.255"), ("103.145.22.0", "103.145.23.255"), ("103.145.114.0", "103.145.114.255"), ("103.146.80.0", "103.146.81.255"), ("103.146.164.0", "103.146.165.255"), ("103.146.250.0", "103.146.251.255"), ("103.147.22.0", "103.147.23.255"), ("103.147.58.0", "103.147.59.255"), ("103.147.130.0", "103.147.131.255"), ("103.148.68.0", "103.148.69.255"), ("103.148.72.0", "103.148.73.255"), ("103.148.130.0", "103.148.131.255"), ("103.148.142.0", "103.148.143.255"), ("103.148.146.0", "103.148.147.255"), ("103.150.36.0", "103.150.37.255"), ("103.150.230.0", "103.150.231.255"), ("103.151.176.1", "103.151.176.250"), ("103.152.150.0", "103.152.151.255"), ("103.152.202.0", "103.152.203.255"), ("103.152.220.0", "103.152.221.255"), ("103.152.252.0", "103.152.253.255"), ("103.153.176.0", "103.153.177.255"), ("103.153.200.0", "103.153.201.255"), ("103.155.132.0", "103.155.132.255"), ("103.155.202.0", "103.155.203.255"), ("103.156.116.0", "103.156.117.255"), ("103.156.148.0", "103.156.149.255"), ("103.156.184.0", "103.156.185.255"), ("103.156.242.0", "103.156.243.255"), ("103.157.42.0", "103.157.43.255"), ("103.157.62.0", "103.157.63.255"), ("103.157.86.0", "103.157.87.255"), ("103.157.111.0", "103.157.111.255"), ("103.196.206.0", "103.196.206.255"), ("103.199.148.0", "103.199.148.255"), ("103.205.72.0", "103.205.72.255"), ("103.205.74.0", "103.205.75.255"), ("103.205.156.0", "103.205.158.63"), ("103.206.120.0", "103.206.120.255"), ("103.208.84.0", "103.208.84.255"), ("103.208.196.0", "103.208.197.255"), ("103.214.70.0", "103.214.70.255"), ("103.229.16.0", "103.229.17.255"), ("103.229.50.0", "103.229.50.255"), ("103.229.226.0", "103.229.227.255"), ("103.236.103.0", "103.236.103.255"), ("103.241.114.0", "103.241.116.255"), ("103.241.236.0", "103.241.236.255"), ("103.241.239.0", "103.241.239.255"), ("103.243.20.0", "103.243.21.255"), ("103.243.23.0", "103.243.23.255"), ("103.246.218.0", "103.246.219.255"), ("103.248.133.0", "103.248.133.255"), ("103.248.151.0", "103.248.151.255"), ("103.249.162.0", "103.249.163.255"), ("103.252.244.0", "103.252.244.255"), ("103.253.56.0", "103.253.56.255"), ("103.253.59.0", "103.253.59.255"), ("104.76.192.0", "104.76.192.255"), ("104.77.93.0", "104.77.95.255"), ("104.116.243.0", "104.116.243.255"), ("104.132.150.0", "104.132.150.255"), ("104.132.193.0", "104.132.194.255"), ("104.132.213.0", "104.132.213.255"), ("104.132.239.0", "104.132.239.255"), ("104.133.15.0", "104.133.15.255"), ("104.133.17.0", "104.133.18.255"), ("106.64.0.0", "106.65.255.255"), ("106.104.0.0", "106.107.255.255"), ("107.150.114.0", "107.150.114.255"), ("107.154.94.0", "107.154.94.255"), ("107.155.57.0", "107.155.58.255"), ("110.24.0.0", "110.31.255.255"), ("111.70.0.0", "111.71.255.255"), ("111.80.0.0", "111.83.255.255"), ("111.184.0.0", "111.185.255.255"), ("112.104.0.0", "112.105.255.255"), ("113.20.144.0", "113.20.145.255"), ("113.212.78.0", "113.212.79.255"), ("114.24.0.0", "114.27.255.255"), ("114.136.0.0", "114.137.255.255"), ("115.80.0.0", "115.83.255.255"), ("115.178.0.0", "115.178.1.255"), ("116.0.68.0", "116.0.69.7"), ("116.206.72.0", "116.206.72.255"), ("116.251.252.0", "116.251.252.255"), ("117.104.191.0", "117.104.191.255"), ("118.99.12.0", "118.99.12.255"), ("118.107.177.0", "118.107.179.255"), ("118.160.0.0", "118.171.255.255"), ("118.193.62.0", "118.193.63.255"), ("118.231.0.0", "118.233.255.255"), ("122.116.0.0", "122.118.255.255"), ("122.120.0.0", "122.127.255.255"), ("122.146.0.0", "122.147.255.255"), ("122.152.179.128", "122.152.179.255"), ("122.248.184.192", "122.248.185.127"), ("123.192.0.0", "123.195.255.255"), ("123.204.0.0", "123.205.150.255"), ("123.240.0.0", "123.241.255.255"), ("123.253.140.0", "123.253.141.255"), ("124.6.34.0", "124.6.34.255"), ("124.8.0.0", "124.12.255.255"), ("124.108.102.0", "124.108.103.255"), ("124.108.111.0", "124.108.114.119"), ("124.108.114.126", "124.108.115.231"), ("124.109.4.0", "124.109.5.31"), ("125.224.0.0", "125.233.255.255"), ("125.252.69.0", "125.252.69.255"), ("125.252.74.64", "125.252.74.191"), ("125.252.76.0", "125.252.77.255"), ("125.252.82.0", "125.252.82.255"), ("125.252.96.64", "125.252.96.175"), ("128.1.32.0", "128.1.32.255"), ("128.1.37.0", "128.1.37.255"), ("128.1.45.0", "128.1.45.255"), ("128.1.50.0", "128.1.50.255"), ("128.1.64.0", "128.1.64.255"), ("128.1.101.0", "128.1.102.255"), ("128.1.155.0", "128.1.155.255"), ("128.1.221.0", "128.1.222.255"), ("128.1.225.0", "128.1.225.255"), ("128.14.226.0", "128.14.227.255"), ("128.14.229.0", "128.14.230.255"), ("128.90.72.0", "128.90.74.255"), ("128.90.111.0", "128.90.111.255"), ("128.90.118.0", "128.90.118.255"), ("134.159.90.0", "134.159.91.255"), ("134.159.101.0", "134.159.101.255"), ("134.159.103.0", "134.159.103.255"), ("134.159.109.128", "134.159.109.255"), ("134.159.123.16", "134.159.123.255"), ("134.159.133.0", "134.159.133.127"), ("134.159.170.0", "134.159.170.255"), ("134.159.194.0", "134.159.195.255"), ("140.82.193.0", "140.82.193.255"), ("141.226.118.0", "141.226.119.255"), ("150.116.0.0", "150.117.255.255"), ("152.101.5.0", "152.101.5.255"), ("152.101.25.0", "152.101.27.255"), ("152.101.32.0", "152.101.32.255"), ("152.101.50.0", "152.101.50.255"), ("152.101.174.0", "152.101.174.255"), ("154.195.6.0", "154.195.7.255"), ("154.201.5.0", "154.201.5.255"), ("154.211.31.0", "154.211.31.255"), ("154.214.255.0", "154.214.255.255"), ("154.218.29.0", "154.218.29.255"), ("156.253.6.0", "156.253.7.255"), ("157.167.38.0", "157.167.38.255"), ("159.100.205.0", "159.100.205.255"), ("160.32.243.0", "160.32.243.255"), ("162.222.165.0", "162.222.165.255"), ("165.84.236.0", "165.84.236.255"), ("165.204.134.0", "165.204.135.255"), ("165.225.102.0", "165.225.102.255"), ("168.149.155.0", "168.149.155.255"), ("172.217.42.0", "172.217.42.255"), ("173.194.93.0", "173.194.93.255"), ("173.194.171.0", "173.194.171.255"), ("173.223.206.0", "173.223.206.255"), ("175.96.0.0", "175.99.255.255"), ("175.180.0.0", "175.183.255.255"), ("180.87.70.9", "180.87.70.255"), ("180.87.76.10", "180.87.77.20"), ("180.176.0.0", "180.177.255.255"), ("180.204.0.0", "180.207.255.255"), ("180.217.0.0", "180.218.255.255"), ("182.233.0.0", "182.235.255.255"), ("183.177.72.0", "183.177.72.255"), ("183.177.94.0", "183.177.95.255"), ("184.26.170.0", "184.26.171.255"), ("184.28.66.0", "184.28.67.255"), ("184.29.38.0", "184.29.38.255"), ("184.29.40.0", "184.29.41.255"), ("184.51.152.0", "184.51.152.255"), ("185.132.78.0", "185.132.78.255"), ("185.202.102.0", "185.202.102.255"), ("185.215.215.0", "185.215.215.255"), ("185.228.185.0", "185.228.185.255"), ("185.253.156.0", "185.253.156.255"), ("188.172.208.0", "188.172.208.255"), ("188.214.106.0", "188.214.106.255"), ("191.96.237.0", "191.96.237.255"), ("192.188.171.0", "192.188.171.255"), ("192.230.120.0", "192.230.120.255"), ("192.253.254.128", "192.253.254.255"), ("193.22.156.0", "193.22.156.255"), ("193.36.119.0", "193.36.119.255"), ("193.239.179.0", "193.239.179.255"), ("193.243.150.0", "193.243.151.255"), ("194.5.52.0", "194.5.52.255"), ("194.127.177.0", "194.127.177.255"), ("194.127.181.0", "194.127.181.255"), ("194.127.183.0", "194.127.183.255"), ("194.127.194.0", "194.127.194.255"), ("194.156.14.0", "194.156.14.255"), ("195.80.148.0", "195.80.148.255"), ("196.52.117.0", "196.52.117.255"), ("196.52.166.0", "196.52.167.255"), ("196.53.232.0", "196.53.232.255"), ("196.53.234.0", "196.53.234.255"), ("196.54.131.0", "196.54.131.255"), ("202.5.4.0", "202.5.5.255"), ("202.6.104.0", "202.6.105.255"), ("202.8.14.0", "202.8.15.255"), ("202.41.146.0", "202.41.146.255"), ("202.47.205.0", "202.47.206.255"), ("202.55.224.48", "202.55.227.15"), ("202.55.227.32", "202.55.228.207"), ("202.55.228.224", "202.55.229.95"), ("202.55.238.72", "202.55.240.127"), ("202.59.250.0", "202.59.251.255"), ("202.66.207.0", "202.66.207.255"), ("202.74.127.16", "202.74.127.255"), ("202.76.86.0", "202.76.86.255"), ("202.80.14.0", "202.80.15.255"), ("202.88.20.0", "202.88.21.255"), ("202.88.27.0", "202.88.27.255"), ("202.89.121.0", "202.89.123.255"), ("202.133.248.192", "202.133.249.127"), ("202.133.249.192", "202.133.250.255"), ("202.135.131.0", "202.135.131.255"), ("202.153.4.0", "202.153.5.255"), ("202.153.160.0", "202.153.162.223"), ("202.153.163.0", "202.153.164.95"), ("202.153.170.128", "202.153.173.63"), ("202.153.173.96", "202.153.176.255"), ("202.153.184.232", "202.153.187.127"), ("202.153.187.192", "202.153.189.175"), ("202.153.190.0", "202.153.191.167"), ("202.153.191.176", "202.153.192.255"), ("202.153.193.112", "202.153.194.191"), ("202.153.194.224", "202.153.198.159"), ("202.153.198.176", "202.153.199.111"), ("202.153.199.128", "202.153.202.79"), ("202.153.202.96", "202.153.202.255"), ("202.153.203.96", "202.153.204.47"), ("202.153.204.56", "202.153.204.215"), ("202.153.204.224", "202.153.205.239"), ("202.153.206.96", "202.153.207.255"), ("202.162.97.0", "202.162.97.255"), ("202.167.58.0", "202.167.58.255"), ("202.167.75.0", "202.167.75.255"), ("202.167.99.0", "202.167.99.255"), ("202.167.160.0", "202.167.160.255"), ("202.174.4.0", "202.174.4.255"), ("202.192.242.0", "202.192.242.255"), ("203.14.212.0", "203.14.212.255"), ("203.55.118.0", "203.55.118.255"), ("203.64.0.0", "203.75.255.255"), ("203.80.169.0", "203.80.169.255"), ("203.83.216.0", "203.83.217.255"), ("203.92.208.0", "203.92.208.255"), ("203.99.254.0", "203.99.254.255"), ("203.102.19.0", "203.102.19.255"), ("203.119.3.0", "203.119.3.255"), ("203.119.94.0", "203.119.94.255"), ("203.148.92.0", "203.148.92.255"), ("203.163.72.0", "203.163.72.255"), ("203.163.90.0", "203.163.90.127"), ("203.167.15.0", "203.167.15.255"), ("203.192.143.0", "203.192.143.255"), ("203.192.170.0", "203.192.170.255"), ("203.194.85.128", "203.194.85.255"), ("203.203.0.0", "203.204.255.255"), ("204.79.62.0", "204.79.63.255"), ("205.248.48.0", "205.248.48.255"), ("205.248.68.0", "205.248.69.255"), ("206.49.92.0", "206.49.92.255"), ("206.73.198.128", "206.73.198.255"), ("206.182.30.0", "206.182.30.255"), ("207.209.3.0", "207.209.3.255"), ("207.209.218.0", "207.209.218.255"), ("207.226.238.0", "207.226.238.255"), ("208.127.158.1", "208.127.159.254"), ("209.28.29.0", "209.28.29.255"), ("209.120.214.0", "209.120.215.255"), ("209.120.248.0", "209.120.248.255"), ("210.16.107.0", "210.16.107.255"), ("210.57.25.0", "210.57.25.255"), ("210.58.0.0", "210.71.255.255"), ("210.80.64.0", "210.80.67.95"), ("210.176.44.0", "210.176.45.255"), ("210.176.136.0", "210.176.137.255"), ("210.176.154.88", "210.176.154.223"), ("210.176.154.232", "210.176.155.255"), ("210.200.0.0", "210.203.127.255"), ("210.240.0.0", "210.244.255.255"), ("211.20.0.0", "211.23.255.255"), ("211.72.0.0", "211.79.255.255"), ("212.22.248.0", "212.22.250.255"), ("213.166.100.0", "213.166.100.255"), ("218.34.0.0", "218.35.255.255"), ("218.210.0.0", "218.211.255.255"), ("219.68.0.0", "219.71.255.255"), ("219.80.0.0", "219.81.255.255"), ("219.84.0.0", "219.87.255.255"), ("219.90.58.64", "219.90.61.127"), ("219.90.61.160", "219.90.63.255"), ("220.228.0.0", "220.229.255.255"), ("222.156.0.0", "222.157.255.255"), ("223.22.0.0", "223.23.255.255"), ("223.136.0.0", "223.143.255.255")]


if __name__ == '__main__':
    print(generate_uuid())
