import pytest
import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from web自动化.operation import Operation, drive
from web自动化.data import Data, get_data

import time



@pytest.fixture(scope='class')
def conn_sql(request):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           database='finance')
    cursor = conn.cursor()
    request.cls.conn = conn
    request.cls.cursor = cursor

    yield

    cursor.close()
    conn.close()


@pytest.mark.usefixtures("conn_sql")
class TestCase(Operation):

    def ASSERT_RESULT(self, result, expect):
        if result == expect:
            print('success')
        else:
            print('failed')

        assert result == expect


    # deplicate ##################### @pytest.mark.parametrize("get_data", ["登录"], indirect=True)
    # @pytest.mark.parametrize("user, passwd, expect", get_data('登录'))
    def test_login(self, user, passwd, expect):
        # for data in Data.success:
        #     print(data)

        self.login(user, passwd)

        pytest.mark.parametrize("load_data", ["注册"], indirect=True)
        # 登录成功，会跳到系统页面
        # 登录失败，会留在登录页面
        hint_user = '/html/body/div[1]/div/div/form/div[1]/span[1]'
        hint_passwd = '/html/body/div[1]/div/div/form/div[2]/span[1]'

        result = None
        match expect:
            case '用户名不存在':
                result = self.driver.find_element(By.XPATH, hint_user).text
            case '密码错误':
                result = self.driver.find_element(By.XPATH, hint_passwd).text
            case _:
                result = self.driver.title

        if self.driver.title != '度小满理财-登录[内测版]':
            self.logout(user)

        self.ASSERT_RESULT(result, expect)


    # @pytest.mark.parametrize("user, passwd, repasswd, expect_page, expect_info", get_data('注册'))
    def test_register(self, user, passwd, repasswd, expect_page, expect_info):
        # print(user, passwd, repasswd, expect_page, expect_info)
        # if 1 == 1:
        #     return

        self.register(user, passwd, repasswd)

        hint_user = '/html/body/div[1]/div/div/form/div[1]/span[1]'
        hint_passwd = '/html/body/div[1]/div/div/form/div[2]/span[1]'
        hint_repasswd = '/html/body/div[1]/div/div/form/div[3]/span[1]'

        page = self.driver.title
        result = None
        # if page == expect_page:
        if page == '度小满理财-登录[内测版]':
            # 注册成功，检查完删除
            sql = f'select * from user where username="{user}" and password=md5("{passwd}")'
            self.cursor.execute(sql)
            has = self.cursor.fetchone()
            if has:
                result = 'ok'
            else:
                result = 'not ok'

            d_sql = f"delete from user where username='{user}' and password=md5('{passwd}');"
            self.cursor.execute(d_sql)
            self.conn.commit()      # ❗记得commit

        else:
            match expect_info:
                case '两次密码不相同' | '重复密码为空':
                    result = self.driver.find_element(By.XPATH, hint_repasswd).text
                case '密码为空':
                    result = self.driver.find_element(By.XPATH, hint_passwd).text
                case _:
                    result = self.driver.find_element(By.XPATH, hint_user).text

        self.ASSERT_RESULT(page, expect_page)
        self.ASSERT_RESULT(result, expect_info)


    @pytest.mark.parametrize("user, passwd, bankname, cardtype, cardno, expect_num_of_this_card", get_data('银行卡新增'))
    def test_bankcard_add(self, user, passwd, bankname, cardtype, cardno, expect_num_of_this_card):
        # 正常情况：新增完验证后删掉
        # 异常情况：重复新增，用 count 验证，但是怎么删掉？  可以删掉 id 比较大的那个
        self.login(user, passwd)
        # 等待按钮能按
        btn = WebDriverWait(self.driver, 1).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '个人中心'))
        )
        btn.click()
        btn = WebDriverWait(self.driver, 1).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, '银行卡管理'))
        )
        btn.click()
        # 等待页面加载
        self.driver.implicitly_wait(1)
        self.bankcard_add(bankname, cardtype, cardno)
        time.sleep(2)  # ❗必须程序强制等待才行，显示/隐式都不行
        self.logout(user)

        # 1.确定当前用户的userId
        sql_user_id = f'select id from user where username="{user}"'
        self.cursor.execute(sql_user_id)
        uid = self.cursor.fetchone()[0]  # ❗fetch返回的是一个行数据，即元组
        # 2.看 该用户在该行的这个卡 有几张
        sql = f'select count(id) from bankcard where userId=%s and cardNum=%s and cardBank=%s'
        self.cursor.execute(sql, (uid, cardno, bankname))
        result = self.cursor.fetchone()[0]
        # 3.删掉id最大的那一张，也就是刚刚新增的
        d_sql = """
        delete b1 from bankcard b1
        join (
        select max(id) as max_id from bankcard
        where userId=%s and cardNum=%s and cardBank=%s
        ) b2 on b1.id=b2.max_id
        """
        self.cursor.execute(d_sql, (uid, cardno, bankname)) # 参数化查询防止SQL注入
        self.conn.commit() #

        if result == expect_num_of_this_card:
            print('success')
        else:
            print('failed')

        self.ASSERT_RESULT(result, expect_num_of_this_card)



    def test_bankcard_rmv(self):
        pass

    def test_bankcard_modify(self):
        pass

    def test_buy_share(self):
        pass

    def test_apply_loan(self):
        pass


