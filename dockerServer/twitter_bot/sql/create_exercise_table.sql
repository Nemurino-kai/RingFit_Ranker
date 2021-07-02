CREATE TABLE Exercise (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_stamp TEXT NOT NULL DEFAULT (DATETIME('now', '+9 hours')),
        tweeted_time TEXT NOT NULL,
        kcal INTEGER NOT NULL ,
        user_name TEXT NOT NULL ,
        user_screen_name TEXT NOT NULL ,
        tweet_id NUMERIC NOT NULL UNIQUE ,
        exercise_day TEXT GENERATED ALWAYS AS (date(datetime(tweeted_time,'-4 hours'))) VIRTUAL ,
        exercise_month TEXT GENERATED ALWAYS AS (strftime('%Y-%m', datetime(tweeted_time,'-4 hours'))) VIRTUAL
        );

CREATE INDEX user_screen_name_index ON Exercise(user_screen_name);
CREATE INDEX exercise_day_index ON Exercise(exercise_day);
CREATE INDEX exercise_month_index ON Exercise(exercise_month);
