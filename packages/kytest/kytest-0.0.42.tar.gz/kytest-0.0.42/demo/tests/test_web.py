"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest
from pages.web_page import IndexPage, LoginPage


@kytest.module('登录模块')
class TestWebDemo(kytest.WebCase):

    def start(self):
        self.username = "13652435335"
        self.password = "wz123456@QZD"
        self.index_name = "首页"
        self.index_page = IndexPage(self.driver)
        self.login_page = LoginPage(self.driver)

    @kytest.title("登录")
    # @data('param', [1, 2, 3])
    def test_login(self):
        # print(param)
        self.index_page.open()
        self.sleep(5)
        self.index_page.loginBtn.click()
        self.sleep(5)
        self.login_page.pwdTab.click()
        self.login_page.userInput.\
            input(self.username)
        self.login_page.pwdInput.\
            input(self.password)
        self.login_page.accept.click()
        self.login_page.loginBtn.click()
        self.login_page.firstItem.click()
        self.assert_url()
        # self.driver.storage_state("state.json")
        self.sleep(3)
        self.screenshot(self.index_name)

    def test_cookies(self):
        self.open("https://www-test.qizhidao.com")
        self.sleep(5)


