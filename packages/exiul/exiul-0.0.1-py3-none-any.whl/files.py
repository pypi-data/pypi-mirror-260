import os
import re


def find_file(path: str, pattern: str):
    """查找文件"""
    # 判断路径是文件
    if os.path.isfile(path) and re.findall(pattern, os.path.basename(path)):
        return path
    sub_files = os.listdir(path)
    for sub_file in sub_files:
        sub_path = os.path.join(path, sub_file)
        if os.path.isfile(sub_path):
            if re.findall(pattern, sub_file):
                return sub_path
        elif os.path.isdir(sub_path):
            return find_file(sub_path, pattern)
    return None
