from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv # 用来加载环境变量
import os # 用来加载环境变量
import time



# 加载 .env 文件中的环境变量
load_dotenv()  
TWID = os.environ.get('TWID')
GUEST_ID = os.environ.get('GUEST_ID')
GUEST_ID_ADS = os.environ.get('GUEST_ID_ADS')
GUEST_ID_MARKETING = os.environ.get('GUEST_ID_MARKETING')
PERSONALIZATION_ID = os.environ.get('PERSONALIZATION_ID')
EXTERNAL_REFERER = os.environ.get('EXTERNAL_REFERER')
GT = os.environ.get('GT')
KDT = os.environ.get('KDT')
TWITTER_SESS = os.environ.get('TWITTER_SESS')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
CT0 = os.environ.get('CT0')


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
driver.get("https://twitter.com/home")
time.sleep(5)

cookies = {
    'lang': 'zh-cn',
	'twid': TWID,
	'guest_id': GUEST_ID,
	'guest_id_ads': GUEST_ID_ADS,
	'guest_id_marketing': GUEST_ID_MARKETING,
	'personalization_id': PERSONALIZATION_ID,
	'external_referer': EXTERNAL_REFERER,
	'gt': GT,
	'kdt': KDT,
	'_twitter_sess': TWITTER_SESS,
	'auth_token': AUTH_TOKEN,
	'ct0': CT0,
}

# 给浏览器对象添加 cookie
for name, value in cookies.items():
    driver.add_cookie({'name': name, 'value': value})
    
# 爬取 twitter
# url = f"https://twitter.com/search?q=hello&src=typed_query"
# 🔥定义要抓取的 twitter 账号
# urls = ["https://twitter.com/OpenAI", "https://twitter.com/OpenAIDevs"]


url = f"https://twitter.com/OpenAIDevs"
driver.get(url)


# 等待直到页面上出现特定的元素 => 等待 cellInnerDiv 元素出现
wait = WebDriverWait(driver, 10) # 10 表示最多等待 10 秒
tweets_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))


# 获取所有推文 => 用 selenium 对网页内容进行解析, 也可以使用 BeautifulSoup
tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')


# 遍历推文并提取 span 内容
for tweet_element in tweets:
    # print("检查元素:", tweet.get_attribute('outerHTML')) # 🌟 每条推文的结构
    
    # 🔗 提取推文链接 ————————————————————————————————————————————————————————————————————————
    try:
		# tweet_url = tweet_element.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]')
        tweetDetailPage_url = tweets_container.find_element(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] > a')
        print(f"链接: ", tweetDetailPage_url.get_attribute('href'), '\n')
    except NoSuchElementException:
        print("没有找到链接 ——————————————")
        pass # 如果没有找到链接, 则忽略

    
    # ✏️ 提取文字内容 ————————————————————————————————————————————————————————————————————————
    try:
        span_content = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"] > span')
        print(f"文字: ", span_content.text, '\n')
    except NoSuchElementException:
        # 当找不到指定元素时，跳过当前循环
        print('没有找到文字 ——————————————')
        pass # 如果没有找到文字, 则忽略
        # continue
        
	# ⛰️ 提取图片 ————————————————————————————————————————————————————————————————————————
    try:
        # ⛰️ 提取<img>标签的src属性中的URL => 先找出 a 标签, 再找出 img 标签 => 正确的内容图片是在 a 标签内的, 否则会抓到头像！
        photoWrapper = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] > img')
        # image_element = tweet_element.find_element(By.TAG_NAME, 'img')
        # image_element = tweet_element.find_element(By.CSS_SELECTOR, 'img[draggable="true"]')
        # image_element = photoWrapper.find_element(By.TAG_NAME, 'img')
        image_url = photoWrapper.get_attribute('src')
        print(f"图片: ", image_url, '\n')
    except NoSuchElementException:
        print("没有找到图片 ——————————————")
        pass # 如果没有找到图片, 则忽略
    
    # 📺 提取视频 ————————————————————————————————————————————————————————————————————————
    try:
        video_element = tweet_element.find_element(By.TAG_NAME, 'video')
        video_url = video_element.get_attribute('src')
        print(f"视频: ", video_url, '\n')
		# continue  # 如果有视频，跳过后续图片处理
    except NoSuchElementException:
        print("没有找到视频 ——————————————")
        pass # 如果没有找到视频, 则忽略
          
    # 只抓取一条推文, 注销掉就会抓取一屏幕的推文     
    print("✅ 推文抓取完成")
    break 
                


# 利用 BeautifulSoup 对网页进行分析
# from bs4 import BeautifulSoup
# html = driver.page_source
# soup = BeautifulSoup(html, "html.parser")

# 找出所有推文
# tweets = soup.find_all("div", {'data-testid': "cellInnerDiv"})
# # 再继续找推文内容的属性
# for tweetText in tweets:
# 	# content = tweetText.find('div', {'data-testid': "tweetText"}).text
# 	span_content = tweetText.find('span', {'style': "text-overflow: unset"})
# 	if span_content:
# 		content = span_content.text
# 		print(content)
