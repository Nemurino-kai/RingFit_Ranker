# coding: utf-8
from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
import config
import sqlite3
import datetime
import info_convert
import pandas as pd

app = Flask(__name__)
bootstrap = Bootstrap(app)

# タイムゾーン指定
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

@app.route('/')
def index():

    day = request.args.get('day')
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()

    if datetime.datetime.now(JST).hour < 4:
            # 昨日の4時～今
            now = datetime.datetime.now(JST)
            yesterday = now - datetime.timedelta(days=1)
            stop_t = now.strftime("%Y-%m-%d %H:%M:%S")
            start_day = yesterday.strftime("%Y-%m-%d")
            start_t = start_day + " 04:00:00"
            params = (start_t,stop_t)
            max_day=start_day
    else:
            # 今日の4時～今
            now = datetime.datetime.now(JST)
            stop_t = now.strftime("%Y-%m-%d %H:%M:%S")
            start_day = now.strftime("%Y-%m-%d")
            start_t = start_day + " 04:00:00"
            params = (start_t,stop_t)
            max_day = start_day

    if day is not None:
        # 指定日前日の4時～指定日の3時59分59秒
        start_day = day
        stop_day = datetime.datetime.strftime(datetime.datetime.strptime(day,'%Y-%m-%d') + datetime.timedelta(days=1),'%Y-%m-%d')
        stop_t = stop_day + " 03:59:59"
        start_t = start_day + " 04:00:00"
        params = (start_t, stop_t)

    print(params)
    cur.execute("select RANK() OVER(ORDER BY kcal DESC) AS ranking,user_name,kcal,tweeted_time from Exercise "
                "WHERE  time_stamp BETWEEN ? AND ? ORDER BY kcal DESC ;",params
    )


    exercise_data_list = cur.fetchall()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = exercise_data_list[(page - 1) * 100: page * 100]
    pagination = Pagination(page=page, total=len(exercise_data_list), per_page=100, css_framework='bootstrap4')

    return render_template('index.html',results = res,start_t = start_t,start_day=start_day,
                           stop_t=stop_t,max_day=max_day, pagination=pagination)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analytics')
def analytics():
    day = request.args.get('day')
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()

    if datetime.datetime.now(JST).hour < 4:
            # 昨日の4時～今
            now = datetime.datetime.now(JST)
            yesterday = now - datetime.timedelta(days=1)
            stop_t = now.strftime("%Y-%m-%d %H:%M:%S")
            start_day = yesterday.strftime("%Y-%m-%d")
            start_t = start_day + " 04:00:00"
            params = (start_t,stop_t)
            max_day=start_day
    else:
            # 今日の4時～今
            now = datetime.datetime.now(JST)
            stop_t = now.strftime("%Y-%m-%d %H:%M:%S")
            start_day = now.strftime("%Y-%m-%d")
            start_t = start_day + " 04:00:00"
            params = (start_t,stop_t)
            max_day = start_day

    if day is not None:
        # 指定日前日の4時～指定日の3時59分59秒
        start_day = day
        stop_day = datetime.datetime.strftime(datetime.datetime.strptime(day,'%Y-%m-%d') + datetime.timedelta(days=1),'%Y-%m-%d')
        stop_t = stop_day + " 03:59:59"
        start_t = start_day + " 04:00:00"
        params = (start_t, stop_t)

    print(params)
    cur.execute("select time_stamp from Exercise "
                "WHERE time_stamp BETWEEN ? AND ? ORDER BY time_stamp DESC ;",params
    )


    exercise_data_list = cur.fetchall()

    exercise_data_list = info_convert.convert_datatuple_to_callist(exercise_data_list)
    df = pd.DataFrame(exercise_data_list, columns=['time_stamp'])
    dateTimeIndex = pd.DatetimeIndex(df['time_stamp'])
    df.index = dateTimeIndex
    hist = df.groupby(pd.Grouper(freq='60min')).groups
    print(hist)
    bins = list(hist.keys())
    hist = list( hist.values() )
    bins = map(lambda x: x * 2, bins)
    print(hist)
    print(bins)
    #n, bins = np.histogram(exercise_data_list,bins=30)
    #n=n.tolist()
    n=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

    return render_template('analytics.html',start_t = start_t,start_day=start_day,
                           stop_t=stop_t,max_day=max_day, n=hist,bins=bins)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500


if __name__ == '__main__':
    app.run()