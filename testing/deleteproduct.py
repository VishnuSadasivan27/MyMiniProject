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
driver.find_element("id", "your_name").send_keys("stebinbabu75@gmail.com")
time.sleep(3)
driver.find_element("id", "your_pass").send_keys("Stebin@123")
time.sleep(3)
driver.find_element("xpath", '//*[@id="signin"]').click()
time.sleep(3)
print("User Logged In")


print("Farmer Home Page ")
driver.get("http://127.0.0.1:8000/farmerhome/")
time.sleep(3)
driver.find_element("xpath","/html/body/div/div/section[2]/div/div[2]/div/a").click()
time.sleep(3)
print("entered view page")
driver.find_element("xpath","/html/body/div/div[1]/div/table/tbody/tr[1]/td[11]/a[2]/i").click()
time.sleep(3)
print("delete")
driver.find_element("xpath","/html/body/div[1]/div[2]/div/div/form/div[3]/input[2]").click()
time.sleep(3)

print("deleted")