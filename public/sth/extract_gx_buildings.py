#!/usr/bin/env python3
"""
提取广西历史建筑数据脚本
从public/GXbuildingsData/tmp/tmp/历史建筑/目录下的所有JSON文件中提取coordinate和historicalBuildName
"""

import os
import json
import glob

def extract_building_data():
    """提取所有历史建筑的坐标和名称"""
    base_path = "public/GXbuildingsData/tmp/tmp/历史建筑"
    buildings = []
    
    # 使用glob递归查找所有JSON文件
    json_files = glob.glob(os.path.join(base_path, "**", "*.json"), recursive=True)
    
    print(f"找到 {len(json_files)} 个JSON文件")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 提取数据
            if 'data' in data:
                building_data = data['data']
                name = building_data.get('historicalBuildName', '')
                coordinate = building_data.get('coordinate', '')
                city = building_data.get('city', '')
                county = building_data.get('county', '')
                
                # 解析坐标
                if coordinate and ',' in coordinate:
                    lng, lat = coordinate.split(',')
                    try:
                        lat_float = float(lat.strip())
                        lng_float = float(lng.strip())
                        
                        if name:  # 确保名称不为空
                            buildings.append({
                                'label': name,
                                'lat': lat_float,
                                'lng': lng_float,
                                'city': city,
                                'county': county,
                                'file_path': json_file
                            })
                    except ValueError:
                        print(f"坐标格式错误: {coordinate} in file {json_file}")
                        
        except Exception as e:
            print(f"处理文件 {json_file} 时出错: {e}")
    
    print(f"成功提取 {len(buildings)} 个建筑信息")
    return buildings

def generate_vue_format(buildings):
    """生成Vue文件格式的代码"""
    lines = []
    lines.append("  {")
    lines.append("    label: \"GX Buildings\",")
    lines.append("    visible: false,")
    lines.append("    items: [")
    
    for building in buildings:
        line = f"      {{ label: \"{building['label']}\", lat: {building['lat']}, lng: {building['lng']} }},"
        lines.append(line)
    
    lines.append("    ]")
    lines.append("  },")
    
    return "\n".join(lines)

def main():
    """主函数"""
    print("开始提取广西历史建筑数据...")
    
    # 提取建筑数据
    buildings = extract_building_data()
    
    if not buildings:
        print("没有找到任何建筑数据")
        return
    
    # 生成Vue格式代码
    vue_code = generate_vue_format(buildings)
    
    # 保存到文件
    with open("gx_buildings_vue_code.txt", "w", encoding="utf-8") as f:
        f.write(vue_code)
    
    print(f"Vue代码已保存到 gx_buildings_vue_code.txt")
    print(f"总共 {len(buildings)} 个建筑")
    
    # 显示前5个建筑作为示例
    print("\n前5个建筑示例:")
    for i, building in enumerate(buildings[:5]):
        print(f"{i+1}. {building['label']} - ({building['lat']}, {building['lng']}) - {building['city']}{building['county']}")
    
    # 保存完整的JSON数据用于备份
    with open("gx_buildings_full_data.json", "w", encoding="utf-8") as f:
        json.dump(buildings, f, ensure_ascii=False, indent=2)
    
    print("完整数据已保存到 gx_buildings_full_data.json")

if __name__ == "__main__":
    main()
