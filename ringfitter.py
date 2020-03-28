import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import os
import re
import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './client_credentials.json'
THRESHOLD=0.95
TEMPLATE = cv2.imread('template.jpg')


def readText(image):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    # Performs text detection on the image file
    _, decode_image = cv2.imencode('.jpg', image)
    decode_image = decode_image.tobytes()
    decode_image = types.Image(content=decode_image)
    response = client.text_detection(image=decode_image)
    texts = response.text_annotations
    return texts

def readTime(time_image):
    texts = readText(time_image)
    #数字だけを抽出する
    regex = re.compile('\d+')
    time_array =[]
    for line in str(texts[0].description).splitlines():
        match = regex.findall(line)
        time_array.extend(match)
    print(time_array)
    #time型に変換
    if(len(time_array)==1):
        return datetime.time(second=int(time_array[0]))
    if(len(time_array)==2):
        return datetime.time(minute=int(time_array[0]),second=int(time_array[1]))
    if(len(time_array)==3):
        return datetime.time(hour=int(time_array[0]),minute=int(time_array[1]),second=int(time_array[2]))

def readCal(cal_image):
    texts = readText(cal_image)
    for text in texts:
        print(text.description)
    # 小数付きでkcalを返す
    return float(re.findall("\d+\.\d+",texts[0].description)[0])

def isResultImage():
    fetch_image = cv2.imread('temp.jpg')

    result = cv2.matchTemplate(fetch_image, TEMPLATE, cv2.TM_CCOEFF_NORMED)
    #検出結果から検出領域の位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    if(max_val > THRESHOLD):return True
    else: return False

def ImageToText():
    fetch_image = cv2.imread('temp.jpg')

    #各部分の画像を切り出す
    total_time =  fetch_image[257:257+84,552:552+404]
    total_cal =  fetch_image[396:396+65,586:586+371]
    total_distance = fetch_image[493:493+76,560:560+396]

    time = readTime(total_time)
    return (str(time)+' 頑張ったね！お疲れ様！')
