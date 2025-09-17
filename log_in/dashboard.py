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


BASE_URL = "https://shrinkagemanagementuat.tops.co.th/"
USERNAME = "takittithat@central.co.th"
PASSWORD = "Password2025"
STORE_CODE = "004"

driver.get(BASE_URL)
wait = WebDriverWait(driver, 10)

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
time.sleep(3)
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



def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

        

        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "ใกล้หมดอายุรอบ1" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True
    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("ใกล้หมดอายุรอบ1")


def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

        

        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "ใกล้หมดอายุรอบ 2,3" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True
    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("ใกล้หมดอายุรอบ 2,3")


def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

        

        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "สินค้าเข้าใหม่" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True
    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("สินค้าเข้าใหม่")



def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )
        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "โปรโมชัน" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True
    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("โปรโมชัน")


def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

        barcode_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='กรุณากรอกรหัสผ่าน']")
# barcode_input.clear()
# barcode_input.send_keys("8003180036496")

        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "ตรวจสอบสินค้าที่ตกหล่น" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True
    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("ตรวจสอบสินค้าที่ตกหล่น")



def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

     
        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "สินค้าตั้งกอง" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True

    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("สินค้าตั้งกอง")

def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

     
        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "ค้นหาสินค้าด้วยบาร์โค้ด" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True

    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("ค้นหาสินค้าด้วยบาร์โค้ด")

def click_button(label: str, timeout: int = 6):
    try:
        # หา element ปุ่มตาม label
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//flt-semantics[@role='button' and @flt-tappable "
                f"and (contains(@aria-label, '{label}') or contains(text(), '{label}'))]"
            ))
        )

     
        driver.execute_script("""
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            arguments[0].dispatchEvent(event);
        """, button)

        # เช็คว่ามีการเปลี่ยนหน้า (ถ้ายังอยู่หน้าเดิม fallback ใช้วิธี 2)
        WebDriverWait(driver, 5).until(
            lambda d: "สินค้าเสียหาย" not in d.page_source
        )

        print(f"กดปุ่ม {label} สำเร็จ ✅")
        return True

    except Exception:
        # --- วิธีที่ 2: ActionChains fallback ---
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            print(f"กดปุ่ม {label} สำเร็จด้วย ActionChains ✅")
            return True
        except Exception:
            print(f"ไม่เจอปุ่ม {label} ❌")
            return False

# ใช้งาน
click_button("สินค้าเสียหาย")



driver.quit()