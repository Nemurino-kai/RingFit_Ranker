# coding: utf-8
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dateutil.relativedelta import relativedelta
import uvicorn
from datetime import datetime, date, timedelta, timezone
from typing import Optional
from sql_alchemy.schemes import DailyResponse, MonthlyResponse, UserResponse
from sql_alchemy.controller import get_daily_ranking, get_monthly_ranking, get_user_ranking
from sql_alchemy.models import get_db, Session
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


@app.get('/api', response_model=DailyResponse)
def daily(session: Session = Depends(get_db), day: Optional[date] = (datetime.now(JST) - timedelta(hours=4)).date()):
    stop_day = day + timedelta(days=1)

    exercise_data_list = get_daily_ranking(session, day)

    return DailyResponse(start_day=day, stop_day=stop_day, exercise_data_list=exercise_data_list)


@app.get('/api/monthly', response_model=MonthlyResponse)
def monthly(session: Session = Depends(get_db),
            month: Optional[str] = (datetime.now(
                JST) - timedelta(hours=4)).strftime("%Y-%m")):
    start_day = month + "-01"
    stop_day = (datetime.strptime(start_day, "%Y-%m-%d") +
                relativedelta(months=1)).strftime("%Y-%m-%d")

    exercise_data_list = get_monthly_ranking(session, month)

    return MonthlyResponse(start_day=start_day, stop_day=stop_day, exercise_data_list=exercise_data_list)


@app.get('/api/user', response_model=UserResponse)
def user(user: str, session: Session = Depends(get_db)):
    user_exercise_data_list = get_user_ranking(session, user)
    return UserResponse(user_exercise_data_list=user_exercise_data_list)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
