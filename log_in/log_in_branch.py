from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


BASE_URL = "https://shrinkagemanagementuat.tops.co.th/"
USERNAME = "takittithat@central.co.th"
PASSWORD = "Password2025"
STORE_CODE = "009"

driver.get(BASE_URL)
wait = WebDriverWait(driver, 50)

# Login
username_input = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea[data-semantics-role="text-field"]'))
)
username_input.clear()
username_input.send_keys(USERNAME)

password_input = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='กรุณากรอกรหัสผ่าน']"))
)
password_input.clear()
password_input.send_keys(PASSWORD)

login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]"))
)
login_button.click()

# Try selecting store
def select_store(code: str, timeout: int = 20) -> bool:
    try:
        store_item = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//flt-semantics[@role="radio" and contains(@aria-label, "{code}")]')
            )
        )
        # scroll ให้เห็นก่อน
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", store_item)

        # คลิกสาขา
        driver.execute_script("arguments[0].click();", store_item)
        time.sleep(3)  
        print(f"เลือกสาขา {code} สำเร็จ")

        return True
    
    except TimeoutException:
        return False

# ---------- ถ้าเลือกสาขาได้ → ไปหน้าแรก ----------
if select_store(STORE_CODE, timeout=25):
    try:
        home_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[contains(text(), "ไปยังหน้าแรก")]') 
            )
        )
    
        driver.execute_script("arguments[0].click();", home_button)
        time.sleep(6)  
        print("เข้าสู่หน้าแรกสำเร็จ ✅")

    except TimeoutException:
        print("เลือกสาขาได้ แต่ไม่เจอปุ่ม 'ไปยังหน้าแรก'")
else:
    try:
        retry_login_btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]"))
        )
        retry_login_btn.click()
        print("ไม่เจอสาขา → กดปุ่มเข้าสู่ระบบแทน")
    except TimeoutException:
        print("ไม่พบทั้งสาขาและปุ่มเข้าสู่ระบบ")

driver.quit()
