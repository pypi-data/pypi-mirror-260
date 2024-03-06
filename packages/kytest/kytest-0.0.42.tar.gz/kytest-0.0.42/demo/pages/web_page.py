"""
@Author: kang.yang
@Date: 2023/11/16 17:49
"""
from kytest import Page, WebElem as Elem


class IndexPage(Page):
    """首页"""
    url = "https://www-test.qizhidao.com/"
    loginBtn = Elem(xpath='//div[text()="登录/注册"]')
    patentText = Elem(xpath='//*[text()="查专利"]')


class LoginPage(Page):
    """登录页"""
    pwdTab = Elem(xpath='//*[text()="帐号密码登录"]')
    userInput = Elem(xpath='//input[@placeholder="请输入手机号码"]')
    pwdInput = Elem(xpath='//input[@placeholder="请输入密码"]')
    accept = Elem(css=".agreeCheckbox .el-checkbox__inner")
    loginBtn = Elem(xpath='//*[text()="立即登录"]')
    firstItem = Elem(xpath="(//img[@class='right-icon'])[1]")
