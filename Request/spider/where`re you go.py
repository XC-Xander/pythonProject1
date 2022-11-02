# -*- codeing =utf-8 -*-
# author:XC
# @Time :2022/10/24 16:01
# @File :where`re you go.py
# @Software: PyCharm

'phantomjs的用处是需要完整使用js代码时，用无头浏览器模拟真实运行环境'
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

class get_spider():
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.driver.get('https://flights.ctrip.com/online/channel/domestic')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def Elements(self):
        #查找元素
        from_place=self.driver.find_element(By.XPATH,r"//div/input[@name='owDCity']")
        to_place=self.driver.find_element(By.XPATH,r"//div/input[@name='owACity']")
        button=self.driver.find_element(By.XPATH,r'//button[@class="search-btn"]')
        from_date=self.driver.find_element(By.XPATH,r'//input[@aria-label="请选择日期"]')
        to_date=self.driver.find_elements(By.XPATH,r"//div/input[@aria-label='请选择日期']")[1]
        #动作操作
        js="arguments[0].value ='';"
        from_place.click()
        time.sleep(2)
        self.driver.execute_script(js,from_place)
        from_place.send_keys("衡阳(HNY)")


        to_place.click()
        time.sleep(2)
        self.driver.execute_script(js,to_place)
        to_place.send_keys("上海(SHA)")


        js_time = "arguments[0].removeAttribute('readOnly');arguments[0].value=arguments[1];"
        from_date.click()
        time.sleep(2)
        self.driver.execute_script(js_time,from_date,"2022-11-1")
        to_date.click()
        time.sleep(2)
        self.driver.execute_script(js_time,to_date,"2022-11-5")

        time.sleep(2)
        self.driver.execute_script("arguments[0].click();",button)
        alert=self.driver.find_element(By.XPATH,r"//div[@class='btn-group']")
        alert.click()
        time.sleep(2)

        #获取页面内容
        while True:
            try:
                WebDriverWait(self.driver,10).until(\
                    EC.title_contains(to_place)\
                    )
            except Exception as e:
                print(e)
                break
            time.sleep(5)

        js="window.scrollTo(0,document.body.scrollHeight);"
        self.driver.execute_script(js)
        time.sleep(5)
        htm_const=self.driver.page_source
        return htm_const

    def parser_html(self):
        html=self.Elements()
        text=etree.HTML(html)
        airplane_cm=text.xpath(r'//span[@id="airlineName9C6476_16667484000009C6475_1666996800000-0"]/text()')[0]
        date=text.xpath(r'//div[@index="0"]/descendant::*[@class="time"]/text()')
        place=text.xpath(r'//div[@index="0"]/descendant::*[@class="airport"]/span[last()-1]/text()')
        dic={'from_date':date[0],'to_date':date[1],'from_place':place[0],'to_place':place[1],'airplane_cm':airplane_cm}
        print(dic)

if __name__ =='__main__':
    a=get_spider()
    a.parser_html()