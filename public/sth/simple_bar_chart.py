import matplotlib.pyplot as plt
import numpy as np

# 🎯 数据修改区域 - 在这里修改您的数据
# ================================================

# 类别名称和颜色 (可以添加或删除类别)
CATEGORIES = {
    'GeoQA for City': '#FF6B9D',
    'Infrastructure Inference': '#4ECDC4', 
    'Geospatial Prediction': '#45B7D1',
    'Street Navigation': '#FFA726',
    'Image Geolocalization': '#5C6BC0'
}

# X轴标签 (可以修改数量和名称)
X_LABELS = ['Tier1', 'Tier2', 'Tier3', 'Tier4', 'Tier5', 'Tier6', 'Tier7']

# 数据 (每个类别对应X轴标签的数值)
DATA = {
    'GeoQA for City': [1, 2, 3, 4, 5, 7, 9],
    'Infrastructure Inference': [2, 2, 2, 5, 4, 5, 5],
    'Geospatial Prediction': [2, 2, 4, 4, 4, 4, 5],
    'Street Navigation': [2, 4, 6, 6, 7, 7, 8],
    'Image Geolocalization': [0, 1, 3, 3, 3, 4, 4]
}

# 图表设置
CHART_TITLE = 'QA System Accuracy by Building Data Tiers'
X_AXIS_LABEL = 'Number of buildings provided'
Y_AXIS_LABEL = 'Accuracy'

# ================================================

def generate_bar_chart():
    """生成柱状图"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 计算柱子位置
    x = np.arange(len(X_LABELS))
    width = 0.15
    multiplier = 0
    
    # 绘制每个类别的柱子
    for category, color in CATEGORIES.items():
        values = DATA[category]
        offset = width * multiplier
        bars = ax.bar(x + offset, values, width, label=category, color=color, alpha=0.8)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{height}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        multiplier += 1
    
    # 设置图表样式
    ax.set_xlabel(X_AXIS_LABEL, fontsize=14, fontweight='bold')
    ax.set_ylabel(Y_AXIS_LABEL, fontsize=14, fontweight='bold')
    ax.set_title(CHART_TITLE, fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(X_LABELS)
    
    # 设置样式
    ax.set_ylim(0, max(max(values) for values in DATA.values()) + 2)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=10)
    ax.set_facecolor('#FAFAFA')
    
    # 保存和显示
    plt.tight_layout()
    plt.savefig('py/quick_bar_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ 图表已生成: py/quick_bar_chart.png")
    plt.show()

if __name__ == "__main__":
    print("🚀 开始生成柱状图...")
    print(f"📊 类别数量: {len(CATEGORIES)}")
    print(f"📈 数据点数量: {len(X_LABELS)}")
    
    generate_bar_chart()
    
    print("\n💡 如需修改数据，请编辑文件顶部的数据区域：")
    print("   - CATEGORIES: 修改类别和颜色")
    print("   - X_LABELS: 修改横轴标签")
    print("   - DATA: 修改数值数据") 