import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from fake_useragent import UserAgent

from src.parser.settings import get_driver_options

from src.models import WishPars


def parse_item_info(
        link: str,
        wildberries = None,
        ozon = None,
        aliexpress = None
) -> WishPars:

    if "ozon.ru/" in link:
        title_class = 'm4q_27 tsHeadline550Medium'
        picture_class = ['nk2_27 n2k_27']
        ozon = True
    elif "wildberries.ru/" in link:
        title_class = 'product-page__title'
        picture_class = ['slide__content img-plug']
        wildberries = True
    else:
        title_class = 'snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography-Primary__base__1xop0e snow-ali-kit_Typography__strong__1shggo snow-ali-kit_Typography__sizeHeadingL__1shggo HazeProductDescription_HazeProductDescription__name__1fmsi HazeProductDescription_HazeProductDescription__smallText__1fmsi'
        picture_class = ['gallery_Gallery__picture__crhgwn']
        aliexpress = True

    if not aliexpress:

        driver = webdriver.Chrome(
            options=get_driver_options()
        )

        driver.get(link)
        time.sleep(1)
        driver.refresh()
        if wildberries:
            time.sleep(1)
        html = driver.page_source
        driver.quit()
    else:
        html = requests.get(
            url=link
        ).text

    soup = BeautifulSoup(html, 'lxml')

    try:
        title = f"{soup.find(class_=title_class).text}".strip()
    except AttributeError:
        title = None

    try:
        picture_link = soup.find(class_=picture_class[0]).img["src"]
    except AttributeError:
        picture_link = None

    wish = WishPars(
        name=title,
        picture_src=picture_link
    )

    return wish


if __name__ == '__main__':
    pass
