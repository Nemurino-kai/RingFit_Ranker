from enum import Enum,auto,unique
import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import LinearSegmentedColormap

import datetime
import numpy as np


THRESHOLD = 0.95
TEMPLATE = cv2.imread('templates/running.jpg')
TEMPLATE2 = cv2.imread('templates/time.jpg')
HISTGRAM_BINS =30

class ExerciseData:
    def __init__(self, time, cal,distance):
        self.time = time
        self.cal = cal
        self.distance = distance

@unique
class ImageType(Enum):
    EXERCISE_IMAGE = auto()
    CUSTOM_EXERCISE_IMAGE = auto()

def generate_cmap(colors):
    """自分で定義したカラーマップを返す"""
    values = range(len(colors))

    vmax = np.ceil(np.max(values))
    color_list = []
    for v, c in zip(values, colors):
        color_list.append( ( v/ vmax, c) )
    return LinearSegmentedColormap.from_list('custom_cmap', color_list)

def read_cal_by_connectedComponets(image):
    # 大津の二値化
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(im_gray, 0, 255, cv2.THRESH_OTSU)

    # 白黒反転
    img_reverse = cv2.bitwise_not(image)
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_reverse)

    stats = stats[np.argsort(stats[:, 0])] # x座標でソート
    kcal_str =""

    if (nlabels > 4 or nlabels <= 1):
        raise ValueError(f"ConnectedComponets > 4 or ConnectedComponets <= 1. nlabels is {nlabels}.")

    for i in range(1, nlabels):
        cut_image = image[stats[i][1]:stats[i][1]+stats[i][3],stats[i][0]:stats[i][0]+stats[i][2]]
        white_img = cv2.imread(f'templates/numbers/white.jpg')
        white_img = cv2.cvtColor(white_img, cv2.COLOR_BGR2GRAY)

        height, width = cut_image.shape[:2]
        white_img[0:height, 0:width] = cut_image
        cut_image = white_img

        similarity = 0
        pred_num=0
        for i in range(10):
            tmp_img = cv2.imread(f'templates/numbers/{i}.jpg')
            tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(cut_image, tmp_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val>similarity:
                pred_num = i
                similarity = max_val
        kcal_str = kcal_str + str(pred_num)
    print(f"{kcal_str}kcalと推定します。")
    return int(kcal_str)

def is_result_image():
    fetch_image = cv2.imread('temp.jpg')

    # fetch_imageのsizeが公式のものでなければout
    h, w, _ = fetch_image.shape
    if h != 720 or w != 1280:
        return None

    result = cv2.matchTemplate(fetch_image, TEMPLATE, cv2.TM_CCOEFF_NORMED)
    # 検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if max_val > THRESHOLD:
        return ImageType.EXERCISE_IMAGE
    result = cv2.matchTemplate(fetch_image, TEMPLATE2, cv2.TM_CCOEFF_NORMED)
    # 検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if max_val > THRESHOLD:
        return ImageType.CUSTOM_EXERCISE_IMAGE
    else:
        return None


def image_to_data(imagetype):
    fetch_image = cv2.imread('temp.jpg')

    # 各部分の画像を切り出す
    if imagetype == ImageType.EXERCISE_IMAGE:
        # total_time = fetch_image[257:257 + 84, 552:552 + 404]
        total_cal = fetch_image[400:400 + 60, 617:617 + 197]
        # total_distance = fetch_image[493:493 + 76, 560:560 + 396]
    elif imagetype == ImageType.CUSTOM_EXERCISE_IMAGE:
        total_cal = fetch_image[438:438 + 60, 617:617 + 197]
    else:
        print(imagetype)
        raise ValueError("An error has ocurred! Image is not a exercise image.")


    # dummyData
    time = datetime.time(second=0)
    cal = read_cal_by_connectedComponets(total_cal)
    distance = 0
    return ExerciseData(time, cal,distance)


def convert_datalist_to_timelist(exercise_data_list):
    return [e.time.hour + (e.time.minute / 60.0) + (e.time.second / 3600.0) for e in
            exercise_data_list]


def convert_datatuple_to_list(exercise_data_list):
    return [e[0] for e in exercise_data_list]


def datalist_to_histogram(exercise_list, ranking):
    plt.figure()
    n, bins, patches = plt.hist(exercise_list, color='darkturquoise', ec='black', bins=HISTGRAM_BINS,range=(0,max(exercise_list)))
    print(n, bins)
    print(exercise_list[ranking])
    print("xは", np.where(exercise_list[ranking] >= bins)[0][-1])
    x = np.where(exercise_list[ranking] >= bins)[0][-1]
    if x == HISTGRAM_BINS: x = x - 1

    cm = generate_cmap(['dodgerblue','darkturquoise', 'aqua','cyan'])
    for i in range(HISTGRAM_BINS):
        patches[i].set_facecolor(plt.get_cmap(cm)((bins[i] / bins[HISTGRAM_BINS])*1))
    if x == HISTGRAM_BINS: x = x-1
    patches[x].set_facecolor('tomato')

    # y軸を整数にする
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig('hist.png')  # ヒストグラムを保存
    plt.close()


if __name__ == '__main__':
    is_result_image()

    import sqlite3
    import config

    # ヒストグラムのテスト
    print("ヒストグラムテスト")
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("select kcal from Exercise "
                "WHERE date(time_stamp) == '2020-06-01' and kcal > 250 ORDER BY kcal DESC ;")
    exercise_data_list = cur.fetchall()
    print(exercise_data_list)
    num_list = convert_datatuple_to_list(exercise_data_list)

    #num_list = [0, 10, 10, 10, 10.1, 30, 30, 30, 30.2, 40, 50, 70, 90, 200]
    time_ranking = 2
    plt.figure()
    n, bins, patches = plt.hist(num_list, color='darkturquoise', ec='black', bins=HISTGRAM_BINS,range=(0,max(num_list)))
    print(n, bins)
    print(np.where(num_list[time_ranking] >= bins)[0])

    print(np.where(num_list[time_ranking] >= bins)[0][-1])
    x = np.where(num_list[time_ranking] >= bins)[0][-1]
    cm = generate_cmap(['dodgerblue','darkturquoise', 'aqua','cyan'])
    for i in range(HISTGRAM_BINS):
        patches[i].set_facecolor(plt.get_cmap(cm)((bins[i] / bins[HISTGRAM_BINS])*1))
    if x == HISTGRAM_BINS: x = x-1
    patches[x].set_facecolor('tomato')
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig('hist.png')
    plt.show()

    # 画像の計測テスト
    print("画像の計測テスト")
    fetch_image = cv2.imread('debugging_images/robust4.jpg')
    result = cv2.matchTemplate(fetch_image, TEMPLATE, cv2.TM_CCOEFF_NORMED)
    # 検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if max_val > THRESHOLD:
        print(ImageType.EXERCISE_IMAGE)
    result = cv2.matchTemplate(fetch_image, TEMPLATE2, cv2.TM_CCOEFF_NORMED)
    # 検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)

    # 各部分の画像を切り出す
    total_cal = fetch_image[400:400 + 60, 617:617 + 197]
    #total_cal = fetch_image[438:438 + 60, 617:617 + 197]

    # time = read_time(total_time)
    # dummyData
    time = datetime.time(second=0)

    cal = read_cal_by_connectedComponets(total_cal)
