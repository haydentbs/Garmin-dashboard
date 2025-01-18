CREATE TABLE IF NOT EXISTS daily_steps (
    date TIMESTAMP PRIMARY KEY,
    total_steps INTEGER,
    distance INTEGER,
    step_goal INTEGER
);