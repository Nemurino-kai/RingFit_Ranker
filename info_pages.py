# coding: utf-8
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import config
import sqlite3
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)



@app.route('/')
def index():
    conn = sqlite3.connect(config.DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("select RANK() OVER(ORDER BY kcal DESC) AS ranking,user_name,kcal,tweeted_time from Exercise "
                "WHERE date(time_stamp) == date('now','+9 hour') ORDER BY kcal DESC ;"
    )
    exercise_data_list = cur.fetchall()
    print(exercise_data_list)
    return render_template('index.html',results = exercise_data_list)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()