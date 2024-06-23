import os
import asyncio
import logging
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from django.conf import settings
from postdata.models import UploadedFile
from .StructureAgent import StructureAgent
from .ContentAgent import ContentAgent
from .ReferenceAgent import ReferenceAgent

# basic config
load_dotenv(override=True)
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=300, api_key=os.getenv('OPENAI_API_KEY'))
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     handlers=[
#                         logging.FileHandler("debug_info_error.log"),
#                         logging.StreamHandler()
#                     ])

class Writer:
    def __init__(self, user):
        persist_dir = os.path.join(settings.MEDIA_ROOT, f"user_{user.id}", 'indexed_files')    
        self.use_reference = self.check_whether_reference(user)
        if self.use_reference:
            self.index, self.extra_info_dict = self.get_index(user, persist_dir)
            for file_base, info in self.extra_info_dict.items():
                print(info['summary'])
            # if not os.path.exists(persist_dir):
            #     self.index = self.generate_index(user, persist_dir)
            # else:
            #     self.index = self.load_index(persist_dir)

    def check_whether_reference(self, user):
        uploads = UploadedFile.objects.filter(user_name=user)
        count = uploads.count()
        print(f'reference count {count}')
        return False if count==0 else True
    
    def get_index(self, user, persist_dir):
        uploads = UploadedFile.objects.filter(user_name=user)
        url_list = set()
        text_list = set()
        for upload in uploads:
            if upload.text:
                text_list.add(upload.text)
            if upload.url:
                url_list.add(upload.url)
        user_id = user.id
        files_dir = os.path.join(settings.MEDIA_ROOT, f"user_{user_id}", 'original_files')    
        logging.info(f'text_list: {" ".join(text_list)}')
        logging.info(f'url_list: {" ".join(url_list)}')
        logging.info(f'files_dir: {files_dir}')
        if (not url_list) and (not text_list) and (not any(os.listdir(files_dir))):
            raise('loading references wrong!')
        RA = ReferenceAgent(persist_dir)
        index, extra_info_dict = asyncio.run(RA.index(url_list, text_list, files_dir))
        return index, extra_info_dict
    
    def write_outline(self, request_data):
        outline = self.generate_outline(request_data)
        logging.info(f"outline:{outline}")  
        return outline      
    
    def write_content(self,request_data):
        logging.info("writting content start!")
        content = self.generate_content(request_data)
        title = request_data['title']
        return title, content

    def generate_outline(self, request_data):
        SA = StructureAgent()       
        if self.use_reference:
            detailed_outline = SA.run_with_reference(title=request_data.get('title', ''),
                content_requirement=request_data.get('content_requirent', ''),
                niche=request_data.get('style', ''),
                length=request_data.get('length', ''),
                index=self.index,
                doc_info=self.extra_info_dict)
        else:
            detailed_outline = SA.run_without_reference(title=request_data.get('title', ''),
                content_requirement=request_data.get('content_requirent', ''),
                niche=request_data.get('style', ''),
                length=request_data.get('length', ''))
            logging.info('detailed outline finished!')
        return detailed_outline
    
    def generate_content(self, request_data):
        CA = ContentAgent()
        if self.use_reference:
            article = CA.run_reference(self.index, 
                                        content_requirement=request_data.get('content_requirent', ''), 
                                        niche=request_data.get('style', ''),
                                        outline=request_data.get('outline', ''))
        else:
            article = CA.run(content_requirement=request_data.get('content_requirent', ''), 
                            niche=request_data.get('style', ''),
                            outline=request_data.get('outline', ''))
        return article
    
    # def generate_prompt(self, prompt_details):
    #     print(prompt_details)
    #     prompt = '根据以下描述，必须使用中文，撰写一篇文章'
    #     if 'topic' in prompt_details and prompt_details['topic']:
    #         prompt += f"，关于{prompt_details['topic']}"
    #     if 'outline' in prompt_details and prompt_details['outline']:
    #         prompt += "，文章应包含以下几个部分： "
    #         for idx, point in enumerate(prompt_details['outline'], start=1):
    #             prompt += f"{idx}. {point}；"
    #     if 'primaryKeyword' in prompt_details and prompt_details['primaryKeyword']:
    #         prompt += f"确保文章内容围绕{prompt_details['primaryKeyword']}这一主题。"
    #     # if 'secondaryKeywords' in prompt_details and prompt_details['secondaryKeywords']:
    #     #     prompt += f"，同时涉及{prompt_details['secondaryKeywords']}这些关键词。"
    #     # else:
    #     #     prompt += "。"
    #     # if 'view' in prompt_details and prompt_details['view']:
    #     #     prompt += f"文章应该采用{prompt_details['view']}的人称。"
    #     # if 'tone' in prompt_details and prompt_details['tone']:
    #     #     prompt += f"文章应该采用{prompt_details['tone']}的语气。"
    #     if 'style' in prompt_details and prompt_details['style']:
    #         prompt += f"文章类型为： {prompt_details['style']}"
    #     prompt += "在文章中嵌入相关的事实材料以支持论述。"
    #     return prompt
    
    # def display_prompt_dict(prompts_dict):
    #     for k, p in prompts_dict.items():
    #         text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
    #         display(Markdown(text_md))
    #         print(p.get_template())
    #         display(Markdown("<br><br>"))

    # def section_write(self, description):
    #     print('使用分段落书写！')
    #     self.generate_index() 
    #     query_engine = self.index.as_chat_engine()  
    #     if 'outline' in description and description['outline']:
    #         sections_content = []
    #         for idx, section in enumerate(description['outline'], start=1):
    #             section_prompt = self.generate_section_prompt(section, idx, description)
    #             section_response = query_engine.chat(section_prompt)
    #             sections_content.append(f"{section_response.response}\n")
    #         full_article = "\n".join(sections_content)
    #         formated_article = self.format_and_correct_article(full_article)
    #         return formated_article
    #     else:
    #         return self.write(description)
    
    # def generate_section_prompt(self, section, index, description):
    #     prompt = f"根据以下描述，必须使用中文，撰写第 {index} 节的内容，标题为：{section}。"
    #     if 'topic' in description and description['topic']:
    #         prompt += f" 章节内容应与全文主题“{description['topic']}”相关。"
    #     if 'primaryKeyword' in description and description['primaryKeyword']:
    #         prompt += f" 请确保章节内容围绕“{description['primaryKeyword']}”这一主题。"
    #     if 'secondaryKeywords' in description and description['secondaryKeywords']:
    #         prompt += f" 同时请包含如下关键词：{', '.join(description['secondaryKeywords'])}。"
    #     if 'view' in description and description['view']:
    #         prompt += f" 请使用{description['view']}的人称书写。"
    #     if 'tone' in description and description['tone']:
    #         prompt += f" 请采用{description['tone']}的语气。"
    #     prompt += " 请在章节中嵌入相关的事实材料以支持论述，并使用Markdown格式进行排版，确保结构清晰。"
    #     return prompt