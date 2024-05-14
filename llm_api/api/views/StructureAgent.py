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

    def run(self, keyword, niche, length):
        if self.outline:
            return self.write_article_structure_with_outline(keyword, niche, length)
        else:
            return self.write_article_structure_without_outline(keyword, niche, length)

    def write_article_structure_with_outline(self, keyword: str, niche: str, length: int):
        parser = PydanticOutputParser(pydantic_object=Outline)
        prompt = PromptTemplate(
            template="假如你是一个优秀的中文作家，请你使用中文为下面的文章拟定一个全面的、丰富的提纲，不同部分之间内容不可以重复.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        prompt_and_model = prompt | model
        output = prompt_and_model.invoke({"query": f"已知文章的关键词{keyword}，每个部分的标题{self.outline}，文章的风格{niche}， 以及全文的长度为{length}字。要求： 1.将全文的长度划分到文章的每个部分中，给出该部分的字数；2.根据文章和关键词和每个部分的标题，将该部分的内容分为多个段落，然后给出每个段落中需要写的内容。"})
        outline_instance = parser.invoke(output)
        return outline_instance.outline

    def write_article_structure_without_outline(self,keyword: str, niche: str, length: int):
        parser = PydanticOutputParser(pydantic_object=Outline)
        prompt = PromptTemplate(
            template="假如你是一个优秀的中文作家，请你使用中文为下面的文章拟定一个全面的、丰富的提纲，不同部分之间内容不可以重复.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        prompt_and_model = prompt | model
        output = prompt_and_model.invoke({"query": f"已知文章的关键词{keyword}，文章的风格{niche}， 以及全文的长度为{length}字。要求： 1.根据文章的关键词和风格，将全文划分分3-5个不同的部分，每个部分有一个确定的主题；2.将全文的长度划分到文章的每个部分中，给出该部分的字数；3.根据文章和关键词和每个部分的标题，将该部分的内容分为多个段落，然后给出每个段落中需要写的内容。"})
        outline_instance = parser.invoke(output)
        return outline_instance.outline
 
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

if __name__ == "__main__":
    # SA = StructureAgent(['引言', '低空经济的定义','低空经济的发展现状','发展低空经济的建议','总结'])
    SA = StructureAgent(None)
    outline = SA.run('低空经济', '行业研究报告', 3000)
    for section in outline:
        print("Title:", section.title)
        print("Length", section.length)
        for paragraph in section.paragraphs:
            print("Paragraph:", paragraph)