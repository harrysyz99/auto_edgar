import datetime
import sqlite3
import requests
import pandas as pd
import pandas
from sqlalchemy import create_engine
import csv
import random
import time
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from threading import Timer

urls = []


def get_url():
    current_year = datetime.date.today().year
    current_quarter = (datetime.date.today().month - 1) // 3 + 1
    start_year = 2022
    years = list(range(start_year, current_year))
    quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
    history = [(y, q) for y in years for q in quarters]
    for i in range(1, current_quarter + 1):
        history.append((current_year, 'QTR%d' % i))
    urls = ['https://www.sec.gov/Archives/edgar/full-index/%d/%s/crawler.idx' % (x[0], x[1]) for x in history]
    urls.sort()
    return urls


def save_to_db():
    con = sqlite3.connect('edgar_htm_idx.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS idx')
    cur.execute('CREATE TABLE idx (conm TEXT, type TEXT, cik TEXT, date TEXT, path TEXT)')
    urls = get_url()
    for url in urls:
        lines = requests.get(url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"}).text.splitlines()
        print("Downloading from : =>      " + url)
        nameloc = lines[7].find('Company Name')
        typeloc = lines[7].find('Form Type')
        cikloc = lines[7].find('CIK')
        dateloc = lines[7].find('Date Filed')
        urlloc = lines[7].find('URL')
        records = [tuple([line[:typeloc].strip(), line[typeloc:cikloc].strip(), line[cikloc:dateloc].strip(),
                          line[dateloc:urlloc].strip(), line[urlloc:].strip()]) for line in lines[10:]]
        cur.executemany('INSERT INTO idx VALUES (?, ?, ?, ?, ?)', records)
        print(url, 'downloaded and wrote to SQLite')

    con.commit()
    con.close()

    engine = create_engine('sqlite:///edgar_htm_idx.db')
    with engine.connect() as conn, conn.begin():
        data = pandas.read_sql_table('idx', conn)
        print(data)
        # ta = pd.DataFrame([sub.split("|") for sub in  data])
        data.to_csv('data.csv', sep=",")
        # data.to_txt('edgar_htm_idx.csv')


def create_log_file():
    with open('log.csv', 'w', newline='') as log:
        logwriter = csv.writer(log)

        with open('data.csv', newline='') as infile:
            records = csv.reader(infile)

            for i, r in enumerate(records):
                if i == 0:
                    continue
                print(len(r))
                log_row = r.copy()
                print('Start fetching URL to', r[1], r[2], 'filed on', r[3], '...')
                start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                driver = webdriver.Chrome(ChromeDriverManager().install())
                #
                print("try", r[5])
                try:
                    driver.get(r[5])
                    time.sleep(3 + random.random() * 3)
                    filing_date = driver.find_element_by_xpath('//*[@id="formDiv"]/div[2]/div[1]/div[2]').text
                    period_of_report = driver.find_element_by_xpath('//*[@id="formDiv"]/div[2]/div[2]/div[2]').text
                    form_text = driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[4]/td[3]/a').text
                    form_link = driver.find_element_by_link_text(form_text).get_attribute('href')
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print('Success!', start_time, ' --> ', end_time, '\n')
                    log_row = log_row + [start_time, end_time, filing_date, period_of_report, form_link]

                except:

                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print('Error!', start_time, ' --> ', end_time, '\n', traceback.print_exc)
                    log_row = log_row + [start_time, end_time, 'ERROR!']

                driver.quit()

                logwriter.writerow(log_row)


def auto_run():
    get_url()
    save_to_db()
    create_log_file()


def test():
    print("Done")
    timer = Timer(10, test)
    timer.start()


if __name__ == "__main__":
    get_url()
    print(urls)
    # save_to_db()
    # create_log_file()
