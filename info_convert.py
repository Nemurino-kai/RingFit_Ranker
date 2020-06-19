import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import re
import datetime
import numpy as np

from PIL import Image
import sys
import pyocr.builders
import image_processing

THRESHOLD = 0.95
TEMPLATE = cv2.imread('template.jpg')


class ExerciseData:
    def __init__(self, time, cal, user_name):
        self.exercise_time = time
        self.exercise_cal = cal
        self.user_name = user_name


def read_cal_by_tesseract(image):
    image = image_processing.skew_image(image)

    # 大津の二値化をしておく
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(im_gray, 0, 255, cv2.THRESH_OTSU)

    image = Image.fromarray(image)

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[0]
    print("Will use lang '%s'" % (langs))

    txt = tool.image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    print(txt)

    # よくある誤字を修正
    retext = txt.replace(' ', '').replace('i', '1').replace(']', '1').replace('t', '1') \
        .replace('?', '2').replace('O', '0').replace('A', '4').replace('l', '1').replace('I', '1') \
        .replace('Q', '9').replace('g', '9').replace('/', '7')

    # 数字以外はすべて取り除き、intにする
    try:
        retext = int(re.sub('[^0-9]', '', retext))
    except ValueError as e:
        print("this is empty!")
        retext = 0

    # kcalが4桁はあり得ないのでエラー
    try:
        if (retext > 999):
            raise ValueError("Cal is too large!")
    except ValueError as e:
        print(e)
        retext = int(re.sub('[^0-9]', '', txt))

    if str(retext) != txt: print("Text is replaced.")
    return int(retext)


def is_result_image():
    fetch_image = cv2.imread('temp.jpg')

    # fetch_imageのsizeが公式のものでなければout
    h, w, _ = fetch_image.shape
    if h != 720 or w != 1280:
        return False

    result = cv2.matchTemplate(fetch_image, TEMPLATE, cv2.TM_CCOEFF_NORMED)
    # 検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if max_val > THRESHOLD:
        return True
    else:
        return False


def image_to_data(user_name):
    fetch_image = cv2.imread('temp.jpg')

    # 各部分の画像を切り出す
    total_time = fetch_image[257:257 + 84, 552:552 + 404]
    total_cal = fetch_image[396:396 + 65, 586:586 + 228]
    total_distance = fetch_image[493:493 + 76, 560:560 + 396]

    # time = read_time(total_time)
    # dummyData
    time = datetime.time(second=0)
    cal = read_cal_by_tesseract(total_cal)
    return ExerciseData(time, cal, user_name)


def convert_datalist_to_timelist(exercise_data_list):
    return [e.exercise_time.hour + (e.exercise_time.minute / 60.0) + (e.exercise_time.second / 3600.0) for e in
            exercise_data_list]


def convert_datatuple_to_callist(exercise_data_list):
    return [e[0] for e in exercise_data_list]


def datalist_to_histogram(exercise_list, ranking):
    plt.figure()
    n, bins, patches = plt.hist(exercise_list, color='darkturquoise', ec='black', bins=30)
    print(n, bins)
    print(exercise_list[ranking])
    print("xは", np.where(exercise_list[ranking] >= bins)[0][-1])
    x = np.where(exercise_list[ranking] >= bins)[0][-1]
    if x == 30: x = x - 1
    patches[x].set_facecolor('tomato')
    # y軸を整数にする
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig('hist.png')  # ヒストグラムを保存
    plt.close()


if __name__ == '__main__':
    import sqlite3
    import config

    # ヒストグラムのテスト
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("select kcal from Exercise "
                "WHERE date(time_stamp) == date('now', '+9 hours') and kcal < 150 ORDER BY kcal DESC ;")
    exercise_data_list = cur.fetchall()
    print(exercise_data_list)
    # num_list = convert_datatuple_to_callist(exercise_data_list)

    num_list = [0, 10, 10, 10, 10.1, 30, 30, 30, 30.2, 40, 50, 70, 90, 200]
    time_ranking = 10
    plt.figure()
    n, bins, patches = plt.hist(num_list, color='darkturquoise', ec='black', bins=30)
    print(n, bins)
    print(np.where(num_list[time_ranking] >= bins)[0])

    print(np.where(num_list[time_ranking] >= bins)[0][-1])
    x = np.where(num_list[time_ranking] >= bins)[0][-1]
    if x == 20: x = 19
    patches[x].set_facecolor('tomato')
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig('hist.png')
    plt.show()

    fetch_image = cv2.imread('images/badsmall.jpg')

    # 各部分の画像を切り出す
    total_cal = fetch_image[396:396 + 65, 586:586 + 228]

    # time = read_time(total_time)
    # dummyData
    time = datetime.time(second=0)
    cal = read_cal_by_tesseract(total_cal)
