
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
#-----02  กรณี login แต่ไม่ได้เชื่อมต่อ internet

options = Options()
# options.add_argument("--headless=new")  # ถ้าต้องการ headless
service = Service(ChromeDriverManager().install())  # ตั้งค่า chromedriver ที่ดาวน์โหลดไว้

driver = webdriver.Chrome(service=service, options=options)


# ตอนนี้เบราเซอร์จะทำงานเหมือนไม่มีเน็ต
driver.get("https://shrinkagemanagementuat.tops.co.th/")  # จะโหลดไม่ออก หรือแสดง cached content ถ้ามี
wait = WebDriverWait(driver, 20)


# กรอกอีเมล
username_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[data-semantics-role="text-field"]'))
)
username_input.send_keys("PaOrnploy@central.co.th")

# กรอกรหัสผ่าน
password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
password_input.send_keys("12345678")
time.sleep(6)


# เปิด Network domain
driver.execute_cdp_cmd("Network.enable", {})

# ตั้งให้เป็น offline
driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
    "offline": True,
    "latency": 0,               # ms
    "downloadThroughput": 0,   # bytes/s
    "uploadThroughput": 0      # bytes/s
})
time.sleep(10)
# กดปุ่มเข้าสู่ระบบ
login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]")
login_button.click()
element = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[contains(normalize-space(.), 'พบข้อผิดพลาดของเครือข่าย โปรดตรวจสอบเครือข่ายอีกครั้ง')]")
    )
)
print("===>> พบข้อความผิดพลาดหรือไม่?:", element.is_displayed())
assert element.is_displayed()

driver.quit()