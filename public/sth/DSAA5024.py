import pandas as pd
import plotly.express as px

# 加载数据
url = r"C:\Users\xjxl\Desktop\full_data-1.csv"
data = pd.read_csv(url)

# 筛选最新日期的数据
latest_date = data['date'].max()
latest_data = data[data['date'] == latest_date]

# 计算病死率
latest_data['case_fatality_rate'] = (
    latest_data['total_deaths'] / latest_data['total_cases'] * 100
).fillna(0)

# 处理 new_cases 中的空值和负值，并缩放
latest_data['new_cases'] = latest_data['new_cases'].fillna(0).apply(lambda x: max(x, 1))  # 防止为 0

# 调整缩放逻辑以增强对比度
latest_data['scaled_new_cases'] = latest_data['new_cases']**0.3  # 调整指数以增加对比度
latest_data['scaled_new_cases'] = latest_data['scaled_new_cases'].apply(lambda x: max(x, 0.05))  # 让小的点更小
latest_data['scaled_new_cases'] = latest_data['scaled_new_cases'] / latest_data['scaled_new_cases'].max() * 60  # 归一化并调整到最大大小范围

# 检查并替换 NaN 或非法值
latest_data['scaled_new_cases'] = latest_data['scaled_new_cases'].fillna(1).apply(lambda x: max(x, 0.05))

# 对横坐标开平方根
latest_data['sqrt_total_cases'] = latest_data['total_cases'].apply(lambda x: x**0.5)

# 创建综合散点图
fig = px.scatter(
    latest_data,
    x='sqrt_total_cases',
    y='total_deaths',
    color='location',  # 基于 location 着色
    size='scaled_new_cases',  # 根据缩放后的 new_cases 调整点的大小
    hover_data={
        'location': True,               # 显示国家/地区名称
        'new_cases': True,              # 显示新增病例
        'case_fatality_rate': ':.2f',   # 显示病死率，保留两位小数
        'total_cases': True             # 显示总病例数（原始值）
    },
    title='COVID-19 Total Cases vs Total Deaths (Colored by Location, Sized by New Cases)',
    labels={
        'new_cases': 'New Cases',
        'location': 'Location',
        'sqrt_total_cases': 'Sqrt of Total Cases',
        'total_deaths': 'Total Deaths',
        'scaled_new_cases': 'Scaled New Cases'
    },
    size_max=60  # 设置最大圆的大小
)

fig.show()