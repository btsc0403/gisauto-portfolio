import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据配置区域 - 可以在这里轻松修改数据
def get_chart_data():
    """
    配置图表数据
    3类问题，每类问题包含Baseline和Context-Enhanced的对比
    """
    # 3类问题
    problem_types = ['Image Geolocalization', 'GeoQA for City', 'Street Navigation']
    
    # 每类问题对应的颜色
    colors = {
        'Image Geolocalization': '#EBCD51',
        'GeoQA for City': '#559CB6',
        'Street Navigation': '#9EC084'
    }
    
    # 每类问题的Baseline和Context-Enhanced数据
    context_enhanced_data = [9, 24, 22]  # 3类问题使用Context-Enhanced的准确率
    baseline_data = [8, 22, 20]  # 3类问题使用Baseline的准确率
    
    return problem_types, colors, context_enhanced_data, baseline_data

def create_accuracy_bar_chart(save_path='accuracy_bar_chart.png', figsize=(14, 8)):
    """
    创建准确率柱状图 - 横坐标为5类问题，每类问题下有两根柱子（without RAG和RAG）
    
    参数:
    save_path: 保存路径
    figsize: 图片尺寸
    """
    # 获取数据
    problem_types, colors, context_enhanced_data, baseline_data = get_chart_data()
    
    # 设置图片样式
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=figsize)
    
    # 设置柱状图的位置
    n_problems = len(problem_types)
    x = np.arange(n_problems)  # 问题类型的位置
    width = 0.35  # 每根柱子的宽度
    
    # 绘制without RAG的柱子（左边）
    bars1 = ax.bar(x - width/2, baseline_data, width, 
                   label='Standard LLM', alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # 绘制RAG的柱子（右边）
    bars2 = ax.bar(x + width/2, context_enhanced_data, width, 
                   label='Context-Aware LLM', alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # 为每个问题类型设置对应的颜色
    for i, color in enumerate(colors.values()):
        bars1[i].set_color('#B8D4F1')  # 降低饱和度的浅蓝色 - Standard LLM
        bars1[i].set_alpha(0.8)  
        bars1[i].set_edgecolor('black')  
        bars1[i].set_linewidth(0.8)  
        
        bars2[i].set_color('#4A90E2')  # 降低饱和度的深蓝色 - Context-Aware LLM
        bars2[i].set_alpha(1.0)  
        bars2[i].set_edgecolor('black')  
        bars2[i].set_linewidth(0.8)  
    
    # 添加数值标签
    for i, (baseline_val, context_enhanced_val) in enumerate(zip(baseline_data, context_enhanced_data)):
        # Standard LLM标签
        ax.text(i - width/2, baseline_val + 0.5, f'{baseline_val}', 
               ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Context-Aware LLM标签 - 只显示基础数值
        ax.text(i + width/2, context_enhanced_val + 0.5, f'{context_enhanced_val}', 
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 设置图表样式
    ax.set_xlabel('Problem Types', fontsize=14, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=14, fontweight='bold')
    ax.set_title('Standard LLM vs Context-Aware LLM Performance Comparison by Problem Types', 
                fontsize=16, fontweight='bold', pad=20)
    
    # 设置X轴刻度和标签 - 显示问题类型
    ax.set_xticks(x)
    ax.set_xticklabels(['Image Geolocalization', 'GeoQA for City', 'Street Navigation'], 
                       fontsize=10, fontweight='bold')
    
    # 设置Y轴范围和网格
    ax.set_ylim(0, 32)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # 设置图例 - 显示方法类型
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    
    # 创建方法类型图例
    legend_elements = [
        Patch(facecolor='#B8D4F1', alpha=0.8, label='Standard LLM'),
        Patch(facecolor='#4A90E2', alpha=1.0, label='Context-Aware LLM')
    ]
    
    # 添加方法类型图例（右上角）
    legend = ax.legend(handles=legend_elements, loc='upper right', 
                      frameon=True, shadow=True, fontsize=9)
    
    # 在图例上方添加"Methods"标注
    ax.text(0.98, 0.98, 'Methods', transform=ax.transAxes, 
           fontsize=10, fontweight='bold', ha='right', va='top',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # 设置背景和边框
    ax.set_facecolor('#FAFAFA')
    for spine in ax.spines.values():
        spine.set_edgecolor('#CCCCCC')
        spine.set_linewidth(0.8)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"图表已保存至: {save_path}")
    
    # 显示图表
    plt.show()

def create_stacked_bar_chart(save_path='accuracy_stacked_bar_chart.png', figsize=(12, 8)):
    """
    创建堆叠柱状图版本 - 暂时保持原有逻辑
    """
    problem_types, colors, context_enhanced_data, baseline_data = get_chart_data()
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=figsize)
    
    x = np.arange(len(problem_types))
    width = 0.6
    
    # 绘制without RAG数据（现在在底部）
    bars1 = ax.bar(x, baseline_data, width, label='Standard LLM', alpha=0.8)
    # 绘制RAG数据（堆叠在without RAG之上）
    bars2 = ax.bar(x, context_enhanced_data, width, bottom=baseline_data, label='Context-Aware LLM', alpha=0.6)
    
    # 为每个类别设置蓝色系颜色
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        bar1.set_color('#B8D4F1')  # 降低饱和度的浅蓝色
        bar1.set_alpha(0.8)
        bar2.set_color('#4A90E2')  # 降低饱和度的深蓝色
        bar2.set_alpha(0.8)
    
    # 添加数值标签
    for i, (context_enhanced_val, baseline_val) in enumerate(zip(context_enhanced_data, baseline_data)):
        ax.text(i, baseline_val/2, f'{baseline_val}', ha='center', va='center', 
               fontsize=9, fontweight='bold', color='white')
        ax.text(i, baseline_val + context_enhanced_val/2, f'{context_enhanced_val}', ha='center', va='center', 
               fontsize=9, fontweight='bold', color='white')
    
    # 设置图表样式
    ax.set_xlabel('Method', fontsize=14, fontweight='bold')
    ax.set_ylabel('Cumulative Accuracy', fontsize=14, fontweight='bold')
    ax.set_title('Baseline vs Context-Enhanced Cumulative Performance by Problem Types', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(problem_types, rotation=15, ha='right',fontsize=14, fontweight='bold')
    
    # 设置网格和背景
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_facecolor('#FAFAFA')
    ax.set_ylim(0, 50)
    
    # 设置图例
    ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=10)
    
    # 调整布局并保存
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"堆叠柱状图已保存至: {save_path}")
    plt.show()

def customize_chart_data():
    """
    提供交互式数据修改功能
    """
    print("=== 数据自定义功能 ===")
    print("您可以在 get_chart_data() 函数中修改以下内容：")
    print("1. problem_types: 修改问题类型名称")
    print("2. colors: 修改各类型对应的颜色")
    print("3. context_enhanced_data: 修改Context-Enhanced方法的准确率数据")
    print("4. baseline_data: 修改Baseline方法的准确率数据")
    print("\n当前数据预览：")
    
    problem_types, colors, context_enhanced_data, baseline_data = get_chart_data()
    
    print(f"问题类型数量: {len(problem_types)}")
    print(f"问题类型: {problem_types}")
    print(f"Context-Enhanced数据: {context_enhanced_data}")
    print(f"Baseline数据: {baseline_data}")
    print("颜色配置:")
    for ptype, color in colors.items():
        print(f"  {ptype}: {color}")

if __name__ == "__main__":
    print("=== QA系统准确率图表生成器 ===\n")
    
    # 显示数据自定义说明
    customize_chart_data()
    
    print("\n正在生成图表...")
    
    try:
        # 生成分组柱状图
        create_accuracy_bar_chart('py/accuracy_bar_chart.png')
        
        # 生成堆叠柱状图
        create_stacked_bar_chart('py/accuracy_stacked_bar_chart.png')
        
        print("\n✅ 所有图表生成完成！")
        print("📁 文件保存位置: py/ 文件夹")
        print("📊 包含两种图表样式: 分组柱状图 和 堆叠柱状图")
        
    except Exception as e:
        print(f"❌ 生成图表时出错: {e}")
        print("请检查是否安装了所需的依赖包: matplotlib, seaborn, numpy") 