import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select

class AsxGameApi:
        

    def __init__(self, unm, pwd):
        self.driver = webdriver.Chrome(service=Service("C:/Users/junmu/Random Installs/chromedriver_win32/chromedriver.exe")) 
        self.driver.get("https://game.asx.com.au/game/student/school/2022-1/login")
        foundLogin = False
        while not foundLogin:
            try:
                self.driver.find_element(By.ID, 'studentLoginForm:loginId').send_keys(unm)
                foundLogin = True
            except:
                time.sleep(0.5)
        self.driver.find_element(By.ID, 'studentLoginForm:password').send_keys(pwd)
        try:
            self.driver.find_element(By.ID, 'studentLoginForm:j_idt369').send_keys(Keys.ENTER)
        except:
            self.driver.find_element(By.ID, 'studentLoginForm:j_idt370').send_keys(Keys.ENTER)
        print('logged in')
    
    
    def BuyStock(self, stock, amount, orderType, limitPrice):
        self.driver.get("https://game.asx.com.au/game/play/school/2022-1/orders/add")
        self.driver.find_element(By.XPATH, '//*[@id="buyside"]/div[2]').click()
        print('clicked buy button')    
        
        stockDropDown = Select(self.driver.find_element(By.XPATH, '//*[@id="asxCode"]'))
        stockOptions = stockDropDown.options
        for i in range(len(stockOptions)):
            if stock in stockOptions[i].text.split(' - '[0]):
                print(stockOptions[i].text)
                stockIndex = i
        stockDropDown.select_by_index(stockIndex)
        self.driver.find_element(By.ID, 'volume').send_keys(amount)
        print('Selected stock')    
        
        if orderType == 'marketLimit':
            self.driver.find_element(By.XPATH, '//*[@id="market_limit"]/div[2]').click()
        if orderType == 'limit':
            self.driver.find_element(By.XPATH, '//*[@id="limit_order"]/div[2]').click()
            time.sleep(0.1)
            self.driver.find_element(By.ID, 'price').send_keys(limitPrice)
        print('Selected order type')
        
        self.driver.find_element(By.ID, 'submitBtn').send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get_screenshot_as_file('lastOrder.png')
        print('Took screenshot as lastOrder.png')
        try:
            self.driver.find_element(By.ID, 'saveBtn').click()
        except:
            raise Exception('Submitting order failed, there are probably pending orders for the same stock')
        print('Sent order')
        
        
    def SellStock(self, stock, amount, orderType, limitPrice):
        self.driver.get("https://game.asx.com.au/game/play/school/2022-1/orders/add")
        self.driver.find_element(By.XPATH, '//*[@id="sellside"]/div[2]').click()
        print('clicked sell button')    
        
        stockDropDown = Select(self.driver.find_element(By.XPATH, '//*[@id="sellAsxCode"]'))
        stockOptions = stockDropDown.options
        for i in range(len(stockOptions)):
            if stock in stockOptions[i].text.split(' - '[0]):
                print(stockOptions[i].text)
                stockIndex = i
        stockDropDown.select_by_index(stockIndex)
        self.driver.find_element(By.ID, 'volume').send_keys(amount)
        print('Selected stock')    
        
        if orderType == 'marketLimit':
            self.driver.find_element(By.XPATH, '//*[@id="market_limit"]/div[2]').click()
        if orderType == 'limit':
            self.driver.find_element(By.XPATH, '//*[@id="limit_order"]/div[2]').click()
            time.sleep(0.1)
            self.driver.find_element(By.ID, 'price').send_keys(limitPrice)
        print('Selected order type')
        
        self.driver.find_element(By.ID, 'submitBtn').send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get_screenshot_as_file('lastOrder.png')
        print('Took screenshot as lastOrder.png')
        try:
            self.driver.find_element(By.ID, 'saveBtn').click()
        except:
            raise Exception('Submitting order failed, there are probably pending orders for the same stock')
        self.driver.find_element(By.ID, 'saveBtn').click()
        print('Sent order')
        
        
    def AccountDetails(self):
        self.driver.get("https://game.asx.com.au/game/play/school/2022-1/portfolio")
        table = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/table')
        rawdata = []
        for td in table.find_elements(By.TAG_NAME, 'td'):
            rawdata.append(td.text)
        details = {}
        
        keyChange = {
            'Cash *' : 'cash',
            'Shares *' : 'shares',
            'Total portfolio value *' : 'portfolioValue',
            'Daily change' : 'dailyChange',
            'Overall rank' : 'rank'
            }
        
        for i in range(int(len(rawdata)/2)):
            key = ''
            for j in keyChange:
                if j == rawdata[i*2]:
                    key = keyChange[j]
            details[key] = rawdata[i*2+1]
        return details
    
    
    def Holdings(self):
        self.driver.get("https://game.asx.com.au/game/play/school/2022-1/portfolio")
        table = self.driver.find_element(By.XPATH, '//*[@id="table-view"]')
        rawdata = []
        for td in table.find_elements(By.TAG_NAME, 'td'):
            rawdata.append(td.text)
        sortedData = []
        for i in range(int(len(rawdata)/9)):
            rawRow = []
            for j in range(6):
                rawRow.append(rawdata[i*9+j])
            sortedData.append(rawRow)
            
        renameColumns = [
            'code',
            'holding',
            'buyPrice',
            'lastPrice',
            'marketValue',
            'profit'
            ]
        
        holdings = []
        for i in sortedData:
            holding = {}
            for j in range(len(i)):
                holding[renameColumns[j]] = i[j]
            holdings.append(holding)
        return holdings
        
    
    def IsMarketOpen(self):
        self.driver.get("https://game.asx.com.au/game/play/school/2022-1")
        status = self.driver.find_element(By.XPATH, '//*[@id="header"]/nav/div[1]/div[1]/span/span').text
        if status == 'Market open':
            return True
        else:
            return False
        
        
    def LogOut(self):
        self.driver.quit()