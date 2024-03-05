import os
from django.conf import settings
from postdata.models import UploadedFile
from .create_node import *

import llama_index
from llama_index.llms import OpenAI
from llama_index import (VectorStoreIndex, 
                         ServiceContext, 
                         set_global_service_context,
                         )

llama_index.set_global_handler("simple")
# define LLM
llm = OpenAI(model="gpt-3.5-turbo-1106", temperature=0, max_tokens=4000, api_key=os.getenv("OPENAI_API_KEY"))
# configure service context
service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context)

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
            node = create_node_url(url_list)
            self.index.insert_nodes(node)
        if text_list:
            node = create_node_text(text_list)
            self.index.insert_nodes(node)
        if os.listdir(files_dir):
            node = create_node_dir(files_dir)
            self.index.insert_nodes(node)

    def generate_prompt(self, prompt_details):
        prompt = '请根据以下描述，使用中文，撰写一篇文章'
        if 'topic' in prompt_details and prompt_details['topic']:
            prompt += f"，关于{prompt_details['topic']}"
        if 'outline' in prompt_details and prompt_details['outline']:
            prompt += "，文章应包含以下几个部分： "
            for idx, point in enumerate(prompt_details['outline'], start=1):
                prompt += f"{idx}. {point}；"
        if 'primaryKeyword' in prompt_details and prompt_details['primaryKeyword']:
            prompt += f"请确保文章内容围绕{prompt_details['primaryKeyword']}这一主题"
        if 'secondaryKeywords' in prompt_details and prompt_details['secondaryKeywords']:
            prompt += f"，同时涉及{prompt_details['secondaryKeywords']}这些关键词。"
        else:
            prompt += "。"
        if 'view' in prompt_details and prompt_details['view']:
            prompt += f"文章应该采用{prompt_details['view']}的人称。"
        if 'tone' in prompt_details and prompt_details['tone']:
            prompt += f"文章应该采用{prompt_details['tone']}的语气。"
        prompt += "在文章中嵌入相关的事实材料以支持论述。最后，请使用Markdown格式进行排版，确保文章结构清晰。"
        return prompt

    def write(self, description):
        prompt = self.generate_prompt(description)
        self.generate_index()
        query_engine = self.index.as_chat_engine()
        response = query_engine.chat(prompt)
        return response.response
