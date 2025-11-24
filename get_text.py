import time
import requests
import chardet
from get_url import get_url
from to_pdf import to_pdf
from bs4 import BeautifulSoup
from fpdf import FPDF

# 导入配置
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import Config
except ImportError:
    # 如果配置文件不存在，使用默认配置
    class Config:
        USER_AGENT = "Mozilla/5.0 (兼容浏览器)"
        REQUEST_DELAY = 2

def update(num):
    pdf = FPDF()

    headers = {
        'User-Agent': Config.USER_AGENT
    }

    a_list = get_url(num)

    for a in a_list:
        time.sleep(Config.REQUEST_DELAY)
        nbw_url = f"{Config.TARGET_BASE_URL}/{a}" # 某一篇文章的网址
        response = requests.get(nbw_url,headers=headers)
        encoding = chardet.detect(response.content)['encoding']  # 检测编码
        response.encoding = encoding  # 应用检测到的编码

        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            article_title = soup.find("h1") # 提取文章标题
            div1 = soup.find("div", attrs={"class": "article-sm text-center"})
            text = div1.get_text(strip=True)  # 获取全部文本（去除空白）
            author = text.split('：')[1].split('发布时间')[0].strip()  # 提取作者部分
            publish_time = text.split('：')[2].split('点击数')[0].strip() # 提取发布时间
            div2 = soup.find("div", {"class": "v_news_content"})
            p_list = div2.find_all("p")
            article_text = '\n'.join(p.get_text(strip=True) for p in p_list)
            to_pdf(pdf, article_title.string, author, publish_time, article_text)
            # print(f"标题：{article_title.string}")
            # print(f"作者：{author}")
            # print(f"发布时间：{publish_time}")
            # print(article_text)
        else:
            print(f'请求失败，状态码：{response.status_code}')

    # 保存文件
    filename = "News.pdf"
    pdf.output(filename)
    print("更新完成")
    return True