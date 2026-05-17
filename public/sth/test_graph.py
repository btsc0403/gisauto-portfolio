# Fixing syntax error and re-running the visualization

import networkx as nx
import matplotlib.pyplot as plt

# 构建三元组的关系图
triples = [
("Baiyun Hotel", "located at", "367 Huanshi East Road, Yuexiu District, Guangzhou"),
("Baiyun Hotel", "construction started", "1972"),
("Baiyun Hotel", "construction completed", "June 1976"),
("Government", "decided to invest", "20 million RMB"),
("Government", "in", "Guangzhou"),
("Government", "invested in the construction of", "Baiyun Hotel"),
("Baiyun Hotel", "land area", "26,000 square meters"),
("Baiyun Hotel", "building area", "59,100 square meters"),
("Baiyun Hotel", "number of floors", "33 floors"),
("Baiyun Hotel", "building height", "120 meters"),
("Baiyun Hotel", "number of guest rooms", "721 rooms"),
("Baiyun Hotel", "facilities", "restaurant"),
("Baiyun Hotel", "facilities", "bar"),
("Baiyun Hotel", "facilities", "dance hall"),
("Baiyun Hotel", "facilities", "fitness and beauty center"),
("Baiyun Hotel", "facilities", "conference hall"),
("Baiyun Hotel", "facilities", "business center"),
("Baiyun Hotel", "facilities", "color photo printing service center"),
("Baiyun Hotel", "facilities", "post office"),
("Baiyun Hotel", "facilities", "bank"),
("Baiyun Hotel", "adjacent to", "Li Bai Square"),
("Baiyun Hotel", "adjacent to", "Friendship Store"),
("Baiyun Hotel", "adjacent to", "World Trade Center"),
("Baiyun Hotel", "adjacent to", "famous bar street"),
("Baiyun Hotel", "included in", "the second batch of China’s 20th Century Architectural Heritage"),
("Baiyun Hotel", "star rating", "five-star hotel"),
("Baiyun Hotel", "included in", "the first batch of historic buildings in Guangzhou"),
("Baiyun Hotel", "included in", "Guangzhou's first batch of historical building preservation list in January 2023"),
("Baiyun Hotel", "named after", "the panoramic view of Baiyun Mountain")
]

# 创建一个有向图
G = nx.DiGraph()

# 添加三元组到图中
for head, relation, tail in triples:
    G.add_edge(head, tail, label=relation)

# 设置图的布局
pos = nx.spring_layout(G, k=1, seed=42)

# 画节点
plt.figure(figsize=(15, 10))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=12, font_weight='bold', edge_color='gray')

# 画边的标签
edge_labels = {(head, tail): relation for head, relation, tail in triples}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)

# 展示图
plt.title("白云宾馆知识图谱")
plt.show()
