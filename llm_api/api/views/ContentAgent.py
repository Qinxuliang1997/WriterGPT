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
from llama_index.core.llms import ChatMessage

# from IPython.display import Markdown, display

class ContentAgent: 
    def __init__(self):
        pass

    def run(self, content_requirement, niche, outline):
        sections_dict = {}
        section_index = 1
        complete_article = ""
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
                    complete_article=complete_article
                )
                complete_article += written_paragraph + "\n"
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
        return sections_dict

    def run_reference(self, index, content_requirement, niche, outline):
        sections_dict = {}
        section_index = 1
        complete_article = ""
        for section_key, section in outline.items():
            chinese_index = self.number_to_chinese(section_index)
            updated_title = f"{chinese_index}、{section['title']}"
            section_dict = {}
            paragraph_index = 1
            for paragraph_key, paragraph in section['paragraphs'].items():
                written_paragraph = self.write_paragraph_reference(
                    niche=niche,
                    content_requirement=content_requirement,
                    title=section['title'],
                    paragraph=paragraph['content'],
                    index=index,
                    complete_article=complete_article
                )
                complete_article += written_paragraph + "\n"
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
        return sections_dict

    def run_reference_section(self, index, content_requirement, niche, outline):
        sections_dict = {}
        section_index = 1
        complete_article = ""
        for section_key, section in outline.items():
            chinese_index = self.number_to_chinese(section_index)
            updated_title = f"{chinese_index}、{section['title']}"
            section_length = section['length']
            section_content = self.write_section(
                niche=niche,
                content_requirement=content_requirement,
                title=section['title'],
                index=index,
                complete_article=complete_article,
                length = section_length)
            complete_article += section_content + '\n'

            section_dict = {}
            paragraph_index = 1
            for paragraph in list(section_content.split('\n')):
                if len(paragraph) == 0:
                    continue
                section_dict[f"段落 {paragraph_index}"] = {
                    "content": paragraph,
                    "word_count": len(paragraph)
                }
                paragraph_index += 1
            sections_dict[f"小节 {section_index}"] = {
                "title": updated_title,
                "paragraphs": section_dict
            }
            section_index += 1
        return sections_dict

    def write_paragraph(self, niche, content_requirement, title, paragraph, complete_article):
        template = ("你是一名资深内容撰稿人，现在需要你根据段落描述完成一篇文章中的一个段落。"
                    "文章中不得暴露这是人工智能生成的内容。不要添加如“引言”、“结论”等标签。文字使用中文。"
                    "段落必须非常专业且富有情感。你将获得文章的类型，以及这段话的描述。"
                    "根据这些信息撰写段落。")
        human_template = f"文章类型: {niche}, 已写内容: {complete_article}, 段落描述: {paragraph}"
        return self.call_llm(template,
                            human_template,)
    
    def write_paragraph_reference(self, niche, content_requirement, title, paragraph, index, complete_article):
        template = ("你是一名资深内容撰稿人，现在你必须根据要求撰写一段话。要求："
                    f"1.风格要求：符合{niche}类型的文章的写作风格。"
                    f"2.内容要求：严格遵照这段话的内容说明（ {paragraph}），摘录并整理参考资料中与这段话内容相关的文字，注意不要与已写内容重复、连接顺畅。"
                    "3.其他要求：不得暴露这是人工智能生成的内容。"
                    "4.不要添加除内容外的任何描述。"
                    "5. 使用中文。")
        logging.info('start using llamaindex')
        # query_engine = index.as_query_engine()
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(paragraph)
        paragraph_context = [node.node.text.replace("\n", "") for node in nodes]
        print(paragraph, paragraph_context)
        human_template = f"已写内容: {complete_article}, 参考资料: {' '.join(paragraph_context)}"
        paragraph_content = self.call_llm(template, human_template)
        return paragraph_content
    
    def write_section(self, niche, content_requirement, title, index,  complete_article, length):
        template = ("你是一名资深内容撰稿人，现在需要你根据小节标题完成一篇文章中的一个小节。"
                    "文章中不得暴露这是人工智能生成的内容。不要添加除内容外的任何描述。不要添加如“引言”、“结论”等标签。使用中文。"
                    "小节必须非常专业且富有情感。你将获得文章的类型，这个小节的标题，已经完成的部分，参考资料，以及这个小节的长度。"
                    "根据这些信息撰写小节。")
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(title)
        paragraph_context = [node.node.text.replace("\n", "") for node in nodes]
        human_template = (f"文章类型: {niche}"
                          f"已写内容: {complete_article}"
                          f"参考资料: {' '.join(paragraph_context)}"
                          f"小节标题: {title}"
                          f"长度: {length}")
        return self.call_llm(template, human_template)

    def call_llm(self, template, human_template):
        load_dotenv(override=True)
        llm = OpenAI(model="gpt-4o", temperature=0, max_tokens=1500, api_key=os.getenv('OPENAI_API_KEY'))
        messages = [
            ChatMessage(
                role="system", content=template
            ), 
            ChatMessage(role="user", content=human_template),
        ]
        response = llm.chat(messages)
        content =response.message.content
        return content

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