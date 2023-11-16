import sqlite3
import bcrypt

connection = sqlite3.connect('database.db')

SECRET_KEY="49e31e809b72d4b0bc9a7353bcfeac2deafeb22b41065c44440cb0b1b99e339e"

salt = bcrypt.gensalt()

dummy_users = [
        {
            "id": "a1c28c6b-e932-4423-958a-9ea427e69d0b",
            "username": "user1",
            "email": "user1@example.com",
            "password": b"password1"
        },
        {
            "id": "24e7f7a2-72a2-48ab-8776-1f0f3ec4f09b",
            "username": "user2",
            "email": "user2@example.com",
            "password": b"password2"
        },
        {
            "id": "c7a301f8-9ca5-4813-920c-798b5e0e3301",
            "username": "user3",
            "email": "user3@example.com",
            "password": b"password3"
        },
        {
            "id": "5a9f344a-1a84-43d7-95df-7c6b6e4ddce5",
            "username": "user4",
            "email": "user4@example.com",
            "password": b"password4"
        },
        {
            "id": "b9f999f6-8937-48b7-9b8e-0b16dd53c073",
            "username": "user5",
            "email": "user5@example.com",
            "password": b"password5"
        }
    ]


with open('admin.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for i in dummy_users:
    password = i['password']
    hashed_pw = bcrypt.hashpw(password, salt)
    cur.execute("INSERT INTO admin (id, username, email, password) VALUES (?, ?, ?, ?)",
            (i['id'], i['username'], i['email'], hashed_pw.decode("utf8")))
    
    


connection.commit()
connection.close()