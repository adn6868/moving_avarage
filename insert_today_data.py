import mysql.connector
import requests
import json
from datetime import date, datetime
from stonk_crawler import URL_BUILDER
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


start_time = datetime.now().replace(hour=8, minute=0)
end_time = datetime.now().replace(hour=16, minute=0)
vn30 = open('vn30.input', 'r')
symbol_list = []
for line in vn30:
    symbol_list.append(line.strip('\n'))
    # symbol_list = ['NRE' , 'VPB' , 'VNM' , 'VJC' , 'VIC' , 'VHM' , 'VCB' , 'TPB' , 'TCH' , 'TCB' , 'STB' , 'SSI' , 'SBT' , 'REE' , 'POW' , 'PNJ' , 'PLX' , 'PDR' , 'NVL' , 'MWG' , 'MSN' , 'MBB' , 'KDH' , 'HPG' , 'HDB' , 'GAS' , 'FPT' , 'CTG' , 'BVH' , 'BID']
# symbol_list = ['VNM']
for symbol in symbol_list:
    url_builder = URL_BUILDER(symbol, start_time, end_time)
    r = requests.get(url_builder.get_URL())
    data = r.json()
    if data['s'] == 'ok':
        length = len(data['t'])
        sql_query = "INSERT INTO tblMarket (SYMBOL, TIME, OPEN, HIGH, LOW, CLOSE, VOLUME) VALUES (%s, %s, %s, %s, %s ,%s ,%s)"
        for i in range(length):
            val = (symbol, from_timestamp_to_sql_format(
                data['t'][i]), data['o'][i], data['h'][i], data['l'][i], data['c'][i], data['v'][i])
            try:
                mycursor.execute(sql_query, val)
                mydb.commit()
                print("record for %s inserted" % symbol)
            except mysql.connector.errors.IntegrityError as e:
                print("Unable to insert data with error")
                print(e)
