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
    cur.execute("select user_name,kcal,time_stamp from Exercise "
                "WHERE date(time_stamp) == date('now','+9 hour') ORDER BY kcal DESC ;"
    )
    exercise_data_list = cur.fetchall()
    print(exercise_data_list)
    return render_template('index.html',results = exercise_data_list)


if __name__ == '__main__':
    app.run()