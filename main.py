from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import os
import pandas as pd
import numpy as np
import time
import datetime

CHROMEDRIVER_PATH = r"D:\softwares\chromedriver.exe"
WINDOW_SIZE = "1920,1080"
chrome_options = Options()

chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')

service = Service(CHROMEDRIVER_PATH)


def main():
    dff = pd.DataFrame(columns=['Job Title', 'Description', 'Experience Reqd', 'Company', 'City', 'Salary Range',
                                'Date Posted', 'URL'])

    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Hyderabad%2F+Secunderabad%2C%22Graduate+Trainee%22%2CFresher%2CFresher%2C%22Computer+Science%22&txtKeywords=%22Graduate+Trainee%22%2CFresher%2C%22Computer+Science%22&txtLocation=Hyderabad%2F+Secunderabad&cboWorkExp1=0'
    driver.get(url)

    time.sleep(10)

    try:
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
    except Exception as e:
        print('EXCEPTION OCCURRED')
        pass

    page_counter = 0

    max_pages = 10

    exception = 0

    while page_counter < max_pages:

        if page_counter == 0:
            next_counter = 0
        else:
            next_counter = 1

        page_next_counter = np.arange(2, 12)

        for page_next in page_next_counter:

            try:
                driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
            except Exception as e:
                print('EXCEPTION OCCURRED \n  x not present in the screen \n')
                pass

            soup = BeautifulSoup(driver.page_source, 'lxml')

            try:
                driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
            except Exception as e:
                print('EXCEPTION OCCURRED \n  x not present in the screen \n')
                pass
            try:
                driver.find_element(By.XPATH, '//*[@id="closeSpanId"]').click()
            except Exception as e:
                print('EXCEPTION OCCURRED \n  x ver 2 not present in the screen \n')
                pass

            result = soup.find('ul', class_='new-joblist')

            if result is not None:
                result2 = result.find_all('li', class_='clearfix job-bx wht-shd-bx')

                if result2:
                    for i in result2:
                        title = i.find('a')
                        title = title.text.strip()

                        description = i.find('label').next_sibling.strip()

                        text = i.find('h3', class_='joblist-comp-name')
                        text = text.text
                        initial_company = text.find('(')
                        Company = text[:initial_company]
                        Company = Company.strip()

                        Mat_icons = i.find_all('i', class_='material-icons')
                        Exp = Mat_icons[0].next_sibling.text.strip()

                        spans = i.find_all('span')
                        City = spans[1].text

                        Date = i.find('span', class_='sim-posted')
                        Date = Date.text.strip()

                        URL = i.find('a').get('href')

                        try:
                            Salary = i.find('i', class_="material-icons rupee").next_sibling
                        except Exception as e:
                            print("EXCEPTION OCCURRED AT SALARY")
                            exception = exception + 1
                            Salary = 'Not Mentioned'

                        dff = pd.concat(
                            [dff, pd.DataFrame([[title, description, Exp, Company, City, Salary, Date, URL]],
                                               columns=['Job Title', 'Description', 'Experience Reqd', 'Company',
                                                        'City', 'Salary Range', 'Date Posted', 'URL'])],
                            ignore_index=True)

                    print(dff)

                    dff.to_excel(
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data',
                                     "TimesJobs_scraped_data" + ".xlsx"), index=False)

                    driver.execute_script("window.scrollTo(0,(document.body.scrollHeight))")

                    scroll_time = 2
                    time.sleep(scroll_time)

                    dff.to_excel(
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data',
                                     "TimesJobs_" + str(datetime.date.today()) + ".xlsx"), index=False)

                    page_counter = page_counter + 1

                    final_page_next = next_counter + page_next
                    try:
                        driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div[4]/section/div[2]/div[2]/div[4]/em[' + str(
                                                final_page_next) + ']/a').click()
                    except Exception as e:
                        print('EXCEPTION OCCURRED (UNABLE TO FIND THE BUTTON)\n', e,
                              '\n********** KINDLY LOOK AFTER IT **********')

                    loading_time = 1
                    time.sleep(loading_time)

                    print('NUMBER OF EXCEPTIONS: ', exception)

                else:
                    print("No job list items found on the page.")
            else:
                print("No 'ul' element with class 'new-joblist' found on the page.")


main()

