# coding: utf-8
from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
import config
import sqlite3
import datetime

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
    return render_template('index.html',results = exercise_data_list,start_t = start_t,start_day=start_day,stop_t=stop_t,max_day=max_day)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('internal_server_error.html'), 500


if __name__ == '__main__':
    app.run()