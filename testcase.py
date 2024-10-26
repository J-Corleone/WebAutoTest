import pytest
import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By

from web自动化.operation import Operation, drive
from web自动化.data import Data, get_data


@pytest.fixture(scope='class')
def conn_sql(request):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='root',
                           database='finance')
    cursor = conn.cursor()
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


    # @pytest.mark.parametrize("get_data", ["登录"], indirect=True)
    @pytest.mark.parametrize("user, passwd, expect", get_data('登录'))
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


    # @pytest.mark.parametrize("user, passwd, repasswd, expect_page, expect_info", Data.success)
    # def test_register(self, user, passwd, repasswd, expect_page, expect_info):
    #     self.register(user, passwd, repasswd)
    #
    #     hint_user = '/html/body/div[1]/div/div/form/div[1]/span[1]'
    #     hint_passwd = '/html/body/div[1]/div/div/form/div[2]/span[1]'
    #     hint_repasswd = '/html/body/div[1]/div/div/form/div[3]/span[1]'
    #
    #     page = self.driver.title
    #     result = None
    #     # if page == expect_page:
    #     if page == '度小满理财-登录[内测版]':
    #         # 注册成功，检查完删除
    #         sql = f'select * from user where username="{user}" and password=md5("{passwd}")'
    #         self.cursor.execute(sql)
    #         has = self.cursor.fetchone()
    #         if has:
    #             result = 'ok'
    #         else:
    #             result = 'not ok'
    #
    #         d_sql = f"delete from user where username='{user}' and password=md5('{passwd}');"
    #         self.cursor.execute(d_sql)
    #
    #     else:
    #         match expect_info:
    #             case '两次密码不相同' | '重复密码为空':
    #                 result = self.driver.find_element(By.XPATH, hint_repasswd).text
    #             case '密码为空':
    #                 result = self.driver.find_element(By.XPATH, hint_passwd).text
    #             case _:
    #                 result = self.driver.find_element(By.XPATH, hint_user).text
    #
    #     self.ASSERT_RESULT(page, expect_page)
    #     self.ASSERT_RESULT(result, expect_info)



    def test_bankcard_add(self):
        pass

    def test_bankcard_rmv(self):
        pass

    def test_bankcard_modify(self):
        pass

    def test_buy_share(self):
        pass

    def test_apply_loan(self):
        pass


