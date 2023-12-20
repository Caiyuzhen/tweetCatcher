from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys



# 实例化
options = webdriver.ChromeOptions()

# 开启无界面模式
# options.add_argument("--headless")

# 创建服务对象
chromedriver_path = '/Users/aic/chromedriver'
service = Service(executable_path=chromedriver_path)


# 实例化浏览器对象, 创建 webdriver.Chrome 实例时传入 options 和 service 参数
driver = webdriver.Chrome(service=service, options=options)


# 进入 Twitter 页面
driver.get("https://www.google.com/")
driver.implicitly_wait(10)


# driver.find_element_by_css_selector('#input').send_keys('Python')  # 在搜索框输入Python
# driver.find_element_by_css_selector('#input').send_keys(Keys.ENTER)  # 执行回车
driver.find_element_by_tag_name('textarea').send_keys('Python')  # 在搜索框输入Python
driver.find_element_by_tag_name('textarea').send_keys(Keys.ENTER)  # 执行回车