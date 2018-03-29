from selenium import webdriver
from scrapy.selector import Selector
import time

# browser = webdriver.Chrome(executable_path='E:/caiji/chromedriver_win32/chromedriver.exe')

# browser.get('https://weibo.com/login.php')
# browser.get('https://www.oschina.net/blog')
# time.sleep(5)
# print(browser.page_source)
# time.sleep(5)
# browser.find_element_by_css_selector(".info_list.username .input_wrap input#loginname").send_keys('18659328891')
# browser.find_element_by_css_selector(".info_list.password .input_wrap input[name='password']").send_keys('zhx18659328891')
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
# for i in range(3):
#     browser.execute_script("window.scrollTo(0,document.body.scrollHeight); var lenofpage=document.body.scrollHeight;return lenofpage")
#     time.sleep(3)
# def calc(*numbers):
#     print(type(numbers))
#     sum = 0
#     for n in numbers:
#         sum = sum + n * n
#     return sum
#
# print(calc(1))

# for i in enumerate(['A','B','C']):
#     print(i[1])
L = ['Hello', 'World', 18, 'Apple', None]
list_item = [s.lower() for s in L if isinstance(s,str)]
print(list_item)