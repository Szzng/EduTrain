from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_selenium_bws(url):
    # 크롬창 열지 않고 백그라운드에서 실행하는 옵션
    options = Options()
    options.headless = True
    # user agent 따로 지정하지 않으면 headless chrome 이라고 뜸
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                         "like Gecko) Chrome/95.0.4638.54 Safari/537.36")
    service = Service("/Users/sz/webproject/education/Extra/chromedriver")
    bws = webdriver.Chrome(service=service, options=options)
    bws.maximize_window()
    bws.get(url)
    return bws