import requests
import time
import chardet
from bs4 import BeautifulSoup

# 导入配置
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import Config
except ImportError:
    # 如果配置文件不存在，使用默认配置
    class Config:
        USER_AGENT = "Mozilla/5.0"
        REQUEST_DELAY = 2

headers = {
    'User-Agent': Config.USER_AGENT
}

def get_url(num):
    a_list = []
    for page_num in range(1,num):
        time.sleep(Config.REQUEST_DELAY)
        response = requests.get(Config.TARGET_PAGE_URL.format(page_num=page_num),
                                headers=headers)
        encoding = chardet.detect(response.content)['encoding']  # 检测编码
        response.encoding = encoding  # 应用检测到的编码
        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content,'html.parser')
            ul = soup.find("ul", attrs={"class": "news-ul text-center"})
            li_list = ul.find_all("li")
            for li in li_list:
                div = li.find("div", attrs={"class": "width04"})
                a_url = div.find("a")['href']
                a_list.append(a_url)
        else:
            print(f"请求失败，状态码{response.status_code}")

    return a_list


