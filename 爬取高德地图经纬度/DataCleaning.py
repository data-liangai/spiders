import pandas as pd
import re

# 读取Excel文件
input_file = "your file"  # 替换文件名
df = pd.read_excel(input_file)

# 只选取省份、城市、区域、街道列,并清除NA行
df = df[['出险省份', '出险市(州)', '出险县(区)','出险街道']].dropna()

# 去掉街道列中的前后空格和前后的句号
df['出险街道'] = df['出险街道'].str.strip().str.strip('.')

# 定义正则表达式过滤函数
def filter_street(street):
    # 过滤掉带有“不详”的所有内容（如“不详村子”除外）
    if re.search(r'不详(?!村子)', street):
        return ''
    # 过滤掉逗号,句号,问号等符号
    if re.search(r'[，？、。,?!]', street):
        return ''
    # 过滤掉纯数字
    if re.fullmatch(r'\d+', street):
        return ''
    return street

# 应用过滤函数
df['出险街道'] = df['出险街道'].apply(filter_street)
# 将空字符串替换为None
df['出险街道'] = df['出险街道'].replace('', None)
# 清除过滤函数之后的空值
df = df.dropna()
# 拼接省市区
df['省市区街道'] = df['出险省份'] + df['出险市(州)'] + df['出险县(区)'] + df['出险街道']
# 去重
df = df[['省市区街道']].drop_duplicates()

# 只输出省市区列到另一个表格中
output_file = "../cleaned.xlsx"  # 替换文件名
df[['省市区街道']].to_excel(output_file, index=False)

print("数据处理完成,结果已输出到新的Excel文件中")
