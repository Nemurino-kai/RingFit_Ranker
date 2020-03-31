import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import os
import re
import datetime
import numpy as np

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './client_credentials.json'
THRESHOLD = 0.95
TEMPLATE = cv2.imread('template.jpg')


class ExerciseData:
    def __init__(self, time, cal, user_name):
        self.exercise_time = time
        self.exercise_cal = cal
        self.user_name = user_name


def read_text(image):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    # Performs text detection on the image file
    _, decode_image = cv2.imencode('.jpg', image)
    decode_image = decode_image.tobytes()
    decode_image = types.Image(content=decode_image)
    response = client.text_detection(image=decode_image)
    texts = response.text_annotations
    return texts


def read_time(time_image):
    texts = read_text(time_image)
    # 数字だけを抽出する
    regex = re.compile(r'\d+')
    time_array = []
    for line in str(texts[0].description).splitlines():
        match = regex.findall(line)
        time_array.extend(match)
    print(time_array)
    # time型に変換
    try:
        if len(time_array) == 1:
            return datetime.time(second=int(time_array[0]))
        if len(time_array) == 2:
            return datetime.time(minute=int(time_array[0]), second=int(time_array[1]))
        if len(time_array) == 3:
            return datetime.time(hour=int(time_array[0]), minute=int(time_array[1]), second=int(time_array[2]))
    except:
        print("Can't Read Error")
        # TODO: Error処理をきちんとする
        return datetime.time(second=0)


def read_cal(cal_image):
    texts = read_text(cal_image)
    for text in texts:
        print(text.description)
    # 小数付きでkcalを返す
    return float(re.findall(r"[-+]?\d*\.\d+|\d+", texts[0].description)[0])


def is_result_image():
    fetch_image = cv2.imread('temp.jpg')

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
    total_cal = fetch_image[396:396 + 65, 586:586 + 371]
    total_distance = fetch_image[493:493 + 76, 560:560 + 396]

    # time = read_time(total_time)
    # dummyData
    time = datetime.time(second=0)
    cal = read_cal(total_cal)
    return ExerciseData(time, cal, user_name)


def convert_datalist_to_timelist(exercise_data_list):
    return [e.exercise_time.hour + (e.exercise_time.minute / 60.0) + (e.exercise_time.second / 3600.0) for e in
            exercise_data_list]


def convert_datalist_to_callist(exercise_data_list):
    return [e.exercise_cal for e in exercise_data_list]


def datalist_to_histogram(exercise_list, ranking):
    n, bins, patches = plt.hist(exercise_list, color='darkturquoise', ec='black', bins=20)
    print(n, bins)
    print(exercise_list[ranking])
    print("xは", np.where(exercise_list[ranking] >= bins)[0][-1])
    x = np.where(exercise_list[ranking] >= bins)[0][-1]
    patches[x].set_facecolor('tomato')
    # y軸を整数にする
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig('hist.png')  # ヒストグラムを保存


if __name__ == '__main__':
    # ヒストグラムのテスト
    num_list = [0, 0, 0, 10, 10.1, 30, 30, 30, 30.2, 40, 50, 70, 90, 200]
    time_ranking = 9
    n, bins, patches = plt.hist(num_list, color='darkturquoise', ec='black', bins=20)
    print(n, bins)
    print(np.where(num_list[time_ranking] >= bins)[0][-1])
    x = np.where(num_list[time_ranking] >= bins)[0][-1]
    patches[x].set_facecolor('tomato')
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.savefig('hist.png')
    plt.show()
