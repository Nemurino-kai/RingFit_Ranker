from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Exercise
from schemes import DailyExerciseData, MonthlyExerciseData, UserExerciseData
from datetime import datetime, date
from sqlalchemy import and_


def get_daily_ranking(session: Session, day: date) -> List[DailyExerciseData]:

    one_day_exercise = session.query(Exercise).filter(
        Exercise.exercise_day == day).subquery()

    individual_ranked = session.query(one_day_exercise,
                                      func.rank().over(
                                          order_by=and_(
                                              Exercise.kcal.desc(), Exercise.id),
                                          partition_by=Exercise.user_screen_name
                                      ).label('rnk')).filter(Exercise.id == one_day_exercise.c.id).subquery()

    individual_best = session.query(
        individual_ranked).filter(individual_ranked.c.rnk == 1).subquery()

    ranked_exercise = session.query(individual_best, func.rank().over(
        order_by=individual_best.c.kcal.desc()).label('ranking')).subquery()

    aligned_exercise = session.query(ranked_exercise.c.id,
                                     ranked_exercise.c.ranking,
                                     ranked_exercise.c.user_name,
                                     ranked_exercise.c.kcal,
                                     ranked_exercise.c.tweeted_time).order_by(
        ranked_exercise.c.kcal.desc(), ranked_exercise.c.tweeted_time).all()

    format_exercise = [DailyExerciseData(
        ranking=r.ranking, user_name=r.user_name, kcal=r.kcal, tweeted_time=str(r.tweeted_time))
        for r in aligned_exercise]

    return format_exercise


def get_monthly_ranking(session: Session, month: str) -> List[MonthlyExerciseData]:
    one_month_exercise = session.query(Exercise).filter(
        Exercise.exercise_month == month).subquery()

    individual_ranked = session.query(one_month_exercise,
                                      func.rank().over(
                                          order_by=and_(
                                              Exercise.kcal.desc(), Exercise.id),
                                          partition_by=and_(
                                              Exercise.user_screen_name, Exercise.exercise_day)
                                      ).label('rnk')).filter(Exercise.id == one_month_exercise.c.id).subquery()

    individual_best = session.query(
        individual_ranked).filter(individual_ranked.c.rnk == 1).subquery()

    ranked_exercise = session.query(individual_best, func.rank().over(
        order_by=func.sum(individual_best.c.kcal).desc()
    ).label('ranking'),
        func.sum(individual_best.c.kcal).label('monthly_kcal'),
        func.count(individual_best.c.user_screen_name).label('days')).group_by(individual_best.c.user_screen_name).all()

    format_exercise = [MonthlyExerciseData(
        ranking=r.ranking, user_name=r.user_name, monthly_kcal=r.monthly_kcal, days=r.days)
        for r in ranked_exercise]

    return format_exercise


def get_user_results(session: Session, user_screen_name: str) -> List[UserExerciseData]:

    individual_ranked = session.query(Exercise, func.rank().over(
        order_by=and_(Exercise.kcal.desc(), Exercise.id),
        partition_by=and_(Exercise.exercise_day, Exercise.user_screen_name)
    ).label('rnk')).subquery()

    individual_best = session.query(
        individual_ranked).filter(individual_ranked.c.rnk == 1).subquery()

    daily_ranked_table = session.query(individual_best, func.rank().over(
        order_by=Exercise.kcal.desc(),
        partition_by=Exercise.exercise_day
    ).label('daily_rank')).filter(Exercise.id == individual_best.c.id).subquery()

    user_results = session.query(
        daily_ranked_table).filter(Exercise.user_screen_name == user_screen_name)\
        .filter(Exercise.id == daily_ranked_table.c.id).all()

    format_exercise = [UserExerciseData(
        daily_rank=r.daily_rank, kcal=r.kcal, tweeted_time=str(r.tweeted_time),
        weeknumber=datetime.strptime(r.exercise_day, '%Y-%m-%d').weekday()) for r in user_results]

    return format_exercise
