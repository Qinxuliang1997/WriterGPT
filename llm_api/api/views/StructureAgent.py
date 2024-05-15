from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from typing import List
from dotenv import load_dotenv
import os

import asyncio
from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser 
from langchain_openai import OpenAI
from langchain_core.runnables import RunnablePassthrough

load_dotenv(override=True)
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0, api_key=os.getenv('OPENAI_API_KEY'), max_tokens=1000)

class Paragraph(BaseModel):
    paragraph: str

class Section(BaseModel):
    title: str = Field(..., description="小节的标题")
    length: str = Field(..., description="本小节的长度")
    paragraphs: List[str] = Field(..., description="当前小节中，每个段落的主旨")

class Outline(BaseModel):
    outline: List[Section]

class StructureAgent:
    def __init__(self, outline: list) -> None:
        self.outline = outline

    def run(self, title, content_requirement, niche, length):
        # if self.outline:
        #     return self.write_article_structure_with_outline(title, content_requirement, niche, length)
        # else:
        return self.write_article_structure_without_outline(title, content_requirement, niche, length)

    def write_article_structure_with_outline(self, title: str, content_requirement: str, niche: str, length: str):
        outline = self.get_outline_text(self.outline)
        print(outline)
        parser = PydanticOutputParser(pydantic_object=Outline)
        prompt = PromptTemplate(
            template="假如你是一个优秀的中文作家，请你使用中文为下面的文章拟定一个全面的、丰富的提纲，不同部分之间内容不可以重复.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        prompt_and_model = prompt | model
        output = prompt_and_model.invoke({"query": f"已知文章的标题{title}，每个部分的标题{outline}，文章的风格{niche}， 文章的要求{content_requirement}, 以及全文的长度为{length}字。要求： 1.将全文的长度划分到文章的每个部分中，给出该部分的字数；2.根据文章和关键词和每个部分的标题，将该部分的内容分为多个段落，然后给出每个段落中需要写的内容。"})
        outline_instance = parser.invoke(output)
        return self.convert_sections_to_dict(outline_instance.outline)

    def write_article_structure_without_outline(self, title: str, content_requirement: str, niche: str, length: str):
        parser = PydanticOutputParser(pydantic_object=Outline)
        prompt = PromptTemplate(
            template="假如你是一个优秀的中文作家，请你使用中文为下面的文章拟定一个全面的、丰富的提纲，不同部分之间内容不可以重复.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        prompt_and_model = prompt | model
        output = prompt_and_model.invoke({"query": f"已知文章的标题{title}，文章的风格{niche}， 文章的要求{content_requirement}， 以及全文的长度为{length}字。要求： 1.根据文章的关键词和风格，将全文划分分3-5个不同的部分，每个部分有一个确定的主题；2.将全文的长度划分到文章的每个部分中，给出该部分的字数；3.根据文章和关键词和每个部分的标题，将该部分的内容分为多个段落，然后给出每个段落中需要写的内容。"})
        outline_instance = parser.invoke(output)
        return self.convert_sections_to_dict(outline_instance.outline)
 
    def write_article_structure_without_outline_openai_func(self, keyword: str, niche: str, number: int) -> Any:
        parser = JsonOutputFunctionsParser()
        function = {
            'name': 'outline',
            'description': 'Writes outline for an given article keyword.',
            'parameters': {
                'type': 'object',
                'properties': {
                    "keyword": {
                        "type": "string",
                        "description": "The keyword for which the article outline is generated.",
                    },
                    'outline': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'title': {
                                    'type': 'string',
                                    'description': 'title of the section',
                                },
                                'paragraphs': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'string',
                                    },
                                    'description': 'an array of strings representing title of each paragraph in the section',
                                },
                            },
                        },
                    },
                },
                'required': ['keyword','outline'],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"Write a 2000 word article outline for the following keyword. \nArticle niche: {niche}. Language: Chinese",
                ),
                ("human", keyword),
            ]
        )
        model = ChatOpenAI(model="gpt-4", temperature=0, api_key='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').bind(
            function_call= {'name': 'outline'},
            functions=[function],
        )
        runnable = {'keyword': RunnablePassthrough()} | prompt | model | parser
        result = runnable.invoke(
            keyword
        )
        return result

    def convert_sections_to_dict(self, sections):
        outline = {}
        for index, section in enumerate(sections):
            section_key = f'小节 {index + 1}'
            outline[section_key] = {
                'title': section.title,
                'paragraphs': {},
                'length':  section.length,
            }
            for para_index, paragraph in enumerate(section.paragraphs):
                paragraph_key = f'段落 {para_index + 1}'
                outline[section_key]['paragraphs'][paragraph_key] = {'content': paragraph}
        return outline
    
    def get_outline_text(self, dict):
        outline_text = []
        for part, section in dict.items():
            section_title = section['title'] + '('
            for part,paragraphs in section['paragraphs'].items():
                section_title += paragraphs['content'] + '，'
            section_title += ")"
        outline_text.append(section_title)
        return outline_text

if __name__ == "__main__":
    outline = {'小节 1': {'title': '引言', 'paragraphs': {'段落 1': {'content': '介绍低空经济的概念和背景'}, '段落 2': {'content': '分析低空经济对国内外经济发展的重要性'}, '段落 3': {'content': '提出本文的研究目的和意义'}}, 'length': '500字'}, '小节 2': {'title': '国内低空经济发展现状', 'length': 300, 'paragraphs': {'段落 1': {'content': '分析国内低空经济的发展历程'}, '段落 2': {'content': '探讨国内低空经济的主要特点和现状'}, '段落 3': {'content': '比较国内低空经济与国外的差距和发展趋势'}}, 'length': '800字'}, '小节 3': {'title': '国外低空经济发展现状', 'paragraphs': {'段落 1': {'content': '介绍国外低空经济的发展情况'}, '段落 2': {'content': '分析国外低空经济的发展模式和特点'}, '段落 3': {'content': '探讨国外低空经济对国际经济的影响'}}, 'length': '800字'}, '小节 4': {'title': '低空经济发展趋势', 'paragraphs': {'段落 1': {'content': '预测未来低空经济的发展趋势和方向'}, '段落 2': {'content': '分析低空经济发展可能面临的挑战和机遇'}, '段落 3': {'content': '提出促进低空经济发展的建议和措施'}}, 'length': '700字'}}
    SA = StructureAgent(outline)
    # SA = StructureAgent(None)
    outline = SA.run('低空经济国内外发展现状','结果国内外低空经济发展现状', '行业研究报告', 3000)
    print(outline)
    # outline_dic = SA.convert_sections_to_dict(outline)
    # print(outline_dic)
    # for section in outline:
    #     print("Title:", section.title)
    #     print("Length", section.length)
    #     for paragraph in section.paragraphs:
    #         print("Paragraph:", paragraph)