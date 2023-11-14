from urllib.parse import urlparse
import os

def generate_unique_filename(url, output_path):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    
    # 提取路径中的文件名
    filename = path.split('/')[-1]
    
    # 如果路径中没有文件名，则使用域名作为文件名
    if not filename:
        filename = domain
    
    # 如果文件名已存在，则在文件名后面添加一个计数器
    counter = 1
    while os.path.exists(os.path.join(output_path, filename)):
        filename = f"{filename}_{counter}"
        counter += 1
    
    return filename

# 示例用法
# url = "http://example.com/documents/document.pdf"
# filename = generate_unique_filename(url)
# print(filename)