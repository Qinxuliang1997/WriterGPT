# import os
# from django.conf import settings
# from postdata.models import UploadedFile
import logging
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from llama_index.core import Settings
import os
from llama_index.core.llms import ChatMessage

# from llama_index.core import VectorStoreIndex

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     handlers=[
#                         logging.FileHandler("debug_info_error.log"),
#                         logging.StreamHandler()
#                     ])

class ModifyAgent:
    def __init__(self):
        load_dotenv(override=True)
        self.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=2000, api_key=os.getenv('OPENAI_API_KEY'))
    
    def modify(self, request_data):
        logging.info(f"selected text: {request_data['originalText']}")
        logging.info(f"user prompt: {request_data['userInput']}")
        logging.info("writting start!")
        print(request_data)
        modified_text = self.modify_text(request_data['style'], request_data['primaryKeyword'], request_data['userInput'], request_data['originalText'])
        logging.info("writting done!")
        return modified_text

    def modify_text(self, niche, keyword, user_prompt, original_text):
        template = ("你是一名资深内容编辑，现在需要你根据用户的要求修改一篇文章中的一段话。"
                    "你需要直接返回修改后的文字。文章中不得暴露这是人工智能生成的内容。不要添加如“引言”、“结论”等标签。文字使用中文。"
                    "你将获得关于全文的描述（风格、关键词）以及用户关于如何修改这段话的要求。"
                    "根据这些信息撰写段落。")
        human_template = f"领域: {niche}, 关键词: {keyword}, 要求: {user_prompt}, 原文: {original_text}"
        return self.call_gpt(template,
                                    human_template,
                                    )

    def call_gpt(self, template, human_template):
        logging.info('start modifying')
        messages = [
            ChatMessage(
                role="system", content=template
            ), 
            ChatMessage(role="user", content=human_template),
        ]
        response =self.llm.chat(messages)
        modified_text =response.message.content
        return modified_text

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
    
    # def format_and_correct_article(self, article):
        # prompt = f"请将以下文章内容转换为正确的 Markdown 格式，并修正任何明显的写作错误，返回修正后的文章，除文章外不要返回其他任何内容：({article})"
        # try:
        #     response = client.completions.create(engine="gpt-3.5-turbo-1106",
        #     prompt=prompt,
        #     temperature=0.5,
        #     max_tokens=4000, 
        #     api_key=os.getenv("OPENAI_API_KEY"))
        #     return response.choices[0].text.strip()
        # except Exception as e:
#             print(f"Error during API call: {e}")
#             return article