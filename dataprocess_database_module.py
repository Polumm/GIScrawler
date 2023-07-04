import os
import pandas as pd
import mysql.connector

# 创建MySQL连接
mydb = mysql.connector.connect(
  host="localhost",
  user="sa",
  password="11811918da"
)

# 创建数据库
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS water_project")

# 创建表
mycursor.execute("USE water_project")
mycursor.execute("""
CREATE TABLE IF NOT EXISTS water_data(
  river_name VARCHAR(255),
  station_name VARCHAR(255),
  water_level FLOAT,
  daily_change FLOAT,
  flow_rate VARCHAR(255),
  defense_level FLOAT,
  alert_level FLOAT,
  ensure_level FLOAT,
  time DATETIME)
""")

# 读取和处理指定目录下的CSV文件，然后写入数据库
project_path = 'data\my_project_2021-9-1-9-2021-10-2-8'
csv_files = os.listdir(project_path)

for csv_file in csv_files:
    if csv_file.endswith('.csv'):
        df = pd.read_csv(os.path.join(project_path, csv_file))
        # 将所有的'--'和空值填补为0
        df = df.replace('--', 0)
        df = df.fillna(0)
        # 原网页水势列意义不明，故删除"水势"这一列
        df = df.drop(['水势'], axis=1)
        # 填补河名的空缺值
        df['河名'].fillna(method='ffill', inplace=True)

        # 将DataFrame写入MySQL
        for i, row in df.iterrows():
            sql = "INSERT INTO water_data (river_name, station_name, water_level, daily_change, flow_rate, defense_level, alert_level, ensure_level, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # val = (row['河名'], row['站名'], row['水位'], row['比昨日\n+涨-落'], row['流量'], row['设防\n水位'], row['警戒\n水位'], row['保证\n水位'], row['time'])
            # 使用iloc即采用数字索引，比使用字符串索引更加安全
            val = (row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3], row.iloc[4], row.iloc[5], row.iloc[6], row.iloc[7],row.iloc[8])
            mycursor.execute(sql, val)

        mydb.commit()
