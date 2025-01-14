"""
页面操作类：
登录，

"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope='class')
def drive(request):
    driver = webdriver.Chrome()
    driver.get('http://localhost:90')
    driver.maximize_window()

    request.cls.driver = driver

    yield

    driver.quit()


# 页面操作
@pytest.mark.usefixtures("drive")
class Operation:

    def login(self, user, passwd):
        # 输入之前先清空
        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'password').clear()

        self.driver.find_element(By.ID, 'username').send_keys(user)
        self.driver.find_element(By.ID, 'password').send_keys(passwd)
        self.driver.find_element(By.ID, 'login_btn').click()
        # 点击按钮后等 1s
        self.driver.implicitly_wait(1)

    def logout(self, user):
        avatar = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, f"{user}"))
        )
        avatar.click()
        logout = WebDriverWait(self.driver, 1).until(
            EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "退出登录"))  # 用链接，xpath总报错找不到
        )
        logout.click()

    def register(self, user, passwd, repasswd):
        if self.driver.title != '个人理财系统注册界面':
            self.driver.find_element(By.PARTIAL_LINK_TEXT, '注册').click()

        # 先清空
        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'password').clear()
        self.driver.find_element(By.ID, 'repassword').clear()

        self.driver.find_element(By.ID, 'username').send_keys(user)
        self.driver.find_element(By.ID, 'password').send_keys(passwd) # ❗空的用例，要在excel中填上 ', 否则会被解析为 None
        self.driver.find_element(By.ID, 'repassword').send_keys(repasswd)
        self.driver.find_element(By.ID, 'login_btn').click()
        # 点击按钮后等 1s
        self.driver.implicitly_wait(1)

    def bankcard_add(self, bankname, cardtype, cardno):
        v = 1 if cardtype == '借记卡' else 2
        self.driver.find_element(By.XPATH, '//button[text()="新增"]').click()
        self.driver.find_element(By.XPATH, '//input[@name="cardbank"]').send_keys(bankname)
        self.driver.find_element(By.XPATH, f'//*[@id="bankCardAddModal"]/div/div/div[2]/form/div[2]/div[1]/div/label[{v}]').click()
        self.driver.find_element(By.XPATH, '//input[@name="cardnum"]').send_keys(cardno)
        self.driver.find_element(By.XPATH, '//*[@id="bankCard_save_btn"]').click()


    def bankcard_rmv(self):
        pass

    def bankcard_modify(self):
        pass

    def buy_share(self):
        pass

    def apply_loan(self):
        pass

"""
<div class="example-box">
    <label class="lyear-radio radio-inline"> <input type="radio" name="type" value="1" checked="checked"><span>借记卡</span></label> 
    <label class="lyear-radio radio-inline"> <input type="radio" name="type" value="2"> <span>信用卡</span></label>
</div>
"""