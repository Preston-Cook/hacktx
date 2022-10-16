import os
import psycopg2
from psycopg2 import Error
from weather import retrieve_weather
from news import retrieve_news

CONNECTION_STR = os.environ.get('CONNECTION_STR')

def create_table():
    try:
        conn = psycopg2.connect(CONNECTION_STR)
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS bikes (id INT PRIMARY KEY, title STRING, price INT)')
        conn.commit()
        conn.close()

    except (Exception, Error) as e:
        print(f'Error Creating Table: {e}')

def keyword_check(prompt):
    res = None
    
    if 'weather' in prompt:
        res = retrieve_weather(prompt)
    elif 'news' in prompt:
        res = retrieve_news(prompt)
    
    return res