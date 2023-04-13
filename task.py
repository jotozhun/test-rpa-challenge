from RPA.Browser.Selenium import Selenium

NYTIMES_URL = "https://www.nytimes.com/"

def minimal_task():
    browser_lib = Selenium()
    browser_lib.open_chrome_browser(NYTIMES_URL, maximized=True)
    browser_lib.set_browser_implicit_wait(value=5.0)
    print("Opened chrome tab")
    news = browser_lib.find_element("xpath:/html/body/div[1]/div[3]/main/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/section[1]/a/div/p").text
    print("New: " + news)
    browser_lib.close_browser()


if __name__ == "__main__":
    minimal_task()
