import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 创建数据库连接
mydb = mysql.connector.connect(
  host="localhost",
  user="sa",
  password="11811918da",
  database="water_project"
)

mycursor = mydb.cursor()

# 执行SQL查询，获取三峡水库的水位数据
mycursor.execute("SELECT DATE(time) as date, avg(flow_rate) FROM water_data WHERE station_name='三峡水库' AND water_level!=0 GROUP BY DATE(time)")
results = mycursor.fetchall()

# 将数据转换为pandas DataFrame
df = pd.DataFrame(results, columns=["date", "avg_water_level"])
# 设置date为index
df.set_index('date', inplace=True)
# 创建一个新的figure，并设定大小
fig, ax = plt.subplots(figsize=(10, 5))

# 使用DayLocator和DateFormatter格式化x轴
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 自动格式化x轴的日期标签以避免它们重叠
fig.autofmt_xdate()

# 绘制折线图
ax.plot(df.index, df["avg_water_level"])
ax.set_title('三峡水库日均流量变化')
ax.set_xlabel('日期')
ax.set_ylabel('流量均值')
plt.savefig('三峡水库日均流量变化.svg')
plt.show()
