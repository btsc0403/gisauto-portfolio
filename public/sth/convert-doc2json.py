import os
import json
import re
from docx import Document

# 批次号映射：数字转汉字
def batch_number_to_chinese(batch_number):
    batch_map = {
        1: "第一批",
        2: "第二批",
        3: "第三批",
        4: "第四批",
        5: "第五批",
        6: "第六批",
        7: "第七批",
        8: "第八批",
        9: "第九批",
        10: "第十批",
        # 如果有更多批次，可以继续添加
    }
    return batch_map.get(batch_number, f"第{batch_number}批")  # 如果超出范围，直接返回类似“第11批”的格式

# 从.docx文件中提取表格内容
def extract_table_data(doc_path):
    doc = Document(doc_path)
    table_data = []
    
    # 遍历所有表格中的每一行
    for table in doc.tables:
        for row in table.rows:
            cells = row.cells
            # 获取表格中的每一行数据（假设每行有编号、所属区、建筑名称、地址四列）
            if len(cells) == 4:  # 如果有四列，按照顺序提取
                num = cells[0].text.strip()  # 编号
                district = cells[1].text.strip()  # 所属区
                name = cells[2].text.strip()  # 建筑名称
                address = cells[3].text.strip()  # 地址
                
                # 检查编号是否包含 '_'
                if "_" in num:
                    # 尝试从编号中提取批次号
                    batch_number = num.split('_')[1]
                    # 如果批次号无法转换为整数，跳过此行
                    try:
                        batch_number_int = int(batch_number)
                        batch = f"属于广州市{batch_number_to_chinese(batch_number_int)}历史建筑"
                    except ValueError:
                        batch = "批次信息缺失"
                else:
                    batch = "批次信息缺失"
                
                table_data.append((name, district, address, batch))
    
    return table_data

# 处理建筑名称为合法的文件名（去除非法字符）
def sanitize_filename(name):
    # 替换文件名中的非法字符
    return re.sub(r'[\\/:*?"<>|]', '_', name)

# 将每个建筑信息保存为单独的 JSON 文件
def save_to_json_files(building_data, output_folder):
    for name, district, address, batch in building_data:
        # 构造每个 JSON 文件的内容
        content = f"{name}位于{district}{address}，{batch}。"
        json_data = {"A2_content": content}
        
        # 将建筑名称作为文件名，确保合法文件名
        sanitized_name = sanitize_filename(name)
        
        # 文件路径（使用建筑名称作为文件名）
        file_path = os.path.join(output_folder, f"{sanitized_name}.json")
        
        # 保存为 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"已保存: {file_path}")

# 主函数
def main():
    input_path = r"C:\Users\xjxl\Desktop\广州市第一批历史建筑名单.docx"
    output_folder = r"C:\Users\xjxl\Desktop\建筑信息JSON"
    
    # 创建文件夹（如果文件夹不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 提取表格数据
    table_data = extract_table_data(input_path)

    # 保存每个建筑为独立的 JSON 文件
    save_to_json_files(table_data, output_folder)

if __name__ == "__main__":
    main()
