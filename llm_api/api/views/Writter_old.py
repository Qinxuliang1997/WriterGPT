import os
from django.conf import settings
from postdata.models import UploadedFile
from .create_node import *
from openai import OpenAI

client = OpenAI()
from llama_index.llms.openai import OpenAI
from llama_index.core import (VectorStoreIndex, 
                              Settings, 
                            )
import logging
import sys
from IPython.display import Markdown, display

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# llama_index.core.set_global_handler("simple")
# define LLM
llm = OpenAI(model="gpt-4", temperature=0, max_tokens=4000, api_key=os.getenv("OPENAI_API_KEY"))
Settings.llm = llm

# configure service context
# service_context = ServiceContext.from_defaults(llm=llm)
# set_global_service_context(service_context)

class ContentAgent:
    def __init__(self, user):
        self.user = user
        self.index = VectorStoreIndex([])
    
    def generate_index(self):
        uploads = UploadedFile.objects.filter(user_name=self.user)
        url_list = set()
        text_list = set()
        for upload in uploads:
            if upload.text:
                text_list.add(upload.text)
            if upload.url:
                url_list.add(upload.url)
        user_id = self.user.id
        files_dir = os.path.join(settings.MEDIA_ROOT, f"user_{user_id}", 'original_files')    
        print(f'text_list: {" ".join(text_list)}')
        print(f'url_list: {" ".join(url_list)}')
        print(f'files_dir: {files_dir}')

        if url_list:
            node = create_node_url(list(url_list))
            self.index.insert_nodes(node)
        if text_list:
            node = create_node_text(list(text_list))
            self.index.insert_nodes(node)
        if os.listdir(files_dir):
            node = create_node_dir(files_dir)
            self.index.insert_nodes(node)

    def generate_prompt(self, prompt_details):
        prompt = '根据以下描述，必须使用中文，撰写一篇文章'
        if 'topic' in prompt_details and prompt_details['topic']:
            prompt += f"，关于{prompt_details['topic']}"
        if 'outline' in prompt_details and prompt_details['outline']:
            prompt += "，文章应包含以下几个部分： "
            for idx, point in enumerate(prompt_details['outline'], start=1):
                prompt += f"{idx}. {point}；"
        if 'primaryKeyword' in prompt_details and prompt_details['primaryKeyword']:
            prompt += f"确保文章内容围绕{prompt_details['primaryKeyword']}这一主题"
        if 'secondaryKeywords' in prompt_details and prompt_details['secondaryKeywords']:
            prompt += f"，同时涉及{prompt_details['secondaryKeywords']}这些关键词。"
        else:
            prompt += "。"
        if 'view' in prompt_details and prompt_details['view']:
            prompt += f"文章应该采用{prompt_details['view']}的人称。"
        if 'tone' in prompt_details and prompt_details['tone']:
            prompt += f"文章应该采用{prompt_details['tone']}的语气。"
        prompt += "在文章中嵌入相关的事实材料以支持论述。"
        return prompt
    
    def display_prompt_dict(prompts_dict):
        for k, p in prompts_dict.items():
            text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
            display(Markdown(text_md))
            print(p.get_template())
            display(Markdown("<br><br>"))
    
    def write(self, description):
        print('使用全文书写！')
        prompt = self.generate_prompt(description)
        self.generate_index()
        query_engine = self.index.as_query_engine()
        prompts_dict = query_engine.get_prompts()
        self.display_prompt_dict(prompts_dict)
        response = query_engine.query(prompt)
        article = response.response
        formated_article = self.format_and_correct_article(article)
        return formated_article
        # return ""

    def section_write(self, description):
        print('使用分段落书写！')
        self.generate_index() 
        query_engine = self.index.as_chat_engine()  
        if 'outline' in description and description['outline']:
            sections_content = []
            for idx, section in enumerate(description['outline'], start=1):
                section_prompt = self.generate_section_prompt(section, idx, description)
                section_response = query_engine.chat(section_prompt)
                sections_content.append(f"{section_response.response}\n")
            full_article = "\n".join(sections_content)
            formated_article = self.format_and_correct_article(full_article)
            return formated_article
        else:
            return self.write(description)
    
    def generate_section_prompt(self, section, index, description):
        prompt = f"根据以下描述，必须使用中文，撰写第 {index} 节的内容，标题为：{section}。"
        if 'topic' in description and description['topic']:
            prompt += f" 章节内容应与全文主题“{description['topic']}”相关。"
        if 'primaryKeyword' in description and description['primaryKeyword']:
            prompt += f" 请确保章节内容围绕“{description['primaryKeyword']}”这一主题。"
        if 'secondaryKeywords' in description and description['secondaryKeywords']:
            prompt += f" 同时请包含如下关键词：{', '.join(description['secondaryKeywords'])}。"
        if 'view' in description and description['view']:
            prompt += f" 请使用{description['view']}的人称书写。"
        if 'tone' in description and description['tone']:
            prompt += f" 请采用{description['tone']}的语气。"
        prompt += " 请在章节中嵌入相关的事实材料以支持论述，并使用Markdown格式进行排版，确保结构清晰。"
        return prompt
    
    def format_and_correct_article(self, article):
        prompt = f"请将以下文章内容转换为正确的 Markdown 格式，并修正任何明显的写作错误，返回修正后的文章，除文章外不要返回其他任何内容：({article})"
        try:
            response = client.completions.create(engine="gpt-3.5-turbo-1106",
            prompt=prompt,
            temperature=0.5,
            max_tokens=4000, 
            api_key=os.getenv("OPENAI_API_KEY"))
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error during API call: {e}")
            return article