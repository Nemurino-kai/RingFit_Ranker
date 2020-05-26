# coding: utf-8
from flask import Flask, render_template
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
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    if datetime.datetime.now(JST).hour < 4:
        # 昨日の4時～今
        now = datetime.datetime.now(JST)
        yesterday = now - datetime.timedelta(days=1)
        stop_t = now.strftime("%Y-%m-%d %H:%M:%S")
        start_t = yesterday.strftime("%Y-%m-%d ") + "04:00:00"
        params = (start_t,stop_t)
    else:
        # 今日の4時～今
        now = datetime.datetime.now(JST)
        stop_t = now.strftime("%Y-%m-%d %H:%M:%S")
        start_t = now.strftime("%Y-%m-%d ") + "04:00:00"
        params = (start_t,stop_t)

    print(params)
    cur.execute("select RANK() OVER(ORDER BY kcal DESC) AS ranking,user_name,kcal,tweeted_time from Exercise "
                "WHERE  time_stamp BETWEEN ? AND ? ORDER BY kcal DESC ;",params
    )


    exercise_data_list = cur.fetchall()
    print(exercise_data_list)
    return render_template('index.html',results = exercise_data_list)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()