from typing import List
from datetime import date
from pydantic import BaseModel


class DailyExerciseData(BaseModel):
    ranking: int
    user_name: str
    kcal: int
    tweeted_time: str


class DailyResponse(BaseModel):
    start_day: date
    stop_day: date
    exercise_data_list: List[DailyExerciseData]


class MonthlyExerciseData(BaseModel):
    ranking: int
    user_name: str
    monthly_kcal: int
    days: int


class MonthlyResponse(BaseModel):
    start_day: date
    stop_day: date
    exercise_data_list: List[MonthlyExerciseData]


class UserExerciseData(BaseModel):
    daily_rank: int
    kcal: int
    tweeted_time: str
    weeknumber: int


class UserResponse(BaseModel):
    user_exercise_data_list: List[UserExerciseData]
