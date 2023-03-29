from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import pandas as pd
import time
from selenium.webdriver.common.by import By
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_jobs(keyword, num_pages):
    options = Options()
    options.add_argument("window-size=1920,1080")
    #Enter your chromedriver.exe path below
    chrome_path = "../chromedriver"
    # options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    driver.get("https://www.glassdoor.co.in/Job/Home/recentActivity.htm")
    time.sleep(4)

#     element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, "sc.keyword")))
# # now script will wait unit the element is present max of 30 sec
# # you can perform the operation either using the element returned in above step or normal find_element strategy
#     element.send_keys(keyword)
#     element.send_keys(Keys.ENTER)

    # driver.implicitly_wait(10)
    search_input = driver.find_element(By.ID, "sc.keyword")
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)
    # time.sleep(2)
    
    
    
    
    company_name = []
    job_title = []
    salary_est = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []
    
    
    
    #Set current page to 1
    current_page = 1     
        
        
    time.sleep(3)
    
    while current_page <= num_pages:   
        
        done = False
        while not done:

            try:
                    driver.find_element(By.XPATH, '//*[@id="MainCol"]/div[1]/div[1]/div/div/div/div').click()
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//*[@id="MainCol"]/div[1]/div[1]/div/div/div/div[2]/ul/li[2]/button').click()
                    time.sleep(2)
            except:
                print('Sorting by Recent failed!, continuing with default')
                pass

            job_cards = driver.find_elements(By.XPATH, "//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            for card in job_cards:
                card.click()
                time.sleep(1)

                #Closes the signup prompt
                try:
                    driver.find_element(By.XPATH, ".//span[@class='SVGInline modal_closeIcon']").click()
                    time.sleep(2)
                except NoSuchElementException:
                    time.sleep(2)
                    pass

                #Expands the Description section by clicking on Show More
                try:
                    # driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb2']").click()
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//*[@id="JobDescriptionContainer"]/div[2]').click()
                    time.sleep(1)
                except NoSuchElementException:
                    card.click()
                    print(str(current_page) + '#ERROR: no such element')
                    time.sleep(1)
                    driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb2']").click()
                except ElementNotInteractableException:
                    card.click()
                    driver.implicitly_wait(1)
                    print(str(current_page) + '#ERROR: not interactable')
                    driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb2']").click()

                #Scrape 

                try:
                    company_name.append(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/div').text)
                except:
                    company_name.append(None)
                    pass

                try:
                    job_title.append(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text)
                except:
                    job_title.append(None)
                    pass

                try:
                    location.append(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]').text)
                except:
                    location.append(None)
                    pass

                try:
                    job_description.append(driver.find_element(By.XPATH, "//div[@id='JobDescriptionContainer']").text)
                except:
                    job_description.append(None)
                    pass

                try:
                    salary_estimate.append(driver.find_element(By.XPATH, '//*[@id="JDCol"]/div/article/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]').text)
                except:
                    salary_estimate.append(None)
                    pass
                
                try:
                    company_size.append(driver.find_element(By.XPATH, '//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text)
                except:
                    company_size.append(None)
                    pass
                
                try:
                    company_type.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                except:
                    company_type.append(None)
                    pass
                    
                try:
                    company_sector.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                except:
                    company_sector.append(None)
                    pass
                    
                try:
                    company_industry.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                except:
                    company_industry.append(None)
                    pass
                    
                try:
                    company_founded.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                except:
                    company_founded.append(None)
                    pass
                    
                try:
                    company_revenue.append(driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                except:
                    company_revenue.append(None)
                    pass
                    
                    
                    
                    
                done = True
                
       # Moves to the next page         
        if done:
            print(str(current_page) + ' ' + 'out of' +' '+ str(num_pages) + ' ' + 'pages done')
            driver.find_element(By.XPATH, "//span[@alt='next-icon']").click()   
            current_page = current_page + 1
            time.sleep(4)
            




    driver.close()
    df = pd.DataFrame({'company': company_name, 
    'job title': job_title,
    'location': location,
    'job description': job_description,
    'salary estimate': salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry, 'company_founded' : company_founded, 'company_revenue': company_revenue})
    
    return df

data = fetch_jobs("Data Scientist", 1)


data.to_csv('data/' + 'data.csv')