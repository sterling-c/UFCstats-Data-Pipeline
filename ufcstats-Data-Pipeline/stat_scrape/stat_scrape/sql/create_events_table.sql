CREATE TABLE IF NOT EXISTS events
(
    id varchar(255) NOT NULL,
    name varchar(255),
    date date NOT NULL,
    location varchar(255),
    link varchar(255) NOT NULL
);