import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import numpy as np
import re

BLACK = 5
WHITE = 6
INVALID_WHITE = 7
MUST_WHITE = 8
LIGHT = 9
ILUMI = 10

ILUMMINABLE_BLOCKS = [WHITE, ILUMI, INVALID_WHITE, MUST_WHITE]

def get_meaning(n):
    if n <= 4:
        return str(n)
    if n == ILUMI:
        return 'ilumi'
    if n == WHITE:
        return 'white'
    if n == BLACK:
        return 'black'
    if n == LIGHT:
        return 'light'
    if n == INVALID_WHITE:
        return 'inv_white'
    if n == MUST_WHITE:
        return 'must_white'

def plot_board(board):
    fig, ax = plt.subplots(figsize = (8,8))

    cmap = colors.ListedColormap(['gray', 'black',  'lightgreen',  'darkred', 'lightcoral'])
    bounds=[0, 5, 6, 9, 10, 11]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    im = ax.imshow(board, cmap=cmap, norm=norm)

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            text = ax.text(j, i, get_meaning(board[i, j]),
                        ha="center", va="center", color="w")
    return fig
    


def rolling_window(a, size):
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a. strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def check_new_light(board, x, y):

    board_size = board.shape[0]

    # evita lâmpadas que se iluminam
    temp_row = board[x, :]
    mask = np.ones_like(temp_row).astype(bool)
    for i_block in ILUMMINABLE_BLOCKS:
        mask = mask & (temp_row != i_block) 
    temp_row = temp_row[mask]
    lights_ok_x = not ([LIGHT, LIGHT] == rolling_window(
        temp_row, 2)).all(axis=1).any()

    temp_row = board[:, y]
    mask = np.ones_like(temp_row).astype(bool)
    for i_block in ILUMMINABLE_BLOCKS:
        mask = mask & (temp_row != i_block) 
    temp_row = temp_row[mask]
    lights_ok_y = not ([LIGHT, LIGHT] == rolling_window(
        temp_row, 2)).all(axis=1).any()

    # ilumina as colunas e linhas
    for i in range(1, board_size-x):
        if board[x+i, y] not in ILUMMINABLE_BLOCKS:
            break
        board[x+i, y] = ILUMI

    for i in range(1, x + 1):
        if board[x-i, y] not in ILUMMINABLE_BLOCKS:
            break
        board[x-i, y] = ILUMI

    for i in range(1, board_size-y):
        if board[x, y+i] not in ILUMMINABLE_BLOCKS:
            break
        board[x, y+i] = ILUMI

    for i in range(1, y + 1):
        if board[x, y-i] not in ILUMMINABLE_BLOCKS:
            break
        board[x, y-i] = ILUMI


    # verifica se a nova lâmpada estoura o limite de lâmpadas vizinhas a um bloco preto numerado
    neigh = np.array([[x+1, y], [x-1, y], [x, y+1], [x, y-1]])
    neigh = neigh[((neigh <= board_size - 1) & (neigh >= 0)).all(axis=1)]

    for x, y in neigh:
        if board[x, y] == 0:
            return False
        if board[x, y] <= 4:
            board[x, y] -= 1

    # coloca branco inválido ao redor de blocos 0 (ZERO)
    for x, y in np.argwhere((board == 0)):
        neigh = np.array([[x+1, y], [x-1, y], [x, y+1], [x, y-1]])
        neigh = neigh[((neigh <= board_size - 1) & (neigh >= 0)).all(axis=1)]
        for x2, y2 in neigh:
            if board[x2, y2] == WHITE:
                board[x2, y2] = INVALID_WHITE

    # evita configurações inválidas dada a restrição do nº de lâmpadas ao redor de um block preto numerado
    for x, y in np.argwhere(((board >= 0) & (board <= 4))):
        neigh = np.array([[x+1, y], [x-1, y], [x, y+1], [x, y-1]])
        neigh = neigh[((neigh <= board_size - 1) & (neigh >= 0)).all(axis=1)]
        whites_around_numbers = 0
        for x2, y2 in neigh:
            whites_around_numbers += int((board[x2, y2] == WHITE) | (board[x2, y2] == MUST_WHITE))

        if board[x,y] == whites_around_numbers:
            for x2,y2 in neigh:
                if board[x2,y2] == WHITE:
                    board[x2,y2] = MUST_WHITE

        if board[x, y] > whites_around_numbers:
            return False


    return lights_ok_x and lights_ok_y


def change_whites(board):
    board_size = board.shape[0]

    # coloca branco inválido ao redor de blocos 0 (ZERO)
    for x, y in np.argwhere((board == 0)):
        neigh = np.array([[x+1, y], [x-1, y], [x, y+1], [x, y-1]])
        neigh = neigh[((neigh <= board_size - 1) & (neigh >= 0)).all(axis=1)]
        for x2, y2 in neigh:
            if board[x2, y2] == WHITE:
                board[x2, y2] = INVALID_WHITE

    # evita configurações inválidas dada a restrição do nº de lâmpadas ao redor de um block preto numerado
    for x, y in np.argwhere(((board >= 0) & (board <= 4))):
        neigh = np.array([[x+1, y], [x-1, y], [x, y+1], [x, y-1]])
        neigh = neigh[((neigh <= board_size - 1) & (neigh >= 0)).all(axis=1)]
        whites_around_numbers = 0
        for x2, y2 in neigh:
            whites_around_numbers += int((board[x2, y2] == WHITE) | (board[x2, y2] == MUST_WHITE))

        if board[x,y] == whites_around_numbers:
            for x2,y2 in neigh:
                if board[x2,y2] == WHITE:
                    board[x2,y2] = MUST_WHITE
    return board


def get_random_board(seed15 = None):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    if seed15 is None:
        seed15 = ''.join([str(random.randint(0,9)) for _ in range(15)])
    url = f"https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7b20s4d2#{seed15}"
    # url = "https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#10x10b20s2d1#248925330725324"
    print(url)
    driver.get(url)
    elem = WebDriverWait(driver, 2000).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="permalink-desc"][@href]'))
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
    board = np.array(arr).reshape(7,7).astype(int)

    return board