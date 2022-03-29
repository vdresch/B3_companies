###################        Librarys        #########################

from datetime import datetime
import pandas as pd
from selenium                      import webdriver
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support    import expected_conditions as EC
from selenium.common.exceptions    import TimeoutException
import sys
import time


###############       Headers, link and path        ################


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#!!! CHANGE THE PATH FOR THE WEBDRIVER HERE!!!#
PATH_WEBDRIVER = '/Users/vitordresch/Documents/Git/B3_tickers/chromedriver'

LINK = 'https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm'


#####################       Functions        #########################

def read_tickers(driver, tickers):

    blocks = driver.find_elements_by_xpath('//*[@id="nav-bloco"]/div/div')


    for i in blocks:
        tickers = tickers.append([i.text.splitlines()])

    return tickers


def next_pag(driver):
    driver.execute_script("window.scrollTo(0, 9000)")

    time.sleep(3) 

    driver.execute_script("window.scrollTo(0, 9000)") 

    driver.find_element_by_xpath('//*[@id="listing_pagination"]/pagination-template/ul/li[10]/a').click()


#####################       main        #########################


if __name__ == '__main__':

    #Try to open Chrome webdriver
    try:
        driver  = webdriver.Chrome(executable_path = PATH_WEBDRIVER)    
    except:
        print('Error opening webdriver')
        sys.exit(1)

    #Open the page
    driver.get(LINK) 

    timeout = 10

    #Get cookies out of the way
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"onetrust-accept-btn-handler\"]")))
    except TimeoutException:
        print('timeoutou')

    driver.find_element(By.XPATH, '//*[@id=\"onetrust-accept-btn-handler\"]').click()

    #Wait until 'Todos' appear and click in it
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"bvmf_iframe\"]")))
    except TimeoutException:
        print('timeoutou')
    driver.execute_script("window.scrollTo(0, 250)") 
    driver.switch_to.frame(driver.find_element_by_xpath("//*[@id=\"bvmf_iframe\"]"))
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Todos"]')))
    except TimeoutException:
        print('timeoutou')
    driver.find_element(By.XPATH, '//button[text()="Todos"]').click()

    print('Page 1')

    #Wait until you can select to show 120 ticker by page
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="selectPage"]')))
    except TimeoutException:
        print('timeoutou')
    Select(driver.find_element_by_xpath('//*[@id="selectPage"]')).select_by_visible_text('120')

    time.sleep(3)

    #Create dataframe to store the tickers
    tickers = pd.DataFrame()

    #Get the first tickers
    tickers = read_tickers(driver, tickers)

    #While there are pages, keeps scraping
    pg = 2

    while True:
        try:

            next_pag(driver)

            print('Page ', pg)

            time.sleep(3)

            tickers = read_tickers(driver, tickers)

            pg += 1

        except:
            print("Last page done")
            break


    
    #Exit driver

    driver.quit()
    
    #Clean and save the data

    print("Saving data")

    tickers = tickers.rename(columns={0:'Code', 1:'Nome', 2:'Nome fantasia', 3:'Governança'})
    tickers['Governança'] = tickers['Governança'].fillna('-')

    name = 'B3_companies_' + datetime.today().strftime('%Y-%m-%d') + '.csv'

    tickers.to_csv(name, index=False)
