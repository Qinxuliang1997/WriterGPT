import os
import logging
import asyncio
from llama_index.llms.openai import OpenAI
import pickle
from pathlib import Path
from tqdm.notebook import tqdm
from llama_index.core import (download_loader, 
                          SimpleDirectoryReader,
                          SummaryIndex)
from llama_index.core import Document
# from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import (TitleExtractor,
                                         SummaryExtractor)
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core import (VectorStoreIndex, 
                              StorageContext,
                              load_index_from_storage,
                              )
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.objects import ObjectIndex

from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager 
from llama_index.agent.openai import OpenAIAgent


# llama_debug
# from llama_index.core.callbacks import LlamaDebugHandler
# llama_debug = LlamaDebugHandler(print_trace_on_end=True)
# Settings.callback_manager = CallbackManager([llama_debug])

# wandb
# from llama_index.core.callbacks import CallbackManager
# from llama_index.callbacks.wandb import WandbCallbackHandler
# run_args = dict(
#     project="llamaindex",
# )
# wandb_callback = WandbCallbackHandler(run_args=run_args)
# Settings.callback_manager = CallbackManager([wandb_callback])

# Langfuse
# from langfuse.llama_index import LlamaIndexCallbackHandler
# langfuse_callback_handler = LlamaIndexCallbackHandler(
#     public_key="pk-lf-ab4327b0-4fc3-4b84-bc71-86231d3d94d8",
#     secret_key="sk-lf-ee521c72-0517-45db-8fce-e9b86577a360",
#     host="https://cloud.langfuse.com"
# )
# Settings.callback_manager = CallbackManager([langfuse_callback_handler])

class ReferenceAgent:
    def __init__(self, base_dir) -> None:
        self.base_dir = base_dir

    async def index(self, url_list, text_list, files_dir):
        extra_info_dict = {}
        all_nodes = []
        node_parser = SentenceSplitter()
        if url_list:
            for url in list(url_list):
                doc = self.load_url([url])
                nodes = node_parser.get_nodes_from_documents(doc)
                file_base = url
                summary = await self.get_summary_per_doc(nodes, file_base)
                extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}
                all_nodes.extend(nodes)
        if text_list:
            for text in text_list:
                doc = self.load_text([text])
                nodes = node_parser.get_nodes_from_documents(doc)
                file_base = text[0:10]
                summary = await self.get_summary_per_doc(nodes, file_base)
                extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}
                all_nodes.extend(nodes)
        if os.listdir(files_dir):
            for file in os.listdir(files_dir):
                doc = self.load_file(os.path.join(files_dir, file))
                nodes = node_parser.get_nodes_from_documents(doc)
                text = ' '.join([node.text for node in nodes])
                if len(text) < 10:
                    print(f'读取文件{file}失败！')
                    continue
                file_base = file
                summary = await self.get_summary_per_doc(nodes, file_base)
                extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}   
                all_nodes.extend(nodes)
        all_doc_index = await self.get_index_all_doc(all_nodes)
        return all_doc_index, extra_info_dict  
    
    async def get_index_all_doc(self, all_nodes):
        vector_out_path = os.path.join(self.base_dir, 'base_index')
        # vector_out_path = f"./data/llamaindex_docs/base_index"
        if not os.path.exists(vector_out_path):
            Path(self.base_dir).mkdir(parents=True, exist_ok=True)
            # build vector index
            vector_index = VectorStoreIndex(all_nodes)
            vector_index.storage_context.persist(persist_dir=vector_out_path)
        else:
            vector_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=vector_out_path),
            )
        return vector_index
    
    async def get_summary_per_doc(self, nodes, file_base):
        summary_out_path = f"{self.base_dir}/{file_base}_summary.pkl"
        if not os.path.exists(summary_out_path):
            summary_index = SummaryIndex(nodes)
            summary_query_engine = summary_index.as_query_engine(
                response_mode="tree_summarize",
            )
            Path(summary_out_path).parent.mkdir(parents=True, exist_ok=True)
            summary = str(
                summary_query_engine.query(
                    "使用中文，请你给出这本书每个部分的关键词，以及该部分所探讨的所有问题"
                )
            )
            pickle.dump(summary, open(summary_out_path, "wb"))
        else:
            summary = pickle.load(open(summary_out_path, "rb"))
        return summary

    def load_text(self, text_list):
        documents = [Document(text=t) for t in text_list]
        # node = parser.get_nodes_from_documents(documents)
        # node = self.pipeline.run(documents=documents)
        return documents

    def load_url(self, url_list):
        SimpleWebPageReader = download_loader(loader_class="SimpleWebPageReader",
                                                refresh_cache=False)
        loader = SimpleWebPageReader()
        documents = loader.load_data(urls=url_list)
        # node = parser.get_nodes_from_documents(documents)
        # node = self.pipeline.run(documents=documents)
        return documents    

    def load_dir(self, dir_path):
        if len(os.listdir(dir_path)) != 0:
            reader = SimpleDirectoryReader(
                input_dir=dir_path
            )
            documents = reader.load_data()
            # node = parser.get_nodes_from_documents(documents)
            # node = self.pipeline.run(documents=documents)
            return documents            
        else:
            raise ValueError("Unsupported input format")   
        
    def load_file(self, input_path):
        if isinstance(input_path, str):
            print("indexing:",input_path)
            if input_path.endswith('.pdf'):
                PDFReader = download_loader(loader_class="PDFReader", 
                                            refresh_cache=False)           
                loader = PDFReader()
                documents = loader.load_data(file=Path(input_path))            
            elif input_path.endswith('.docx'):
                DocxReader = download_loader(loader_class="DocxReader", 
                                            refresh_cache=False)           
                loader = DocxReader()
                documents = loader.load_data(file=Path(input_path))
            elif input_path.endswith('.txt'):
                TextReader = download_loader(loader_class="TextReader", 
                                            refresh_cache=False)           
                loader = TextReader()
                documents = loader.load_data(file=Path(input_path))
            else:
                raise ValueError("Unsupported input format")
            print("finished" , input_path)
            # node = parser.get_nodes_from_documents(documents)
            # node = self.pipeline.run(documents=documents)
            return documents

if __name__ == "__main__":
    RA = ReferenceAgent('./data/llamaindex_docs')
    url_list = set(['https://www.sohu.com/a/699520214_468661'])
    # url_list = set()
    text_list = set()
    files_dir = os.path.join("../../media", "user_1", 'original_files')    
    output_path =  os.path.join("../../media", "user_1", 'indexed_files') 
    all_doc_index, extra_info_dict = asyncio.run(RA.index(url_list, text_list, files_dir))
    for file_base, info in extra_info_dict.items():
        print(info['summary'])