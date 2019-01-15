import sqlite3
import json
from datetime import datetime

timeframe = '2018-05'  # easy to run code on other comments too
sql_transaction= []

connection = sqlite3.connect('{}.db'.format(timeframe))  # sqlite creates a db for us
cursor = connection.cursor()

def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS 
parent_reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, 
comment TEXT, subreddit TEXT, unix INT, score INT)""")


def format_data(data):
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")
    return data


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


def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as error:
        #print("find_existing_score", str(error))
        return False


def transaction_builder(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        cursor.execute('BEGIN TRANSACTION')
        for each in sql_transaction:
            try:
                cursor.execute(each)
            except:
                pass
        connection.commit()
        sql_transaction = []


def acceptable_comment(comment):
    if len(comment.split(' ')) > 50 or len(comment) < 1:
        return  False
    elif len(comment) > 1000:
        return False
    elif comment == '[deleted]' or comment == '[removed]':
        return False
    else:
        return True


def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_builder(sql)
    except Exception as error:
        print('s-update insertion',str(error))


def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_builder(sql)
    except Exception as error:
        print('s-parent insertion',str(error))


def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_builder(sql)
    except Exception as error:
        print('s-noparent  insertion',str(error))


if __name__ == "__main__":
    create_table()
    row_counter = 0
    paired_rows = 0  # to check if comments have replies

    with open("C:/Users/Tarun kolla/Desktop/FISHBot/RC_{}".format(timeframe), buffering= 1000) as file:
        for row in file:
            #print(row)
            row_counter +=1
            row = json.loads(row)
            parent_id = row['parent_id'].split('_')[1]
            comment_id = row['id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            parent_data = find_parent(parent_id)

            if score >= 2:
                if acceptable_comment(body):
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                    else:
                        if parent_data:
                            sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                            paired_rows += 1
                        else:
                            sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)

            if row_counter % 100000 == 0:
                print("Total row read: {}, Paired rows: {}. Time: {}".format(row_counter, paired_rows,str(datetime.now())))