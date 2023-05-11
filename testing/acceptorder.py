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
driver.find_element("xpath","/html/body/div/div/section[2]/div/div[3]/div/a").click()
time.sleep(3)

print("entered view page")
city_input = driver.find_element("xpath","/html/body/div/div/div/table/tbody/tr/td[9]/input")
city_input.send_keys("790198")
time.sleep(3)
print("deliver")
driver.find_element("xpath","/html/body/div/div/div/table/tbody/tr/td[10]/a/div").click()
time.sleep(3)
print("deliverredddd")