import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import json
import requests
import pause
from enum import Enum
from datetime import datetime
import schedule

f = open('volleyball.json')
data = json.load(f)
import threading

class Center(Enum):
    SHAW = '1'
    FSC = '2'
    HALL = '51'
    BLKX = '103'

class Activity(Enum):
    Volleyball = '6'
    Badminton = '2'
    Fitness = '101'


class Poss:
    def __init__(self, username, password, timeslot):
        self.playTime = data['play_date']
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10000)
        self.username = username
        self.password = password
        self.isDevelop = data['develop']
        self.center = data['center']
        self.timeslot = timeslot
        self.Booked = False
        self.booktime = data['book_time']

    def checkBalance(self):
        a = self.driver.find_element(By.CSS_SELECTOR,value = 'body > main > section > div:nth-child(3) > div:nth-child(1) > span')
        print(a.text, self.username)


    def gotoPolyPoss(self):
        self.driver.get('https://www40.polyu.edu.hk/poss/secure/login/loginhome.do')
        self.driver.find_element(By.CSS_SELECTOR, value='#loginform > div.input > table > tbody > tr > td:nth-child(1) > input.id').send_keys(self.username)
        self.driver.find_element(By.CSS_SELECTOR, value='#loginform > div.input > table > tbody > tr > td:nth-child(1) > input.pw').send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, value='#loginform > div.input > table > tbody > tr > td:nth-child(2) > button').click()
        self.wait.until(EC.visibility_of(self.driver.find_element(By.CSS_SELECTOR, value='body > header > div > div > form > a')))
        self.driver.get('https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book.do')
        time.sleep(1)
        self.wait.until(EC.visibility_of(self.driver.find_element(By.CSS_SELECTOR, value='div.dataset-wrap:nth-child(1) > a:nth-child(1)')))
        self.driver.find_element(By.CSS_SELECTOR, value='div.dataset-wrap:nth-child(1) > a:nth-child(1)').click()

    def selectActivity(self,activity):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#actvId')))
        select_activity = self.driver.find_element(By.CSS_SELECTOR,'#actvId')
        select_object_activity = Select(select_activity)
        select_object_activity.select_by_value(activity.value) 

    def selectCenter(self,center):
        select_center = self.driver.find_element(By.CSS_SELECTOR,'#ctrId')
        select_object_center = Select(select_center)
        select_object_center.select_by_value(center.value)

    def selectDate(self,date):
        input = self.driver.find_element(By.CSS_SELECTOR,'#searchDate')
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", input)
        self.driver.find_element(By.CSS_SELECTOR,'#searchDate').clear()
        self.driver.find_element(By.CSS_SELECTOR,'#searchDate').send_keys(date)

    def waitTimeTableLoaded(self):
        self.driver.find_element(By.CSS_SELECTOR,'#searchButton').click()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#timetable-container')))


    def selectTimeSlot(self,startTime):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,('[data-slot-start-time="{time}"]').format(time=startTime))))
        self.timeslot = self.driver.find_element(By.CSS_SELECTOR,('[data-slot-start-time="{time}"]').format(time=startTime))
        # print(self.timeslot.get_attribute('data-selected'))
        while self.timeslot.get_attribute('data-selected') == 'false' or self.timeslot.get_attribute('data-selected') == None:
            self.timeslot.click()
        nextBtn = self.driver.find_element(By.CSS_SELECTOR, '#nextButton')
        while nextBtn.get_attribute('disabled') == None:
            nextBtn.click()
            if(self.driver.current_url == 'https://www40.polyu.edu.hk/starspossfbstud/secure/ui_make_book/make_book_submit.do'):
                break

    def predict(self,base64_encoded):
        data = {
            "signature_name": "serving_default",
            "inputs": 
                {
                "input": {"b64": base64_encoded.decode('utf-8')}
                }
        }

        header={
            "content-type": "application/json",
            "cache-control": "no-cache"
        }

        r = requests.post('http://localhost:8501/v1/models/exported_model:predict',
        headers=header,
        json=data)
        r = r.json()
        return r['outputs']['output']
        #convert image to base64

    def getCaptchaImage_base64(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#validBookCaptcha_CaptchaImage')))
        image = self.driver.find_element(By.CSS_SELECTOR, '#validBookCaptcha_CaptchaImage').screenshot_as_png
        base64_encoded = base64.b64encode(image)
    
        return base64_encoded

    def inputCaptcha(self,result):
        self.driver.find_element(By.CSS_SELECTOR, value='#captchaCode').clear()
        self.driver.find_element(By.CSS_SELECTOR, value='#captchaCode').send_keys(result)

    def refreshCaptcha(self):
        self.driver.find_element(By.CSS_SELECTOR, value='#refreshCaptcha').click()

    def downloadImage(self):
        with open('logo.png','wb') as file:
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#validBookCaptcha_CaptchaImage')))
            image = self.driver.find_element(By.CSS_SELECTOR, '#validBookCaptcha_CaptchaImage').screenshot_as_png
            file.write(image)


    def checkbox(self):
        # self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#declare')))
        if self.driver.find_element(By.CSS_SELECTOR,'#declare'):
            self.driver.find_element(By.CSS_SELECTOR,'#declare').click()

    def submit(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#saveButton'))).click()
        time.sleep(1)
        if(self.driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger')):
            return False
        else:
            return True

    def start(self):
        self.gotoPolyPoss()
        if self.isDevelop:
            self.selectActivity(Activity.Fitness)
            self.selectDate(self.playTime)
            self.selectCenter(Center.SHAW)
        else:
            self.checkBalance()
            self.selectActivity(Activity.Volleyball)
            self.selectDate(self.playTime)
            self.selectCenter(Center[self.center])

        self.waitTimeTableLoaded()
        
        self.selectTimeSlot(self.timeslot)
        while self.Booked == False:
            image = self.getCaptchaImage_base64()
            predict_result = self.predict(image)
            self.inputCaptcha(predict_result)
            self.checkbox()
            datetime_object = datetime.strptime(self.booktime, '%Y-%m-%d %H:%M:%S').timestamp()
            pause.until(datetime_object) 
            self.Booked = self.submit()
            print(self.Booked)


def ThreadStart():
    try:
        account1 = Poss(data['account'][0]['username'], data['account'][0]['password'], data['account'][0]['start_time'] )
        account2 = Poss(data['account'][1]['username'], data['account'][1]['password'],data['account'][1]['start_time'] )
        account3 = Poss(data['account'][2]['username'], data['account'][2]['password'],data['account'][2]['start_time'] )
        # account4 = Poss(data['account'][3]['username'], data['account'][3]['password'],data['account'][3]['start_time'] )

        threading.Thread(target=account1.start).start()
        threading.Thread(target=account2.start).start()
        threading.Thread(target=account3.start).start()
        # threading.Thread(target=account4.start).start()
    except Exception as e:
        print(e)
schedule.every().day.at("08:26:00").do(ThreadStart)
# schedule.every().day.at("17:10:10").do(ThreadStart)
while True:
    schedule.run_pending()
    time.sleep(1)

# ThreadStart()