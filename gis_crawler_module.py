import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta


class GIS_crawler():
    def __init__(self, project_name):
        self.project_name = project_name
        self.setup_method(None)

    def setup_method(self, method):
      chrome_options = Options()
      # 设置请求头
      chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
      self.driver = webdriver.Chrome(options=chrome_options)
      self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()


    def get_timestamp(self):
        timestamp_element = self.driver.find_element(By.XPATH, '//*[@id="reportSecondTitle"]')
        timestamp_text = timestamp_element.text
        timestamp = datetime.strptime(timestamp_text, "%Y年%m月%d日 %H时")
        return timestamp

    def scrape_data(self):
        header = self.driver.find_element(By.XPATH, '//*[@id="div_report"]/div/div/div/div[2]/div[1]/div/table/tbody/tr')
        header_cols = header.find_elements(By.TAG_NAME, 'td')
        column_names = [col.text for col in header_cols]

        # 使用字典来去重，保持元素的顺序
        column_names = list(dict.fromkeys(column_names))
        rows = self.driver.find_elements(By.XPATH, '//*[@id="div_report"]/div/div/div/div[2]/div[2]//tr')
        data1 = []
        data2 = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            row_data = [col.text for col in cols]
            row_data1 = row_data[:9]
            row_data2 = row_data[9:]
            data1.append(row_data1)
            data2.append(row_data2)

        data = data1 + data2

        df_data = {}
        for i in range(len(column_names)):
            column_data = []
            for row in data:
                column_data.append(row[i])
            df_data[column_names[i]] = column_data

        return df_data

    def search_and_save(self, date_hour_str):
      self.driver.find_element(By.ID, "a_search").click()
      # 暂停一段随机时间，模拟人工操作
      time.sleep(random.randint(3, 7))
      data = self.scrape_data()
      df = pd.DataFrame(data)
      df['time'] = date_hour_str

      # 创建项目子目录
      if not os.path.exists(f'data/{self.project_name}'):
        os.makedirs(f'data/{self.project_name}')

      df.to_csv(f'data/{self.project_name}/data_{date_hour_str.replace(":", "-").replace(" ", "_")}.csv', index=False,
                encoding='utf_8_sig')

    def generate_datetime_list(self, start_datetime, end_datetime):
        delta = timedelta(hours=1)
        curr_datetime = start_datetime
        datetime_list = []
        while curr_datetime <= end_datetime:
            datetime_list.append(curr_datetime)
            curr_datetime += delta
        return datetime_list

    def test_action(self, start_datetime, end_datetime):
        self.driver.get("http://113.57.190.228:8001/#!/web/Report/RiverReport")
        self.driver.switch_to.frame(0)

        datetime_list = self.generate_datetime_list(start_datetime, end_datetime)

        for curr_datetime in datetime_list:
            date_str = curr_datetime.strftime("%Y-%m-%d")
            hour_str = curr_datetime.strftime("%H")
            self.driver.find_element(By.ID, "_easyui_textbox_input3").clear()
            self.driver.find_element(By.ID, "_easyui_textbox_input3").send_keys(date_str)
            self.driver.find_element(By.ID, "_easyui_textbox_input2").clear()
            self.driver.find_element(By.ID, "_easyui_textbox_input2").send_keys(f"{hour_str}:00")
            self.search_and_save(f"{date_str} {hour_str}:00")

if __name__ == '__main__':
    # 接口1，项目名称和路径
    project_name = "my_project_2021-9-1-9-2021-10-2-8"
    crawler = GIS_crawler(project_name)
    # 接口2，设置爬取的起止时间
    start_datetime = datetime(2021, 9, 1, 9)  # 2021年9月1日9时
    end_datetime = datetime(2021, 9, 4, 6)  # 2021年9月4日6时
    # 执行爬虫
    try:
        crawler.test_action(start_datetime, end_datetime)
    finally:
        crawler.teardown_method(None)