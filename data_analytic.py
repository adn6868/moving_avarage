import mysql.connector 
from db_config import db_config
db = mysql.connector.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database'],
    auth_plugin='mysql_native_password'
)

cursor = db.cursor()
query = "select * from tblMarket where SYMBOL = 'VNM'"
cursor.execute(query)

result = cursor.fetchall()

