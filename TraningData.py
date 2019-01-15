import sqlite3
import pandas as pd

timeframes = ['2018-05']

for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    cursor = connection.cursor()
    limit = 5000
    last_unix = 0
    cur_length = limit
    counter = 0
    test_done2012 = False
    test_done2013 = False

    while cur_length == limit:

        datafile = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} and parent NOT NULL and score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix,limit),connection)
        last_unix = datafile.tail(1)['unix'].values[0]
        cur_length = len(datafile)

        if not test_done2013:
            with open('tst2013.from','a', encoding='utf8') as file:
                for content in datafile['parent'].values:
                    file.write(content+'\n')

            with open('tst2013.to','a', encoding='utf8') as file:
                for content in datafile['comment'].values:
                    file.write(str(content)+'\n')
 
            test_done2013 = True

        if not test_done2012:
            with open('tst2012.from','a', encoding='utf8') as file:
                for content in datafile['parent'].values:
                    file.write(content+'\n')

            with open('tst2012.to','a', encoding='utf8') as file:
                for content in datafile['comment'].values:
                    file.write(str(content)+'\n')
 
            test_done2012 = True

        else:
            with open('train.from','a', encoding='utf8') as file:
                for content in datafile['parent'].values:
                    file.write(content+'\n')

            with open('train.to','a', encoding='utf8') as file:
                for content in datafile['comment'].values:
                    file.write(str(content)+'\n')

        counter += 1
        if counter % 20 == 0:
            print(counter*limit,'rows completed so far')
    print("you re good to go!")