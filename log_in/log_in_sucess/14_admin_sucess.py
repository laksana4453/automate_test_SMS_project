from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

STORE_CODE = "009"
wait = WebDriverWait(driver, 10)

driver.get("https://shrinkagemanagementuat.tops.co.th/")
time.sleep(6)  

username_input = driver.find_element(By.CSS_SELECTOR, 'textarea[data-semantics-role="text-field"]')
username_input.send_keys("takittithat@central.co.th")
password_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='กรุณากรอกรหัสผ่าน']")
password_input.send_keys("Password2025")
time.sleep(6) 

login_button = driver.find_element(By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]")
login_button.click()
time.sleep(6)  



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
        print(f"เลือกสาขา {code} สำเร็จ ✅")

        return True
    
    except TimeoutException:
        return False

# ---------- ถ้าเลือกสาขาได้ → ไปหน้าแรก ----------
if select_store(STORE_CODE, timeout=15):
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
