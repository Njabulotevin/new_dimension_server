DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
    id UUID PRIMARY KEY,
    email Char(255) NOT NULL,
    username CHAR(255) NOT NULL,
    password CHAR(255) NOT NULL
);