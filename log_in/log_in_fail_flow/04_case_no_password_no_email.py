
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options

#----- 04 กรณี user ไม่กรอก อีเมล และรหัสผ่าน ขึ้นแจ้ง "กรุณากรอกข้อมูล"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://shrinkagemanagementuat.tops.co.th/")

wait = WebDriverWait(driver, 20)

time.sleep(6)

# กดปุ่มเข้าสู่ระบบ
login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]")
login_button.click()

element = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//span[contains(text(),'กรุณากรอกข้อมูล')]")
    )
)
print("===>> พบข้อความ กรุณากรอกข้อมูล หรือไม่?:", element.is_displayed())
assert element.is_displayed()
