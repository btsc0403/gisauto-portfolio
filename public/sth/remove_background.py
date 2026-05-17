#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片背景移除工具
使用rembg库自动移除图片背景并保存为透明PNG格式
"""

import os
from rembg import remove
from PIL import Image
import argparse

def remove_background(input_path, output_path=None):
    """
    移除图片背景
    
    Args:
        input_path (str): 输入图片路径
        output_path (str): 输出图片路径，如果不指定则自动生成
    """
    try:
        # 读取输入图片
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        # 移除背景
        output_data = remove(input_data)
        
        # 确定输出路径
        if output_path is None:
            name, ext = os.path.splitext(input_path)
            output_path = f"{name}_transparent.png"
        
        # 保存结果
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        print(f"背景移除成功！输出文件：{output_path}")
        return output_path
        
    except Exception as e:
        print(f"处理失败：{str(e)}")
        return None

def batch_remove_background(input_folder, output_folder=None):
    """
    批量移除文件夹中所有图片的背景
    
    Args:
        input_folder (str): 输入文件夹路径
        output_folder (str): 输出文件夹路径
    """
    if output_folder is None:
        output_folder = f"{input_folder}_transparent"
    
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    
    # 支持的图片格式
    supported_formats = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
    
    # 处理文件夹中的所有图片
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_transparent.png")
            
            print(f"正在处理：{filename}")
            remove_background(input_path, output_path)

def main():
    parser = argparse.ArgumentParser(description='移除图片背景工具')
    parser.add_argument('input', help='输入图片文件或文件夹路径')
    parser.add_argument('-o', '--output', help='输出路径')
    parser.add_argument('-b', '--batch', action='store_true', help='批量处理模式')
    
    args = parser.parse_args()
    
    if args.batch:
        batch_remove_background(args.input, args.output)
    else:
        remove_background(args.input, args.output)

if __name__ == "__main__":
    # 如果直接运行脚本，处理当前目录的KGlogo.png
    if os.path.exists("src/KGlogo.png"):
        print("发现KGlogo.png，开始处理...")
        result = remove_background("src/KGlogo.png", "src/KGlogo_transparent.png")
        if result:
            print("KGlogo背景移除完成！")
    else:
        main() 