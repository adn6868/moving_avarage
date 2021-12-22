import mysql.connector
import json
from datetime import datetime
from util import from_timestamp_to_sql_format
from db_config import db_config

mydb = mysql.connector.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database'],
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()
symbol_list = ['VPB', 'VNM', 'VJC', 'VIC', 'VHM', 'VCB', 'TPB', 'TCH', 'TCB', 'STB', 'SSI', 'SBT', 'REE', 'POW',
               'PNJ', 'PLX', 'PDR', 'NVL', 'MWG', 'MSN', 'MBB', 'KDH', 'HPG', 'HDB', 'GAS', 'FPT', 'CTG', 'BVH', 'BID']
for symbol in symbol_list:
    with open('/Users/ducanhnguyen/Developer/moving_avarage/dat/%s/%s_five_year.json' % (symbol, symbol)) as json_file:
        data = json.load(json_file)
        if data['s'] != 'ok':
            print('fail to load data')
        length = len(data['t'])
        sql_query = "INSERT INTO tblMarket (SYMBOL, TIME, OPEN, HIGH, LOW, CLOSE, VOLUME) VALUES (%s, %s, %s, %s, %s ,%s ,%s)"
        for i in range(length):
            val = (symbol, from_timestamp_to_sql_format(
                data['t'][i]), data['o'][i], data['h'][i], data['l'][i], data['c'][i], data['v'][i])
            mycursor.execute(sql_query, val)
        mydb.commit()
    print("record for %s inserted" % symbol)

# print(mycursor.rowcount, "record inserted.")
