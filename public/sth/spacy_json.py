import json
import os
import re

# 输出文件夹路径
output_folder = r"E:\项目\GIS\mars2d-vue-template-master\mars2d-vue3-vite\public\neo4j_pre"
os.makedirs(output_folder, exist_ok=True)  # 确保文件夹存在

# 输出文件路径
output_file = os.path.join(output_folder, "output_triplets.json")

# 定义去除标点符号的函数（仅适用于建筑名称、地址、历史建筑批次）
def clean_text(text, preserve_punctuation=False):
    # 如果需要保留符号（仅用于附加信息），则不去除符号
    if preserve_punctuation:
        # 保留逗号、句号等符号，清理其他符号
        return re.sub(r'[！？；：""“”‘’()（）]', '', text).strip()
    else:
        # 默认去除所有标点符号（包括逗号、句号等）
        return re.sub(r'[，。！？、；：""“”‘’()（）]', '', text).strip()

# 定义提取三元组的函数：建筑名称，详细地址，历史建筑批次，额外信息
def extract_information(text):
    print(f"正在处理文本: {text}")

    # 1. 提取建筑名称，位于“位于”之前的部分
    location_name_match = re.match(r"^(.*?)位于", text)
    if location_name_match:
        location_name = location_name_match.group(1).strip()
        location_name = clean_text(location_name)  # 清理建筑名称
    else:
        location_name = ""

    # 2. 提取地址，位于“位于”和“是”之间的部分
    address_match = re.search(r"位于(.*?)是", text)
    if address_match:
        address = address_match.group(1).strip()
        address = clean_text(address)  # 清理地址
    else:
        address = ""

    # 3. 提取历史建筑批次，位于“是”之后的部分
    batch_match = re.search(r"是(广州市第[^\s]+批历史建筑)", text)
    if batch_match:
        batch = batch_match.group(1).strip()
        batch = clean_text(batch)  # 清理历史建筑批次
    else:
        batch = ""

    # 4. 提取附加信息，剩余的部分（保留逗号和句号，但不允许符号作为开头）
    extra_info_match = re.search(r"是.*?批历史建筑(.*?)$", text)
    if extra_info_match:
        extra_info = extra_info_match.group(1).strip()
        extra_info = clean_text(extra_info, preserve_punctuation=True)  # 只保留附加信息中的符号
        # 确保符号不作为句子开头
        if extra_info and extra_info[0] in ",。！？；":
            extra_info = extra_info[1:].strip()
    else:
        extra_info = ""

    # 输出提取的信息
    print(f"建筑名称: {location_name}")
    print(f"地址: {address}")
    print(f"历史建筑批次: {batch}")
    print(f"额外信息: {extra_info}")

    # 返回适合 Neo4j 的三元组结构（建筑 -> 地址，建筑 -> 批次，建筑 -> 附加信息）
    return [
        {"subject": location_name, "predicate": "位于", "object": address},
        {"subject": location_name, "predicate": "属于", "object": batch},
        {"subject": location_name, "predicate": "附加信息", "object": extra_info}
    ]

# 批量处理 JSON 文件并保存三元组到文件
def process_json_file(file_path, output_file):
    print(f"正在处理文件: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        all_triplets = []
        for key, content in data.items():
            print(f"处理键: {key}, 内容: {content}")
            # 提取四个部分的信息并生成三元组
            triplets = extract_information(content)
            all_triplets.extend(triplets)
        
        # 保存三元组到指定文件
        with open(output_file, 'a', encoding='utf-8') as out_file:
            for triplet in all_triplets:
                json.dump(triplet, out_file, ensure_ascii=False)
                out_file.write('\n')

    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")

# 批量处理多个 JSON 文件
def process_multiple_json_files(folder_path, output_file):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            process_json_file(file_path, output_file)

# 定义要处理的文件夹路径
public_folder = "E:/项目/GIS/mars2d-vue-template-master/mars2d-vue3-vite/public/buildingDescriptions"

# 执行批量处理，保存三元组到 JSON 文件
process_multiple_json_files(public_folder, output_file)

print("三元组已经保存到文件:", output_file)
