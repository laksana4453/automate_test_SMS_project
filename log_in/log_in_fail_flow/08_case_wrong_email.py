
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options

# 08 ตรวจสอบการแจ้งเตือน กรณีเข้าสู่ระบบโดยกรอกอีเมลที่ไม่มีข้อมูลอยู่บนระบบ CneXt


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://shrinkagemanagementuat.tops.co.th/")

wait = WebDriverWait(driver, 20)

time.sleep(6)
username_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[data-semantics-role="text-field"]'))
)
username_input.send_keys("Kawinna.g@gmail.com")

# กรอกรหัสผ่าน
password_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
)

password_input.send_keys("xxxxxxxxxx")

time.sleep(3)

# กดปุ่มเข้าสู่ระบบ
login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]")
login_button.click()

element = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[contains(normalize-space(.), 'อีเมลหรือรหัสผ่านไม่ถูกต้อง')]")
    )
)

print("===>> พบข้อความผิดพลาดหรือไม่?:", element.is_displayed())
assert element.is_displayed()

driver.quit()