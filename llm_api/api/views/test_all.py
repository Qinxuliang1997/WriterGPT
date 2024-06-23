from ReferenceAgent import ReferenceAgent
from StructureAgent import StructureAgent
from ContentAgent import ContentAgent
import os
import asyncio


RA = ReferenceAgent('./data/llamaindex_docs')
url_list = set(['https://www.sohu.com/a/699520214_468661'])
text_list = set()
files_dir = os.path.join("../../media", "user_1", 'original_files')    
output_path =  os.path.join("../../media", "user_1", 'indexed_files') 
all_doc_index, extra_info_dict = asyncio.run(RA.index(url_list, text_list, files_dir))
for file_base, info in extra_info_dict.items():
    print(info['summary'])

SA = StructureAgent()
outline = SA.run_with_reference(title='全球及中国低空经济产业发展情况',
                                content_requirement='介绍低空经济的定义、全球低空经济产业发展情况、中国低空经济产业发展情况', 
                                niche='行业研究报告', 
                                length=3000,
                                index=all_doc_index,
                                doc_info=extra_info_dict)
print(outline)

CA = ContentAgent()
content = CA.run_reference_section(
                            index=all_doc_index,
                            content_requirement='介绍低空经济的定义、全球低空经济产业发展情况、中国低空经济产业发展情况', 
                            niche='行业研究报告',
                            outline=outline)

print(content)

