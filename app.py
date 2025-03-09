from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import os  # 新增导入

app = Flask(__name__)

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_etsy_images(shop_url):
    images = []
    headers = {'User-Agent': get_random_user_agent()}

    try:
        response = requests.get(shop_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for item in soup.find_all('div', {'class': 'v2-listing-card__info'}):
            img_tag = item.find('img')
            if img_tag and 'src' in img_tag.attrs:
                images.append(img_tag['src'])

        time.sleep(random.uniform(3, 5))
    except Exception as e:
        print(f"Error: {e}")

    return images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_images', methods=['POST'])
def get_images():
    shop_url = request.form['shop_url']
    image_urls = get_etsy_images(shop_url)
    return jsonify(image_urls)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 关键修改
    app.run(host='0.0.0.0', port=port)  # 关键修改
# 在app.py文件末尾保持以下结构
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
