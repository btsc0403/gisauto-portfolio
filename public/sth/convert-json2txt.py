import os
import json

# 定义文件夹路径和输出文件路径
folder_path = r'E:\项目\GIS\mars2d-vue-template-master\mars2d-vue3-vite\public\buildingDescriptions'  # 修改为你的JSON文件夹路径
output_file_path = 'C:/Users/xjxl/Desktop/output.txt'


# 清空输出文件，准备写入数据
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write('')

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)

        # 读取每个JSON文件
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                json_data = json.load(json_file)

                # 将JSON内容转成字符串并写入TXT文件
                with open(output_file_path, 'a', encoding='utf-8') as output_file:
                    json.dump(json_data, output_file, ensure_ascii=False, indent=2)  # 格式化输出JSON
                    output_file.write('\n\n')
                print(f'已将 {file_name} 的内容写入TXT文件')

            except json.JSONDecodeError as e:
                print(f'无法解析文件 {file_name}: {e}')
