import json
import os
import csv

# 设置文件路径
json_file_path = r"E:\项目\GIS\mars2d-vue-template-master\mars2d-vue3-vite\public\neo4j_pre\output_triplets.json"
output_dir = r"E:\项目\GIS\mars2d-vue-template-master\mars2d-vue3-vite\public\neo4j_pre"

# 定义CSV文件路径
buildings_csv_path = os.path.join(output_dir, "Buildings.csv")
categories_csv_path = os.path.join(output_dir, "Categories.csv")
locations_csv_path = os.path.join(output_dir, "Locations.csv")
building_located_at_csv_path = os.path.join(output_dir, "Building_Located_At.csv")
building_belongs_to_csv_path = os.path.join(output_dir, "Building_Belongs_To.csv")

# 确保输出目录存在
if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
        print(f"已创建目录：{output_dir}")
    except Exception as e:
        print(f"无法创建目录 {output_dir}：{e}")
        exit(1)

# 初始化数据结构
buildings = {}
categories = {}
locations = {}
additional_info = {}
relationships_located_at = []
relationships_belongs_to = []

# 定义唯一ID生成器
def get_unique_id(entity_dict, name):
    if name not in entity_dict:
        entity_dict[name] = len(entity_dict) + 1
    return entity_dict[name]

# 读取JSON文件（JSON Lines格式，每行一个JSON对象）
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue  # 跳过空行
            try:
                obj = json.loads(line)
                subject = obj.get("subject", "").strip()
                predicate = obj.get("predicate", "").strip()
                object_ = obj.get("object", "").strip()

                if not subject:
                    continue  # 跳过没有主体的三元组

                if predicate == "位于":
                    # subject 是 Building， object 是 Location
                    building_id = get_unique_id(buildings, subject)
                    location_id = get_unique_id(locations, object_)
                    relationships_located_at.append((building_id, location_id))
                elif predicate == "属于":
                    # subject 是 Building， object 是 Category
                    building_id = get_unique_id(buildings, subject)
                    category_id = get_unique_id(categories, object_)
                    relationships_belongs_to.append((building_id, category_id))
                elif predicate == "附加信息":
                    # subject 是 Building， object 是 AdditionalInfo
                    if subject not in buildings:
                        building_id = get_unique_id(buildings, subject)
                    additional_info[subject] = object_
                else:
                    print(f"未知的谓词 '{predicate}' 在第 {line_number} 行，已跳过。")
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误在第 {line_number} 行: {e}")
except FileNotFoundError:
    print(f"找不到 JSON 文件：{json_file_path}")
    exit(1)
except Exception as e:
    print(f"读取 JSON 文件时出错：{e}")
    exit(1)

# 检查是否有数据被读取
if not buildings:
    print("没有有效的建筑物数据被读取。请检查输入文件格式。")
    exit(1)
if not categories and not locations:
    print("没有有效的关系数据被读取。请检查输入文件格式。")
    exit(1)

# 写入 Buildings.csv
try:
    with open(buildings_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['BuildingID', 'Name', 'AdditionalInfo'])  # 表头
        for name, b_id in sorted(buildings.items(), key=lambda x: x[1]):
            info = additional_info.get(name, "")
            writer.writerow([b_id, name, info])
    print(f"成功生成 Buildings CSV：{buildings_csv_path}")
except Exception as e:
    print(f"写入 Buildings CSV 时出错：{e}")
    exit(1)

# 写入 Categories.csv
try:
    with open(categories_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CategoryID', 'Name'])  # 表头
        for name, c_id in sorted(categories.items(), key=lambda x: x[1]):
            writer.writerow([c_id, name])
    print(f"成功生成 Categories CSV：{categories_csv_path}")
except Exception as e:
    print(f"写入 Categories CSV 时出错：{e}")
    exit(1)

# 写入 Locations.csv
try:
    with open(locations_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LocationID', 'Address'])  # 表头
        for address, l_id in sorted(locations.items(), key=lambda x: x[1]):
            writer.writerow([l_id, address])
    print(f"成功生成 Locations CSV：{locations_csv_path}")
except Exception as e:
    print(f"写入 Locations CSV 时出错：{e}")
    exit(1)

# 写入 Building_Located_At.csv
try:
    with open(building_located_at_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['BuildingID', 'LocationID'])  # 表头
        for b_id, l_id in relationships_located_at:
            writer.writerow([b_id, l_id])
    print(f"成功生成 Building_Located_At CSV：{building_located_at_csv_path}")
except Exception as e:
    print(f"写入 Building_Located_At CSV 时出错：{e}")
    exit(1)

# 写入 Building_Belongs_To.csv
try:
    with open(building_belongs_to_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['BuildingID', 'CategoryID'])  # 表头
        for b_id, c_id in relationships_belongs_to:
            writer.writerow([b_id, c_id])
    print(f"成功生成 Building_Belongs_To CSV：{building_belongs_to_csv_path}")
except Exception as e:
    print(f"写入 Building_Belongs_To CSV 时出错：{e}")
    exit(1)

print("所有CSV文件已成功生成！")
