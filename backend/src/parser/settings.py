from selenium import webdriver
from fake_useragent import UserAgent


def get_driver_options():

    options = webdriver.ChromeOptions()

    useragent = UserAgent()
    while True:
        user_agent = useragent.random
        if "Windows" in user_agent:
            options.add_argument(f"user-agent={user_agent}")
            break

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")

    return options


if __name__ == '__main__':
    pass
