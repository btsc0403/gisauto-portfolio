import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.patches as mpatches
import numpy as np
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建图
G = nx.Graph()

# 添加中心节点
G.add_node("广州历史建筑", node_type="center", size=5000)

# 添加所有区域节点
districts = ["越秀区", "海珠区", "荔湾区", "白云区", "番禺区", "南沙区", 
             "天河区", "黄埔区", "花都区", "增城区", "从化区"]
for district in districts:
    G.add_node(district, node_type="district", size=3000)
    G.add_edge("广州历史建筑", district)

# 添加批次节点（6个批次）
batches = ["第一批", "第二批", "第三批", "第四批", "第五批", "第六批"]
for batch in batches:
    G.add_node(batch, node_type="batch", size=2500)
    G.add_edge("广州历史建筑", batch)

# 添加更多建筑类型节点
building_types = ["祠堂", "民居", "骑楼", "旧址", "家塾", "宾馆", "门楼", 
                  "书舍", "学校", "商业", "公园", "桥梁", "工业", "其他"]
for btype in building_types:
    G.add_node(btype, node_type="type", size=2000)
    G.add_edge("广州历史建筑", btype)

# 扩展的建筑数据（从各批次选取代表性建筑）
buildings_data = [
    # 第一批代表性建筑
    ("羊城宾馆", "越秀区", "第一批", "宾馆"),
    ("中国大酒店", "越秀区", "第一批", "宾馆"),
    ("新爱群大厦", "越秀区", "第一批", "商业"),
    ("小洲村玉虚宫", "海珠区", "第一批", "祠堂"),
    ("关山月旧居", "海珠区", "第一批", "民居"),
    ("顾庐康庐", "海珠区", "第一批", "民居"),
    ("明勤第", "荔湾区", "第一批", "民居"),
    ("昌华庐", "荔湾区", "第一批", "民居"),
    ("华南工学院宿舍", "天河区", "第一批", "学校"),
    ("海珠桥", "越秀区", "第一批", "桥梁"),
    
    # 第二批代表性建筑
    ("方石曹氏宗祠", "白云区", "第二批", "祠堂"),
    ("梅田迎龙门楼", "白云区", "第二批", "门楼"),
    ("南野公祠", "从化区", "第二批", "祠堂"),
    ("显扬梁公家塾", "番禺区", "第二批", "家塾"),
    ("大岭村龙津街门", "番禺区", "第二批", "门楼"),
    ("黄埔村民居", "海珠区", "第二批", "民居"),
    ("暨南大学办公楼", "天河区", "第二批", "学校"),
    ("流花湖南门", "越秀区", "第二批", "公园"),
    ("东湖公园九曲桥", "越秀区", "第二批", "公园"),
    
    # 第三批代表性建筑
    ("粤汉铁路流溪河桥", "白云区", "第三批", "桥梁"),
    ("沙湾何氏翰林祠", "番禺区", "第三批", "祠堂"),
    ("何炳林故居", "番禺区", "第三批", "民居"),
    ("广州造纸厂", "海珠区", "第三批", "工业"),
    ("朗头村书室", "花都区", "第三批", "书舍"),
    ("录顺船坞", "黄埔区", "第三批", "工业"),
    ("华安楼", "越秀区", "第三批", "民居"),
    
    # 第四批代表性建筑
    ("红线女旧居", "越秀区", "第四批", "民居"),
    ("梧岗书舍", "白云区", "第四批", "书舍"),
    ("张升楼", "南沙区", "第四批", "民居"),
    ("塘坑朱氏祠", "南沙区", "第四批", "祠堂"),
    ("林隐陈祠", "番禺区", "第四批", "祠堂"),
    ("小龙村乡约", "番禺区", "第四批", "其他"),
    
    # 第五批代表性建筑
    ("永汉电影院", "越秀区", "第五批", "商业"),
    ("北京路骑楼", "越秀区", "第五批", "骑楼"),
    ("耀庐", "越秀区", "第五批", "民居"),
    ("竺园", "越秀区", "第五批", "民居"),
    ("敦本堂", "荔湾区", "第五批", "祠堂"),
    ("皇上皇", "荔湾区", "第五批", "商业"),
    ("蛇王福", "荔湾区", "第五批", "商业"),
    ("恩宁路骑楼", "荔湾区", "第五批", "骑楼"),
    
    # 第六批代表性建筑
    ("馨园", "越秀区", "第六批", "民居"),
    ("岭南画派纪念馆", "海珠区", "第六批", "其他"),
    ("车陂郝氏宗祠", "天河区", "第六批", "祠堂"),
    ("华南农学院8号楼", "天河区", "第六批", "学校"),
    ("镇龙黄氏宗祠", "黄埔区", "第六批", "祠堂"),
    ("杨氏更楼", "花都区", "第六批", "其他"),
    ("邓村石屋群", "增城区", "第六批", "民居"),
    ("君松徐公祠", "从化区", "第六批", "祠堂"),
]

# 添加建筑节点和边
for building, district, batch, btype in buildings_data:
    G.add_node(building, node_type="building", size=1000)
    G.add_edge(building, district)
    G.add_edge(building, batch)
    G.add_edge(building, btype)

# 创建紧凑的分层布局
pos = {}
center_x, center_y = 0, 0
pos["广州历史建筑"] = (center_x, center_y)

# 第一层：区域节点（环形排列）
district_radius = 3
district_angle_step = 2 * np.pi / len(districts)
for i, district in enumerate(districts):
    angle = i * district_angle_step
    pos[district] = (center_x + district_radius * np.cos(angle), 
                     center_y + district_radius * np.sin(angle))

# 第一层：批次节点（内圈）
batch_radius = 2
batch_angle_step = 2 * np.pi / len(batches)
for i, batch in enumerate(batches):
    angle = i * batch_angle_step + np.pi/6  # 偏移避免重叠
    pos[batch] = (center_x + batch_radius * np.cos(angle), 
                  center_y + batch_radius * np.sin(angle))

# 第一层：类型节点（中圈）
type_radius = 2.5
type_angle_step = 2 * np.pi / len(building_types)
for i, btype in enumerate(building_types):
    angle = i * type_angle_step + np.pi/12  # 偏移
    pos[btype] = (center_x + type_radius * np.cos(angle), 
                  center_y + type_radius * np.sin(angle))

# 第二层：建筑节点（围绕相关区域）
building_count = {}
for building, district, batch, btype in buildings_data:
    if district not in building_count:
        building_count[district] = 0
    
    # 在区域节点周围排列
    district_pos = pos[district]
    angle = building_count[district] * 0.8
    radius = 1.2
    pos[building] = (district_pos[0] + radius * np.cos(angle),
                     district_pos[1] + radius * np.sin(angle))
    building_count[district] += 1

# 使用spring_layout优化
pos = nx.spring_layout(G, pos=pos, k=0.8, iterations=50)

# 设置图形大小
plt.figure(figsize=(20, 16))

# 定义节点颜色
node_colors = {
    "center": "#E74C3C",      # 红色
    "district": "#3498DB",    # 蓝色
    "batch": "#2ECC71",       # 绿色
    "type": "#F39C12",        # 橙色
    "building": "#9B59B6"     # 紫色
}

# 绘制节点
for node_type in node_colors:
    node_list = [node for node, attr in G.nodes(data=True) if attr.get("node_type") == node_type]
    node_sizes = [G.nodes[node].get("size", 1000) for node in node_list]
    nx.draw_networkx_nodes(G, pos, 
                          nodelist=node_list,
                          node_color=node_colors[node_type],
                          node_size=node_sizes,
                          alpha=0.85,
                          edgecolors='white',
                          linewidths=2)

# 绘制边
# 主要连接
main_edges = [(u, v) for u, v in G.edges() if "广州历史建筑" in [u, v]]
nx.draw_networkx_edges(G, pos, edgelist=main_edges, 
                      edge_color='#34495E', width=2, alpha=0.6)

# 次要连接
other_edges = [(u, v) for u, v in G.edges() if "广州历史建筑" not in [u, v]]
nx.draw_networkx_edges(G, pos, edgelist=other_edges,
                      edge_color='#BDC3C7', width=1, alpha=0.4)

# 绘制标签
# 主要节点标签
main_labels = {node: node for node in G.nodes() 
               if G.nodes[node].get("node_type") in ["center", "district", "batch", "type"]}
nx.draw_networkx_labels(G, pos, main_labels, 
                       font_size=9, font_weight='bold')

# 建筑标签（更小的字体）
building_labels = {node: node for node in G.nodes() 
                  if G.nodes[node].get("node_type") == "building"}

for node in building_labels:
    x, y = pos[node]
    # 智能调整标签位置
    angle = np.arctan2(y, x)
    offset = 0.03
    label_x = x + offset * np.cos(angle)
    label_y = y + offset * np.sin(angle)
    
    # 简化长名称
    label = node
    if len(label) > 8:
        label = label[:6] + "..."
    
    plt.text(label_x, label_y, label, 
             fontsize=7, ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.2", 
                      facecolor="white", 
                      edgecolor="gray",
                      alpha=0.8))

# 添加图例
legend_elements = [
    mpatches.Patch(color='#E74C3C', label='中心节点'),
    mpatches.Patch(color='#3498DB', label='行政区 (11个)'),
    mpatches.Patch(color='#2ECC71', label='批次 (6批)'),
    mpatches.Patch(color='#F39C12', label='建筑类型 (14种)'),
    mpatches.Patch(color='#9B59B6', label='历史建筑 (48个示例)')
]
plt.legend(handles=legend_elements, loc='upper right', fontsize=11, 
          frameon=True, fancybox=True, shadow=True)

# 添加标题
plt.title("广州历史建筑知识图谱（第一批至第六批）", fontsize=24, fontweight='bold', pad=20)

# 添加统计信息
stats_text = (f"数据统计：{len(districts)}个行政区 | {len(batches)}个批次 | "
              f"{len(building_types)}种建筑类型 | {len(buildings_data)}个建筑示例")
plt.text(0.5, 0.02, stats_text, transform=plt.gca().transAxes, 
         ha='center', fontsize=11, 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#ECF0F1", alpha=0.9))

plt.axis('off')
plt.tight_layout()
plt.show()