import requests
import openpyxl
import threading
import time
import pandas as pd

startTime = time.time()
# 高德API Key
api_key = "your api_key"

# 构建请求URL的函数
def get_geocode(address, session, progress, lock):
    url = f"https://restapi.amap.com/v3/geocode/geo?key={api_key}&address={address}"
    response = session.get(url)
    if response.status_code == 200:
        result = response.json()
        if 'geocodes' in result and result['geocodes']:
            location = result['geocodes'][0]['location']
            print(f"Found location for {address}: {location}")  # 添加日志记录
            return address, location.split(',')
        else:
            print(f"No location found for {address}")  # 添加日志记录
            return address, None
    else:
        print(f"Error: {response.status_code} for address: {address}")  # 添加日志记录
        return address, None

# 向Excel文件中追加数据,文件不存在则新建文件
def write_to_excel(data, filename="geocode_results.xlsx"):
    try:
        # 尝试加载现有的工作簿
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active
    except FileNotFoundError:
        # 如果文件不存在，则创建新的工作簿
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Geocode Results"
        sheet.append(["省市区街道", "经度", "纬度"])

    # 追加数据到现有的工作表
    for item in data:
        if item[1]:
            sheet.append([item[0], item[1][0], item[1][1]])
        else:
            sheet.append([item[0], "未找到经度", "未找到纬度"])

    # 保存工作簿
    workbook.save(filename)

# 导入省市区街道数据
addresses = pd.read_excel("../cleaned.xlsx")
# 转化为列表
addresses = addresses['省市区街道'].tolist()
addresses = addresses[:5000]

total_addresses = len(addresses)

# 使用多线程获取经纬度数据
geocode_data = []
threads = []
num_threads = 3  # 适当减少线程数量
requests_per_second = 3
progress = [0]
progress_lock = threading.Lock()

def worker(addresses, session, progress, lock):
    for address in addresses:
        result = get_geocode(address, session, progress, lock)
        with lock:
            geocode_data.append(result)
            progress[0] += 1
            print(f"进度: {progress[0]}/{total_addresses}")
        time.sleep(requests_per_second / num_threads)  # 控制每秒请求数量

# 创建Session对象
session = requests.Session()

# 将地址列表分成若干份，每个线程处理一份
chunk_size = len(addresses) // num_threads
chunks = [addresses[i:i + chunk_size] for i in range(0, len(addresses), chunk_size)]

# 创建并启动线程
for chunk in chunks:
    thread = threading.Thread(target=worker, args=(chunk, session, progress, progress_lock))
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

# 将结果写入Excel文件
write_to_excel(geocode_data)

print("经纬度数据已写入Excel文件")

endTime = time.time()
print(f"总计耗时: {round(endTime - startTime,2)}s")
