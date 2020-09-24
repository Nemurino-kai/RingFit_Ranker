# coding: utf-8
from flask import Blueprint,request, jsonify
import config
import sqlite3
import datetime


module_api = Blueprint('info_api',__name__)
# タイムゾーン指定
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

def dict_factory(cursor, row):
   d = {}
   for idx, col in enumerate(cursor.description):
       d[col[0]] = row[idx]
   return d

@module_api.route('/api')
def api_index():

    day = request.args.get('day')
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    now = datetime.datetime.now(JST)
    ranking_timestamp = now - datetime.timedelta(hours=4)
    max_day = ranking_timestamp.strftime("%Y-%m-%d")

    if day is None:
        day = max_day

    stop_day = (datetime.datetime.strptime(day,"%Y-%m-%d")+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    params=(day,)

    print(params)

    cur.execute("SELECT id,RANK() OVER(ORDER BY kcal DESC) AS ranking,user_name,kcal,tweeted_time "
                "FROM (SELECT *, RANK() OVER(PARTITION BY user_screen_name ORDER BY kcal DESC, id) AS rnk FROM Exercise WHERE   date(datetime(tweeted_time,'-4 hours'))==?) tmp "
                "WHERE rnk = 1 ORDER BY kcal DESC, tweeted_time ASC;",params)

    exercise_data_list = cur.fetchall()

    return jsonify({
        'start_day':day,
        'stop_day': stop_day,
        'exercise_data_list': exercise_data_list
    }), 200

@module_api.route('/api/user')
def api_user():
    user = request.args.get('user')
    conn = sqlite3.connect(config.DATABASE_NAME)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if user is None: user = ""
    params=(user,)

    cur.execute("WITH NonOverlapTable AS (SELECT *, RANK() OVER(PARTITION BY user_screen_name, date(datetime(tweeted_time,'-4 hours')) ORDER BY kcal DESC, id) AS rnk FROM Exercise)"
                ",DailyRankedTable AS (SELECT *,RANK() OVER(PARTITION BY date(datetime(tweeted_time,'-4 hours')) ORDER BY kcal DESC) AS daily_rank FROM NonOverlapTable WHERE rnk = 1)"
                "SELECT id,daily_rank,kcal,tweeted_time, strftime('%w', datetime(tweeted_time,'-4 hours')) AS weeknumber FROM DailyRankedTable WHERE rnk = 1 AND user_screen_name==? ORDER BY tweeted_time DESC;",params)

    exercise_data_list = cur.fetchall()

    return jsonify({
        'user_exercise_data_list': exercise_data_list
    }), 200
