from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from typing import List
from dotenv import load_dotenv
import os

class Paragraph(BaseModel):
    paragraph: str

class Section(BaseModel):
    title: str = Field(..., description="本小节的标题")
    length: str = Field(..., description="本小节的长度")
    paragraphs: List[str] = Field(..., description="当前小节中，每个段落的主旨")

class Outline(BaseModel):
    outline: List[Section]

class StructureAgent:
    def __init__(self) -> None:
        pass

    def run_with_reference(self, title, content_requirement, niche, length, index, doc_info):
        docs_summary = []
        for file_base, info in doc_info.items():
            docs_summary.append(file_base + info['summary'].replace('\n', ' '))
        docs_summary_str = ' '.join(docs_summary)
        parser = PydanticOutputParser(pydantic_object=Outline)
        prompt = PromptTemplate(
            template="假如你是一个优秀的中文作家，请你使用中文为下面的文章拟定一个全面的、丰富的提纲，不同部分之间内容不重复.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        load_dotenv(override=True)
        model = ChatOpenAI(model_name="gpt-4o", temperature=0.0, api_key=os.getenv('OPENAI_API_KEY'), max_tokens=1500)
        prompt_and_model = prompt | model
        output = prompt_and_model.invoke({"query": f"已知文章的标题{title}，文章的类型{niche}， 文章的要求{content_requirement}， 以及全文的长度为{length}字，参考文献的内容{docs_summary_str}。要求： 1.根据文章的类型、要求以及参考文献提供的资料，将全文划分到不同的部分，每个部分有一个确定的主题；2.将全文的长度划分到文章的每个部分中，给出该部分的字数；3.根据文章和关键词和每个部分的标题，将该部分的内容分为多个段落，然后给出每个段落中需要写的内容。"})
        outline_instance = parser.invoke(output)
        return self.convert_sections_to_dict(outline_instance.outline)

    def run_without_reference(self, title: str, content_requirement: str, niche: str, length: str):
        parser = PydanticOutputParser(pydantic_object=Outline)
        prompt = PromptTemplate(
            template="假如你是一个优秀的中文作家，请你使用中文为下面的文章拟定一个全面的、丰富的提纲，不同部分之间内容不可以重复.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        load_dotenv(override=True)
        model = ChatOpenAI(model_name="gpt-4o", temperature=0.0, api_key=os.getenv('OPENAI_API_KEY'), max_tokens=1500)
        prompt_and_model = prompt | model
        query = "要求:" \
                "1.根据文章的关键词和风格，将全文划分到不同的部分，每个部分有一个确定的主题；"\
                "2.将全文的长度划分到文章的每个部分中，给出该部分的字数；"\
                "3.考虑全文的统一性，将每个部分的内容分为多个段落，给出每个段落中需要写的内容。"\
                f"文章的标题: {title}"\
                f"文章的类型: {niche}"\
                f"文章关键词: {content_requirement}"\
                f"文章长度: {length}"
        output = prompt_and_model.invoke({"query": query})
        print(output)
        outline_instance = parser.invoke(output)
        return self.convert_sections_to_dict(outline_instance.outline)

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
    SA = StructureAgent()
    outline = SA.run_without_reference(title='全球及中国低空经济产业发展情况',
                                        content_requirement='介绍低空经济的定义、全球低空经济产业发展情况、中国低空经济产业发展情况', 
                                        niche='行业研究报告', 
                                        length=3000)
    print(outline)
    outline_dic = SA.convert_sections_to_dict(outline)
    print(outline_dic)
    for section in outline:
        print("Title:", section.title)
        print("Length", section.length)
        for paragraph in section.paragraphs:
            print("Paragraph:", paragraph)