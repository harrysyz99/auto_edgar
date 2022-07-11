import requests
import csv
import random
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

test = "0001667769"

with open('log2.csv', 'w', newline='') as log:
    logwriter = csv.writer(log)
    with open('log3.csv', newline='') as infile:
        records = csv.reader(infile)
        for r in records:
            print(r[4])
            print(len(r))
            log_row = r.copy()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # try:
            if not r:
                continue
            driver.get(r[4])
            time.sleep(3 + random.random() * 3)
            # txturl= driver.find_element_by_xpath('/html/body/pre').text
            # try:
            # txturl = driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[4]/td[3]/a').get_attribute('href')
            # txturl = driver.get(r[4])
            # end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # except:
            #     try:
            #         txturl = driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[3]/td[3]/a').get_attribute('href')
            #     except:
            #         txturl = driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a').get_attribute('href')
            openurl = driver.find_element_by_xpath('/html/body/pre').text
            # print(openurl)
            if (test in openurl):
                end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print('There is one !', start_time, ' --> ', end_time, '\n')
                log_row = log_row + [start_time, end_time, r[4]]

            else:
                end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print('Not found!', start_time, ' --> ', end_time, '\n')

            #             except:
            #                 end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #                 end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #                 print('Error!', start_time, ' --> ', end_time, '\n')
            #                 log_row = log_row + [start_time, end_time, 'ERROR!']

            # driver.quit()

            logwriter.writerow(log_row)