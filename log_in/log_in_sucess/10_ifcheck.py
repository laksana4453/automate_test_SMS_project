from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



driver.get("https://shrinkagemanagementuat.tops.co.th/")
time.sleep(6)  

username_input = driver.find_element(By.CSS_SELECTOR, 'textarea[data-semantics-role="text-field"]')
username_input.send_keys("chArin@tops.co.th")
password_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='กรุณากรอกรหัสผ่าน']")
password_input.send_keys("Password2025")
time.sleep(6) 

login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]")
login_button.click()
time.sleep(6)  