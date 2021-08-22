from sqlalchemy.sql import func
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Column, String, DateTime, Integer, Computed, BigInteger
import datetime
import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append('./')


class RepresentableBase(object):
    def __repr__(self):
        """Dump all columns and value automagically.

        This code is copied a lot from followings.
        See also:
           - https://gist.github.com/exhuma/5935162#file-representable_base-py
           - http://stackoverflow.com/a/15929677
        """
        #: Columns.
        columns = ', '.join([
            '{0}={1}'.format(k, repr(self.__dict__[k]))
            for k in self.__dict__.keys() if k[0] != '_'
        ])

        return '<{0}({1})>'.format(
            self.__class__.__name__, columns
        )


meta = MetaData()

engine = create_engine(
    "sqlite:///" + os.environ["DATABASE_NAME"], connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(cls=RepresentableBase)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clear_database():
    session = SessionLocal()
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        try:
            session.execute(table.delete())
        except:
            pass
    session.commit()


def create_database():
    clear_database()
    Base.metadata.create_all(bind=engine)


class Exercise(Base):
    __tablename__ = "Exercise"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    time_stamp = Column(DateTime(timezone=True), nullable=False,
                        server_default=func.now(), onupdate=func.now())
    tweeted_time = Column(DateTime, nullable=False)
    kcal = Column(Integer, nullable=False)
    user_name = Column(String(255), nullable=False)
    user_screen_name = Column(String(255), nullable=False, index=True)
    tweet_id = Column(BigInteger, nullable=False, unique=True)
    exercise_day = Column(String(255), Computed(
        "date(datetime(tweeted_time,'-4 hours'))"), index=True)
    exercise_month = Column(String(255), Computed(
        "strftime('%Y-%m', datetime(tweeted_time,'-4 hours'))"), index=True)


def move_sql(db_path: str):
    import sqlite3
    from datetime import datetime as dt

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * from Exercise")

    exercise_data_list = cur.fetchall()
    print(exercise_data_list[0])
    session = SessionLocal()
    modified = [Exercise(time_stamp=dt.strptime(e[1], '%Y-%m-%d %H:%M:%S'),
                         tweeted_time=dt.strptime(e[2], '%Y-%m-%d %H:%M:%S'), kcal=e[3], user_name=e[4],
                         user_screen_name=e[5], tweet_id=e[6]) for e in exercise_data_list]
    session.add_all(modified)
    session.commit()

    session.close()


def add_fixture():
    session = SessionLocal()
    results = [Exercise(tweeted_time=datetime.datetime(2021, 8, i, i, 0), kcal=i * 100, user_name=f'{i}さん',
                        user_screen_name=f'{i}_san', tweet_id=f'{i}') for i in range(1, 6)]
    session.add_all(results)
    session.commit()

    session.close()


if __name__ == '__main__':
    create_database()
