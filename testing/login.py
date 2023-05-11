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
driver.find_element("id", "your_pass").send_keys("Stebin@12")
time.sleep(3)
driver.find_element("xpath", '//*[@id="signin"]').click()
time.sleep(3)
print("User Logged In")

# ***********Test Case 3 : Guest Enquiry sending from Guest Home Page. ***************
# Navigate to Studenthome and change the password
print("Farmer Home Page ")
driver.get("http://127.0.0.1:8000/farmerhome/")
time.sleep(3)
driver.find_element("link text", "stebin").click()
time.sleep(3)
driver.find_element("link text", "My Profile").click()
time.sleep(3)
print("My Profile")

driver.find_element("xpath","/html/body/div/main/section/div/div[2]/div/div/ul/li[4]/button").click()
time.sleep(3)
print("cahanging password started ")
driver.find_element("id", "currentPassword").send_keys("Stebin@12")
time.sleep(3)
driver.find_element("id", "newPassword").send_keys("Stebin@123")
time.sleep(3)
driver.find_element("id", "renewPassword").send_keys("Stebin@123")
time.sleep(3)
driver.find_element("xpath", "/html/body/div/main/section/div/div[2]/div/div/div/div[4]/form/div[4]/button").click()
time.sleep(3)
print("Password is changed")