"""
@Author: kang.yang
@Date: 2023/5/13 10:16
"""
import time

from kytest.utils.log import logger
from playwright.sync_api import expect
from kytest.utils.exceptions import KError
from kytest.core.web.driver import WebDriver
from kytest.utils.common import calculate_time


class WebElem:
    """
    通过selenium定位的web元素
    """

    def __init__(self,
                 driver: WebDriver = None,
                 xpath: str = None,
                 css: str = None,
                 _debug: bool = False):
        """

        @param driver: 浏览器驱动
        @param xpath: xpath定位
        @param css: css定位
        @param _debug: 截图并圈选位置，用于调试
        """
        self._xpath = xpath
        self._css = css

        self._locator = None
        if self._xpath is not None:
            self._locator = self._xpath
        if self._css is not None:
            self._locator = self._css

        self._driver = driver
        self._debug = _debug

    def __get__(self, instance, owner):
        """pm模式的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    # 公共方法
    def get_locator(self):
        element = self._driver.page.locator(self._locator)
        return element

    @calculate_time
    def find(self, timeout=10):
        """查找指定的一个元素"""
        logger.info(f"查找元素: {self._locator}")
        element = self.get_locator()

        try:
            element.wait_for(timeout=timeout*1000)
            logger.info("查找成功")
            if self._debug is True:
                element.evaluate('(element) => element.style.border = "2px solid red"')
                time.sleep(1)
                self._driver.screenshot("查找成功")
            return element
        except:
            logger.info("查找失败")
            self._driver.screenshot("查找失败")
            raise KError(f"{self._locator} 查找失败")

    def exists(self, timeout=5):
        logger.info(f'判断元素 {self._locator} 是否存在')
        result = False
        while timeout > 0:
            result = self.get_locator().is_visible()
            logger.debug(result)
            if result is True:
                break
            time.sleep(1)
            timeout -= 1
        logger.info(f"final result: {result}")
        return result

    # 属性
    @property
    def text(self):
        logger.info(f"获取 {self._locator} 文本属性")
        elem = self.find()
        text = elem.text_content()
        logger.info(text)
        return text

    def get_text_list(self):
        logger.info(f"获取 {self._locator} 文本属性")
        elems = self.find().all()
        text_list = [elem.text_content() for elem in elems]
        logger.info(text_list)
        return text_list

    # 其他方法
    def scroll_into_view(self, timeout=5):
        logger.info(f"{self._locator} 滑动的可视区域")
        self.find(timeout=timeout).scroll_into_view_if_needed(timeout=timeout * 1000)

    def click(self, timeout=5, position=None):
        logger.info(f"点击 {self._locator}")
        self.find(timeout=timeout).click(timeout=timeout * 1000, position=position)

    def click_exists(self, timeout=5):
        logger.info(f"元素 {self._locator} 存在才点击")
        if self.exists(timeout=timeout):
            self.click(timeout=timeout)

    def input(self, text, timeout=5, enter=False):
        logger.info(f"输入文本: {text}")
        _element = self.find(timeout=timeout)
        _element.fill(text, timeout=timeout * 1000)
        if enter is True:
            time.sleep(1)
            _element.press('Enter', timeout=timeout*1000)

    def input_exists(self, text, timeout=5, enter=False):
        logger.info(f"元素 {self._locator} 才输入文本 {text}")
        if self.exists(timeout=timeout):
            self.input(text, timeout=timeout, enter=enter)

    def enter(self, timeout=5):
        logger.info("点击enter")
        self.find(timeout=timeout).press("Enter")

    def check(self, timeout=5):
        logger.info("选择选项")
        self.find(timeout=timeout).check(timeout=timeout * 1000)

    def select(self, value: str, timeout=5):
        logger.info("下拉选择")
        self.find(timeout=timeout).select_option(value, timeout=timeout * 1000)

    def assert_visible(self, timeout=5):
        logger.info(f"断言 {self._locator} 可见")
        expect(self.find(timeout=timeout)).to_be_visible(timeout=timeout * 1000)

    def assert_hidden(self, timeout=5):
        logger.info(f"断言 {self._locator} 被隐藏")
        expect(self.find(timeout=timeout)).to_be_hidden(timeout=timeout * 1000)

    def assert_text_cont(self, text: str, timeout=5):
        logger.info(f"断言 {self._locator} 包含文本: {text}")
        expect(self.find(timeout=timeout)).to_contain_text(text, timeout=timeout * 1000)

    def assert_text_eq(self, text: str, timeout=5):
        logger.info(f"断言 {self._locator} 文本等于: {text}")
        expect(self.find(timeout=timeout)).to_have_text(text, timeout=timeout * 1000)


if __name__ == '__main__':
    pass

