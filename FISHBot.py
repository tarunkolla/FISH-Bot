import sqlite3
import json
from datetime import datetime

timeframe = '2017-05'  # easy to run code on other comments too
sql_transaction= []

connection = sqlite3.connect('{}.db'.format(timeframe))  # sqlite creates a db for us
cursor = connection.cursor()

def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS 
parent_reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, 
comment TEXT, subreddit TEXT, unix INT, score INT)""")


def format_data(format):
    format = format.replace("\n", " tarunkolla ").replace("\r", " tarunkolla ").replace('"', "'")
    return format


def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as error:
        #print("find_parent", error)
        return False

if __name__ == "__main__":
    create_table()
    row_counter = 0
    paired_rows = 0  # to check if comments have replies

    with open("C:/Users/Tarun kolla/Desktop/FISH Bot/RC_{}".format(timeframe), buffering= 1000) as file:
        for row in file:
            #print(row)
            row_counter +=1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']

            parent_data = find_parent(parent_id)
