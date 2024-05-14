import asyncio
from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser 
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

class StructureAgent():
    def __init__(self, outline) -> None:
        self.outline = outline

    def run(self, keyword):
        if self.outline:
            self.write_article_structure_with_outline(keyword)
        else:
            self.write_article_structure_without_outline(keyword)

    def write_article_structure_without_outline(self, keyword: str, niche: str) -> Any:
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

