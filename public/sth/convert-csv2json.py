import os
import csv

def clear_first_row_content(folder_path, output_folder):
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csv_path = os.path.join(folder_path, filename)
            
            # 打开CSV文件并读取内容
            with open(csv_path, mode='r', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                rows = list(csvreader)
                
                # 清空第一行的内容（保留第一行的字段名）
                if rows:
                    rows[0] = [''] * len(rows[0])  # 清空第一行的所有内容，保留字段名
                
                # 准备新的CSV文件路径
                new_csv_filename = os.path.splitext(filename)[0] + '_modified.csv'
                new_csv_path = os.path.join(output_folder, new_csv_filename)

                # 将修改后的内容写入新的CSV文件
                with open(new_csv_path, mode='w', newline='', encoding='utf-8') as new_csvfile:
                    csvwriter = csv.writer(new_csvfile)
                    csvwriter.writerows(rows)
                
                print(f"{filename} 的第一行内容已删除，并保存为 {new_csv_filename} 在 {output_folder}")

# 调用函数，将“your_folder_path”替换为你的文件夹路径，“output_folder_path”替换为目标文件夹路径
clear_first_row_content(r'E:\项目\GIS\mars2d-vue-template-master\mars2d-vue3-vite\public\csv_output', r'E:\项目\GIS\mars2d-vue-template-master\mars2d-vue3-vite\public\csv_output_modified')
