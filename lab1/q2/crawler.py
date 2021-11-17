from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import re
import numpy as np

from utils import BLACK, WHITE


def get_random_board(seed15=None, url = None):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=options)

    if seed15 is None:
        seed15 = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    if url is None:
        url = f"https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7b20s4d2#{seed15}"
    # url = "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#10x10b20s2d1#248925330725324"
    

    print(url)
    driver.get(url)
    elem = WebDriverWait(driver, 2000).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="permalink-desc"][@href]'))
    )

    # elem = driver.find_element_by_id("permalink-desc")
    board_desc = elem.get_attribute("href").split(":")[-1]

    arr = []
    for t in board_desc:
        if re.match(r"[a-z]", t):
            arr.extend((ord(t) - ord('a') + 1) * [WHITE])
        else:
            if t == 'B':
                arr.append(BLACK)
            else:
                arr.append(t)

    shape = re.findall(r"#(\d+)x(\d+)", url)
    print(shape)
    board = np.array(arr).reshape(int(shape[0][0]), int(shape[0][1])).astype(int)

    return board
