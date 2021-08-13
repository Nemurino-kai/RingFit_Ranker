# coding: utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dateutil.relativedelta import relativedelta
import uvicorn
from datetime import datetime, date, timedelta, timezone
from typing import Optional
import sqlite3
import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from dotenv import load_dotenv
load_dotenv()

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*'],
)

asgi_app = SentryAsgiMiddleware(app)

# タイムゾーン指定
JST = timezone(timedelta(hours=+9), 'JST')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.get('/api')
def api_index(day: Optional[date] = None):

    conn = sqlite3.connect(os.environ['DATABASE_NAME'])
    conn.row_factory = dict_factory
    cur = conn.cursor()

    if day is None:
        now = datetime.now(JST)
        day = (now - timedelta(hours=4)).date()

    stop_day = day + timedelta(days=1)
    params = (day,)

    print(params)

    cur.execute("SELECT id,RANK() OVER(ORDER BY kcal DESC) AS ranking,user_name,kcal,tweeted_time "
                "FROM (SELECT *, RANK() OVER(PARTITION BY user_screen_name ORDER BY kcal DESC, id) AS rnk FROM Exercise WHERE exercise_day==?) tmp "
                "WHERE rnk = 1 ORDER BY kcal DESC, tweeted_time ASC;", params)

    exercise_data_list = cur.fetchall()

    return {
        'start_day': day.strftime("%Y-%m-%d"),
        'stop_day': stop_day.strftime("%Y-%m-%d"),
        'exercise_data_list': exercise_data_list
    }


@app.get('/api/monthly')
def api_monthly(month: str = None):

    conn = sqlite3.connect(os.environ['DATABASE_NAME'])
    conn.row_factory = dict_factory
    cur = conn.cursor()

    if month is None:
        now = datetime.now(JST)
        ranking_timestamp = now - timedelta(hours=4)
        start_day = ranking_timestamp.strftime("%Y-%m") + "-01"
    else:
        start_day = month + "-01"

    stop_day = (datetime.strptime(start_day, "%Y-%m-%d") +
                relativedelta(months=1)).strftime("%Y-%m-%d")
    params = (start_day,)

    print(params)

    cur.execute("SELECT id,RANK() OVER(ORDER BY SUM(kcal) DESC) AS ranking,user_name,SUM(kcal) AS monthly_kcal,COUNT(user_name) AS days "
                "FROM (SELECT *, RANK() OVER(PARTITION BY [user_screen_name],[exercise_day] ORDER BY kcal DESC, id) AS rnk "
                "FROM (SELECT * FROM Exercise) WHERE exercise_month == strftime('%Y-%m',?)) tmp "
                "WHERE rnk = 1 GROUP BY user_screen_name ORDER BY monthly_kcal DESC, tweeted_time ASC ;", params)

    exercise_data_list = cur.fetchall()

    return {
        'start_day': start_day,
        'stop_day': stop_day,
        'exercise_data_list': exercise_data_list
    }


@app.get('/api/user')
def api_user(user: str = None):
    conn = sqlite3.connect(os.environ['DATABASE_NAME'])
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if user is None:
        return {'user_exercise_data_list': []}
    params = (user,)

    cur.execute("WITH NonOverlapTable AS (SELECT *, RANK() OVER(PARTITION BY user_screen_name, exercise_day ORDER BY kcal DESC, id) AS rnk FROM Exercise)"
                ",DailyRankedTable AS (SELECT *,RANK() OVER(PARTITION BY exercise_day ORDER BY kcal DESC) AS daily_rank FROM NonOverlapTable WHERE rnk = 1)"
                "SELECT id,daily_rank,kcal,tweeted_time, strftime('%w', datetime(tweeted_time,'-4 hours')) AS weeknumber FROM DailyRankedTable WHERE rnk = 1 AND user_screen_name==? ORDER BY tweeted_time DESC;", params)

    exercise_data_list = cur.fetchall()

    return {
        'user_exercise_data_list': exercise_data_list
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
