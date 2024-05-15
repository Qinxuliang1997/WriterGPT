import os
import logging
import sys
from dotenv import load_dotenv
from typing import Dict, List, Any
from llama_index.llms.openai import OpenAI
from llama_index.core import (VectorStoreIndex, 
                              Settings, 
                            )
import json

# from IPython.display import Markdown, display

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class ContentAgent:
    def __init__(self):
        load_dotenv(override=True)
        Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=300, api_key=os.getenv('OPENAI_API_KEY'))

    def run(self, index, content_requirement, niche, outline):
        sections_dict = {}
        section_index = 1
        for section_key, section in outline.items():
            chinese_index = self.number_to_chinese(section_index)
            updated_title = f"{chinese_index}、{section['title']}"
            section_dict = {}
            paragraph_index = 1
            for paragraph_key, paragraph in section['paragraphs'].items():
                written_paragraph = self.write_paragraph(
                    niche=niche,
                    content_requirement=content_requirement,
                    title=section['title'],
                    paragraph=paragraph['content'],
                    index=index
                )
                section_dict[f"段落 {paragraph_index}"] = {
                    "content": written_paragraph,
                    "word_count": len(written_paragraph)
                }
                paragraph_index += 1
            sections_dict[f"小节 {section_index}"] = {
                "title": updated_title,
                "paragraphs": section_dict
            }
            section_index += 1
        # for section_index, section in enumerate(outline, start=1):
        #     chinese_index = self.number_to_chinese(section_index)
        #     updated_title = f"{chinese_index}、{outline[section]['title']}"
        #     section_dict = {}
        #     for paragraph_index, paragraph in enumerate(outline[section]['paragraphs'], start=1):
        #         logging.info(f"Writing section {outline[section]['title']}, paragraph {paragraph_index}")
        #         written_paragraph = self.write_paragraph(
        #             niche=niche,
        #             content_requirement=content_requirement,
        #             title=section.title,
        #             paragraph=outline[section]['paragraphs'][paragraph]['content'],
        #             index=index
        #         )
        #         section_dict[f"段落 {paragraph_index}"] = {
        #             "content": written_paragraph,
        #             "word_count": len(written_paragraph)
        #         }
        #         logging.info(f"Done writing paragraph, {len(written_paragraph)} words")
        #     sections_dict[f"小节 {section_index}"] = {
        #         "title": updated_title,
        #         "paragraphs": section_dict
        #     }
        # article_data = self.serialize_dic(section_dict)
        return sections_dict

    def run_old(self, index, keyword, niche, outline):
        sections = []
        for section in outline:
            paragraphs = []
            logging.info("Writing section", section.title)
            for paragraph in section.paragraphs:
                logging.info(f"Writing paragraph: {paragraph}")
                written_paragraph = self.write_paragraph(
                    niche=niche,
                    keyword=keyword,
                    title=section.title,
                    paragraph=paragraph,
                    index = index,
                )
                paragraphs.append(written_paragraph)
                logging.info(f"Done writing paragraph, {len(written_paragraph)} words")
            sections.append((section.title, paragraphs))
        article_text = self.join_article(sections)
        return article_text

    def write_paragraph(self, niche, content_requirement, title, paragraph, index):
        template = ("你是一名资深内容撰稿人，现在需要你根据段落描述完成一篇文章中的一个段落。"
                    "文章中不得暴露这是人工智能生成的内容。不要添加如“引言”、“结论”等标签。文字使用中文。"
                    "段落必须非常专业且富有情感。你将获得关于全文的描述（风格、关键词），关于这个部分的描述（标题），以及这段话的描述。"
                    "根据这些信息撰写段落。")
        human_template = f"领域: {niche}, 内容要求: {content_requirement}, 段落标题: {title}, 段落描述: {paragraph}"
        return self.call_llamaindex(template,
                                    human_template,
                                    index
                                    )
    
    def call_llamaindex(self, template, human_template, index):
        logging.info('start using llamaindex')
        prompt = template + human_template
        query_engine = index.as_query_engine()
        # prompts_dict = query_engine.get_prompts()
        # self.display_prompt_dict(prompts_dict)
        response = query_engine.query(prompt)
        paragraph_content = response.response
        return paragraph_content

    def join_article(self, sections: List[Dict[str, str]]) -> str:
        article = ""
        for title, paragraphs in sections:
            article += title
            article += "\n"
            article += "\n".join(paragraphs)
            article += "\n"
        return article
    
    def serialize_dic(self, data):
        json_data = json.dumps(data, indent=None, separators=(',', ':'))
        return json_data

    def number_to_chinese(self, number):
        chinese_numerals = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
        if 1 <= number <= 10:
            return chinese_numerals[number]
        elif number > 10:
            return str(number)
