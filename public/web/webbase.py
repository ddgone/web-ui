# -*- coding: utf-8 -*-
# @File: selenium_driver.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/4  14:40

import os
import time

import pyautogui, pyperclip
import allure
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from public.logs import logger
from config.setting import PRPORE_SCREEN_DIR
from config.setting import POLL_FREQUENCY, IMPLICITLY_WAIT_TIME


class Base():

    def __init__(self, driver):
        self.driver = driver

    def get_title(self):
        """
        获取当前页面  title
        :return:
        """
        title = self.driver.title
        logger.info(f"获取当前title {title}")
        return title

    def get_url(self):
        """
        获取当前页面的URL
        :return:
        """
        currentURL = self.driver.current_url
        logger.info(f"获取当前url {currentURL}")
        return currentURL

    def get_url_html(self):
        """
        获取当前页面 html内容
        :return:
        """
        sourceHtml = self.driver.page_source
        return sourceHtml

    def refresh(self):
        """
        刷新当前页面
        :return:
        """
        logger.info('刷新当前页面')
        return self.driver.refresh()

    def back(self):
        """
        返回上一个页面
        :return:
        """
        self.driver.back()
        logger.info('返回上一个页面')

    def forward(self):
        """
        前进到下一个页面
        :return:
        """
        self.driver.forward()
        logger.info('前进到下一个页面')

    def baclick(self):
        """
        点击页面
        :return:
        """
        base_click = self.driver.click()

        return base_click

    def web_scroll(self, direction):
        """
        网页滚动
        :param direction: str   up 向上   Down 向下
        :return:
        """
        if direction == "up":
            logger.info('滚动到顶部')
            self.driver.execute_script("window.scrollBy(0, -10000);")
        if direction == "down":
            logger.info('滚动到底部')
            self.driver.execute_script("window.scrollBy(0, 10000)")

    def current_window(self):
        """
        获取当前窗口句柄 不能单一使用 实际获取的不是当前句柄
        :return:
        """
        current_window = self.driver.current_window_handle
        logger.info(f'获取当前句柄 {current_window}')
        return current_window

    def all_handle(self):
        """
        获取所有句柄
        :return:  list
        """
        handle = self.driver.window_handles
        logger.info(f'获取所有句柄 {handle}')
        return handle

    def switch_windows(self, index):
        """
        多窗口切换
        :param index: 列表索引 all_handle的列表索引位置
        :return:
        """
        indexHandle = self.all_handle()[index]
        try:
            logger.info(f'窗口已经切换{indexHandle}')
            return self.driver.switch_to_window(indexHandle)

        except Exception as e:
            logger.error("查找窗口句柄handle异常-> {0}".format(e))

    def accept(self):
        """
        警告框处理 确认
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.accept()
            logger.info('警告框已确认')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def dismiss(self):
        """
        警告框处理  取消
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.dismiss()
            logger.info('警告框已取消')
            return accept
        except Exception as e:
            logger.error("查找dismiss弹出框异常-> {0}".format(e))

    def alertText(self):
        """
        警告框处理 提取警告框文本
        :return:
        """
        try:
            accept = self.driver.switch_to.alert.text
            logger.info(f'警告框文本信息为 {accept}')
            return accept
        except Exception as e:
            logger.error("查找alert弹出框异常-> {0}".format(e))

    def screen_shot(self, doc):
        """
        截取当前界面图片
        :param doc:  str 名称
        :return:
        """
        fileName = doc + "." + str(round(time.time() * 1000)) + ".png"
        if len(fileName) >= 200:
            fileName = str(round(time.time() * 1000)) + ".png"
        filePath = os.path.join(PRPORE_SCREEN_DIR, fileName)

        self.driver.save_screenshot(filePath)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=fileName,
                      attachment_type=allure.attachment_type.PNG)
        logger.info(f"截图成功已经存储在: {filePath}")

    def get_dropdown_options_count(self, types, locate):
        """
        获取下拉选项的个数
        :param locatorType: 定位类型
        :param locate: 定位器
        :return:
        """

        element = self.used_operate(types, locate)
        sel = Select(element)
        options = sel.options
        return options

    def element_hover(self, types, locate):
        """
        获取元素后悬停到元素位置
        :param locatorType: 定位类型
        :param locate: 定位器
        :return:
        """
        element = self.used_operate(types, locate)
        hover = ActionChains(self.driver).move_to_element(element).perform()
        logger.info(f"鼠标悬停位置{locate}")
        return hover

    def element_hover_clicks(self, types, locate):
        """
        获取元素后悬停到元素位置 后点击该元素
        :param locatorType: 定位类型
        :param locate: 定位器
        :return:
        """
        element = self.used_operate(types, locate)
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(0.5)
        self.used_double_click(types=types, locate=locate)
        logger.info(f"鼠标悬停位置{locate}")

    def save_as_img(self, types, locate, filename, sleep=1):
        """
        图片另存为  下载文件也可以直接使用
        :param locatorType: 定位类型
        :param locate: 定位器
        :param filename: 图片名称 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待windo 窗口时间 默认 1 秒
        :return: str path 文件路径
        """
        # 右键点击
        self.used_right_click(types=types, locate=locate)
        # 图片另存为
        pyautogui.typewrite(['V'])

        # 将地址以及文件名复制
        pic_dir = os.path.join(PRPORE_SCREEN_DIR, f'{filename}.jpg')
        pyperclip.copy(pic_dir)

        # 等待窗口打开，以免命令冲突，粘贴失败，试过很多次才有0.8，具体时间自己试
        time.sleep(sleep)

        # 粘贴
        pyautogui.hotkey('ctrlleft', 'V')

        # 保存
        pyautogui.press('enter')
        logger.info(f'图片路径为{filename}！')
        return pic_dir

    def upload_files(self, types, locate, filepath, sleep=1):
        """
        文件上传
        :param locatorType: 定位类型
        :param locate: 定位器
        :param filepath: 文件路径 路径必须要输入正确 以为函数没办法判断是否成功
        :param sleep: 等待windo 窗口时间 默认 1 秒
        :return:
        """
        self.used_right_click(types, locate)

        time.sleep(sleep)

        # pyautogui.write(filepath)  # 不支持中文路径

        # 支持中文路径
        pyperclip.copy(filepath)
        time.sleep(sleep)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('enter', presses=2)
        logger.info(f'上传文件路径{filepath}')

    def selcet_locat(self, types, locate, value):
        """
        下拉框操作  **此函数只支持 Select标签 其它标签不支持
        :param types:  定位类型
        :param locate: 定位参数
        :param value:   #选项文字内容
            # 通过index进行选择
            .select_by_index(1)
            # 通过value进行选择
            .select_by_value("2")
            select_by_visible_text("Male")
            # 通过选项文字进行选择
        :return:
        """
        selcet = self.used_operate(types, locate)
        Select(selcet).select_by_visible_text(value)

    def get_by_type(self, types):
        """
        获取定位类型
        :param types:  str  in(id,name,xpath,css,class,link,partlink,tag)
        :return:  False
        """
        locatorType = types.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        elif locatorType == "partlink":
            return By.PARTIAL_LINK_TEXT
        elif locatorType == "tag":
            return By.TAG_NAME
        else:
            logger.info(f"Locator type {locatorType} not correct/supported")
            raise  Exception('定位类型错误！！！！')


    def isElementDisplayed(self, types, locate):
        """
        检查元素是否可见
        :param types:定位类型
        :param locate: 定位器
        :param element:
        :return:
        """
        isDisplayed = False
        element = None

        if locate:
            element = self.used_operate(types, locate)
        if element is not None:
            isDisplayed = element.is_displayed()
            logger.info(f"Element is displayed with locate: {locate} and types: {types}")
        else:
            logger.error(f"Element is not displayed with locate: {locate} and types: {types}")
        return isDisplayed

    def isElementExist(self, types, locate):
        """
        检查元素是否存在
        :param types: 定位类型 used_operate 函数传递过来
        :param locate: 定位器
        :return:
        """
        if self.waitForElement(types, locate):
            elementList = self.driver.find_elements(types, locate)
            if len(elementList) > 0:
                logger.info(f"找到元素 {locate}")
                return True
            else:
                logger.info("元素未找到")
                return False

    def waitForElement(self, types, locate):
        """
        等待元素被加载  配合 isElementExist 函数检查元素是否存在
        :param types: 定位类型  used_operate 函数传递过来
        :param locate:  定位器
        :return:
        """
        timeout = IMPLICITLY_WAIT_TIME
        poll = POLL_FREQUENCY
        try:
            wait = WebDriverWait(self.driver, timeout, poll_frequency=poll)

            element = wait.until(EC.presence_of_element_located((types, locate)))
            logger.info(f'等待页面元素 {locate} {types}  存在')
            return element
        except Exception as e:
            logger.error('等待元素错误,元素在等待时间内未出现！')
            logger.error(e)

    def used_operate(self, types, locate, el=None):
        """
        获取元素  此函数配合 isElementExist 检查元素是否存在
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :return: driver 对象
        """
        types = self.get_by_type(types)
        if self.isElementExist(types, locate):
            if el is not None:
                # find_element 不为空时 查询多个
                element = self.driver.find_elements(types, locate)
            else:
                # find_element 为空时 查询单个
                element = self.driver.find_element(types, locate)
            return element
        else:
            logger.error('定位元素错误未找到！')

    def used_text(self, types, locate, el=None, index=None):
        """
        获取元素  提取文本内容
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :return: driver 对象
        """

        types = self.get_by_type(types)

        if self.isElementExist(types, locate):
            try:
                if el is not None and index is not None:
                    # 多个定位
                    return self.used_operate(types=types, locate=locate, el=el)[index].text
                else:
                    # 单个定位提取文本元素必须是唯一 如果多个时默认返回第一个
                    return self.used_operate(types=types, locate=locate).text
            except Exception as e:
                if AttributeError:
                    logger.error(f'未找到元素或此元素没有 {e}')
                else:
                    logger.error(f'find_element 不为空时 index 参数必须传递！！{e}')
        else:
            logger.error('定位元素错误未找到！')

    def used_click(self, types, locate, el=None, index=None):
        """
        获取元素后  点击
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        try:
            if el is not None and index is not None:
                # 多个定位定位 利用index 列表索引点击
                self.used_operate(types=types, locate=locate, el=el)[index].click()
            else:
                # 单个定位点击
                self.used_operate(types=types, locate=locate).click()
        except Exception as e:
            if AttributeError:
                logger.error(f'未找到元素或此元素没有 {e}')
            else:
                logger.error(f'el 不为空时 index 参数必须传递！！{e}')

    def used_right_click(self, types, locate, el=None, index=None):
        """
        获取元素后 右键点击
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        try:
            if el is not None and index is not None:
                element = self.used_operate(types=types, locate=locate, el=el)[index].click()
                ActionChains(self.driver).context_click(element).perform()
            else:
                # 单个定位点击
                element = self.used_operate(types=types, locate=locate, ).click()
                ActionChains(self.driver).context_click(element).perform()
        except Exception as e:
            if AttributeError:
                logger.error(f'未找到元素或此元素没有 {e}')
            else:
                logger.error(f'el 不为空时 index 参数必须传递！！{e}')

    def used_double_click(self, types, locate, el=None, index=None):
        """
        获取元素后 双击击
        :param locatorType: 定位类型
        :param locate: 定位器
        :return:
        """
        try:
            if el is not None and index is not None:
                element = self.used_operate(types=types, locate=locate, el=el)[index].click()
                ActionChains(self.driver).double_click(element).perform()
            else:
                # 单个定位点击
                element = self.used_operate(types=types, locate=locate, ).click()
                ActionChains(self.driver).double_click(element).perform()
        except Exception as e:
            if AttributeError:
                logger.error(f'未找到元素或此元素没有 {e}')
            else:
                logger.error(f'el 不为空时 index 参数必须传递！！{e}')

    def used_input(self, types, locate, text, el=None, index=None):
        """
        获取元素后输入 并支持键盘操作
        :param types: 定位类型
        :param locate:  定位元素或者 表达式
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 代表多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        try:
            if el is not None and index is not None:
                self.used_operate(types=types, locate=locate, el=el)[index].send_keys(text)
            else:
                self.used_operate(types=types, locate=locate, ).send_keys(text)
        except Exception as e:
            if AttributeError:
                logger.error(f'未找到元素或此元素没有 {e}')
            else:
                logger.error(f'find_element 不为空时 index 参数必须传递！！{e}')

    def used_clear(self, types, locate, el=None, index=None):
        """
        清除输入框
        :param types: 定位类型
        :param locate: 定位元素
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        """
        try:
            if el is not None and index is not None:
                self.used_operate(types=types, locate=locate, el=el)[index].clear()
            else:
                self.used_operate(types=types, locate=locate).clear()
            logger.warning('此定位方法只android系统！！！')
        except Exception as e:
            if AttributeError:
                logger.error(f'未找到元素或此元素没有 {e}')
            else:
                logger.error(f'find_element 不为空时 index 参数必须传递！！{e}')

    def used_clear_continue_input(self, types, locate, text, el=None, index=None):
        """
        清除数据在输入
        :param types: 定位类型
        :param locate: 定位元素
        :param text: 输入文本
        :param el: 单个/多个  默认 find_element=None 单个  / 如果 find_element = 's' 多个
        :param index: 列表索引位置  find_element传递时 此值必填
        :return:
        """
        try:
            self.used_clear(types=types, locate=locate, el=el, index=index)
            time.sleep(0.5)
            self.used_input(types=types, locate=locate, text=text, el=el, index=index)
        except Exception as e:
            if AttributeError:
                logger.error(f'未找到元素或此元素没有 {e}')
            else:
                logger.error(f'find_element 不为空时 index 参数必须传递！！{e}')

    def if_commonly_used_predicate(self, types, locate, operate=None, text=None, el=None, index=None, wait=0.5):
        """
        判断 CommonlyUsed 执行操作
        :param locate:  表达 或者定位元素
        :param operate: 执行操作 类型input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) ,
        :param text: 输入文本内容
        :param el: 输入文本内容
        :param wait: 默认 等待0.5 秒
        :return:
        """
        if operate is None:
            time.sleep(wait)
            return self.used_operate(types=types, locate=locate, el=el)

        elif operate == 'text':  # 提取文本
            time.sleep(wait)
            return self.used_text(types=types, locate=locate, el=el, index=index)

        elif operate == 'click':  # 点击操作
            time.sleep(wait)
            self.used_click(types=types, locate=locate, el=el, index=index)

        elif operate == 'input':  # 输入操作
            if text is not None:
                time.sleep(wait)
                return self.used_input(types=types, locate=locate, text=text, el=el, index=index)
            logger.error('android_uiautomator_input 函数必须传递 text 参数')

        elif operate == 'clear':  # 清除操作
            time.sleep(wait)
            return self.used_clear(types=types, locate=locate, el=el, index=index)

        elif operate == 'clear_continue_input':  # 清除后在输入操作
            if text is not None:
                time.sleep(wait)
                return self.used_clear_continue_input(types=types, locate=locate, text=text, el=el, index=index)
            logger.info('android_uiautomator_clear_continue_input 函数必须传递 text 参数')
        else:
            logger.info('暂时不支持此操作！！！')
            logger.error("""
        目前只支持类型 ： input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本) 
            """)


class WebBase(Base):
    """
     常用定位方式  class(安卓对应 ClassName / iso对应 type) 、 xpath 、 id、
    """

    def web_expression(self, types, locate, operate=None, text=None, el=None, index=None, wait=0.5):
        """
        web 执行操作判断
        :param types: 定位类型
        :param locate: 表达 或者定位元素
        :param operate: 执行操作  input(输入) , clear(清除) , clear_continue_input(清除在输入) 、click(点击) ,text(提取文本)  * 只支持 5种
        :param text : 输入文本内容
        :param el: 单个/多个  默认 el=None 单个  / 如果 el = 's' 代表多个
        :param index:
        :param wait: 默认 等待0.5 秒
        :return:
        """
        # 只支持安卓

        if types in ('id', 'name', 'xpath', 'css', 'class', 'link', 'partlink', 'tag'):
            return self.if_commonly_used_predicate(types=types, locate=locate, operate=operate, text=text, el=el,
                                                   index=index,
                                                   wait=wait)
        else:
            logger.error(f'输入的{operate}操作类型，暂时不支持！！')
            logger.error("""只支持 id,name,xpath,css,class,link,partlink,tag 定位方式""")