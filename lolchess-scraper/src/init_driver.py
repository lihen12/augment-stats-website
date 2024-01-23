from selenium import webdriver

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = webdriver.chrome.service.Service('C:\\Program Files\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

if __name__ == "__main__":
    driver = init_driver()
    print("WebDriver initialized successfully.")
