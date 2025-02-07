import pandas as pd
import folium
from folium.plugins import FastMarkerCluster

# 读取Excel文件
df = pd.read_excel('geocode_results.xlsx')

# 过滤掉包含 "未找到经度" 或 "未找到纬度" 的行
df = df[(df['经度'] != "未找到经度") & (df['纬度'] != "未找到纬度")]

# 将经度和纬度列转换为浮点数
df['经度'] = df['经度'].astype(float)
df['纬度'] = df['纬度'].astype(float)

# 创建地图对象，设置初始位置和缩放级别，并使用高德地图的瓦片图层
m = folium.Map(
    location=[df['纬度'].mean(), df['经度'].mean()],
    zoom_start=6,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='高德地图'
)

# 创建FastMarkerCluster对象并添加到地图
FastMarkerCluster(data=list(zip(df['纬度'], df['经度']))).add_to(m)

# 保存地图到HTML文件
m.save('map.html')
