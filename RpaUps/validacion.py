from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

driver = webdriver.Remote(
'http://localhost:4444/wd/hub',
   desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
)

driver.get("https://www.w3schools.com/html/default.asp")
time.sleep(5)
all_cookies = driver.get_cookies()
print(all_cookies)
