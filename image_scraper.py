import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from PIL import Image
from io import BytesIO
import base64

# 自动安装ChromeDriver
chromedriver_autoinstaller.install()

def download_image(url, folder_path, img_name):
    if url.startswith('data:image'):
        # 处理Base64编码的图像数据
        base64_data = url.split(',')[1]
        image_data = base64.b64decode(base64_data)
        img = Image.open(BytesIO(image_data))
        img.save(os.path.join(folder_path, img_name))
        print(f'Downloaded {img_name} (Base64)')
    else:
        # 处理常规图像URL
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, img_name), 'wb') as f:
                f.write(response.content)
                print(f'Downloaded {img_name}')
        else:
            print(f'Failed to download {url}')

def scrape_images(query, download_path, num_images):
    # 设置ChromeDriver服务
    service = Service()
    driver = webdriver.Chrome(service=service)

    try:
        # 访问Bing图像搜索
        driver.get('https://www.bing.com/images')

        # 查找搜索框并清除默认文本
        search_box = driver.find_element(By.NAME, 'q')
        search_box.clear()

        # 输入搜索查询并提交
        search_box.send_keys(query)
        search_box.submit()

        # 等待页面加载
        time.sleep(1)

        # 创建下载目录
        os.makedirs(download_path, exist_ok=True)

        # 滚动页面以加载更多图片
        images = driver.find_elements(By.CSS_SELECTOR, 'img.mimg')
        while len(images) < num_images:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            images = driver.find_elements(By.CSS_SELECTOR, 'img.mimg')
            if len(images) >= num_images:
                break

        # 下载指定数量的图片
        for idx, img in enumerate(images[:num_images]):
            img_url = img.get_attribute('src')
            if img_url:
                download_image(img_url, download_path, f'image_{idx + 1}.jpg')

    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    search_query = "刘亦菲"  # 替换为你想要搜索的关键词
    download_folder = "downloaded_images"  # 替换为你想要保存图片的文件夹路径
    num_images = 300  # 替换为你想要下载的图片数量
    scrape_images(search_query, download_folder, num_images)
