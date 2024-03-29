CREATE TABLE IF NOT EXISTS fighters
(
    id varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    t_wins integer NOT NULL,
    t_losses integer NOT NULL,
    t_draws integer NOT NULL,
    t_no_contests integer NOT NULL,
    nickname varchar(255),
    ufc_wins integer NOT NULL,
    ufc_losses integer NOT NULL,
    ufc_draws integer NOT NULL,
    ufc_no_contests integer NOT NULL,
    height integer,
    reach integer,
    stance varchar(255),
    date_of_birth date,
    sig_strike_landed real NOT NULL,
    sig_strike_accuracy integer NOT NULL,
    sig_strike_absorbed real NOT NULL,
    strike_defense integer NOT NULL,
    takedown_average real NOT NULL,
    takedown_accuracy integer NOT NULL,
    takedown_defense integer NOT NULL,
    submission_average real NOT NULL,
    link varchar(255) NOT NULL
)