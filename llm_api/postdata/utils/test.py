# from pathlib import Path
# from llama_index import download_loader

# PDFReader = download_loader("PDFReader")

# loader = PDFReader()
# documents = loader.load_data(file=Path('../articles/us-tmt-semiconductor-industry-outlook.pdf'))

# print(documents)

import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件所在的目录路径
current_directory_path = os.path.dirname(current_file_path)

# 获取当前目录的上一级目录路径
top_level_package_path = os.path.dirname(current_directory_path)

print("当前项目的顶级包路径：", top_level_package_path)