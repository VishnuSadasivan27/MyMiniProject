from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
print("Login test case started")
options=webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches',['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("http://127.0.0.1:8000/Login/")
driver.find_element("id", "your_name").send_keys("yedhu@gmail.com")
time.sleep(3)
driver.find_element("id", "your_pass").send_keys("Yedhu@123")
time.sleep(3)
driver.find_element("xpath", '//*[@id="signin"]').click()
time.sleep(3)
print("User Logged In")



print("Boy Home Page ")
driver.get("http://127.0.0.1:8000/delivaryhome/")
time.sleep(3)
driver.find_element("xpath","/html/body/div/div/section[2]/div/div[4]/div/a").click()
time.sleep(3)
city_input = driver.find_element("id", "date")
city_input.clear()
city_input.send_keys("06/27/2000")
time.sleep(3)
city_input = driver.find_element("id", "reason")
city_input.clear()
city_input.send_keys("fever")
time.sleep(3)
driver.find_element("xpath", '/html/body/div/div/div/div/div[2]/form/div[3]/div/input').click()
time.sleep(3)
print("Applied")