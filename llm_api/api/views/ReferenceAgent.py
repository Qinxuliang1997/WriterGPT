import os
from llama_index.core import (download_loader, 
                          SimpleDirectoryReader)
from llama_index.core import Document
from dotenv import load_dotenv
from pathlib import Path
from llama_index.llms.openai import OpenAI
# from llama_index.node_parser import SimpleNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.core import (VectorStoreIndex, 
                              Settings, 
                            )

load_dotenv(override=True)
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=300, api_key=os.getenv('OPENAI_API_KEY'))
class ReferenceAgent:
    def __init__(self) -> None:
        # create the pipeline with transformations
        self.pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=500, chunk_overlap=0),
                TitleExtractor(),
                OpenAIEmbedding(),
            ]
        )

    def indexing(self,url_list, text_list, files_dir):
        index = VectorStoreIndex([])
        if url_list:
            node = self.create_node_url(list(url_list))
            index.insert_nodes(node)
        if text_list:
            node = self.create_node_text(list(text_list))
            self.index.insert_nodes(node)
        if os.listdir(files_dir):
            node = self.create_node_dir(files_dir)
            index.insert_nodes(node)
        return index

    def create_node_text(self, text_list):
        documents = [Document(text=t) for t in text_list]
        # node = parser.get_nodes_from_documents(documents)
        node = self.pipeline.run(documents=documents)
        return node

    def create_node_url(self, url_list):
        SimpleWebPageReader = download_loader(loader_class="SimpleWebPageReader",
                                                refresh_cache=False)
        loader = SimpleWebPageReader()
        documents = loader.load_data(urls=url_list)
        # node = parser.get_nodes_from_documents(documents)
        node = self.pipeline.run(documents=documents)
        return node    

    def create_node_dir(self, dir_path):
        if len(os.listdir(dir_path)) != 0:
            print(os.listdir(dir_path))
            reader = SimpleDirectoryReader(
                input_dir=dir_path
            )
            documents = reader.load_data()
            # node = parser.get_nodes_from_documents(documents)
            node = self.pipeline.run(documents=documents)
            return node            
        else:
            raise ValueError("Unsupported input format")   
        
    def create_node_file(self, input_path):
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
            node = self.pipeline.run(documents=documents)
            return node

    def save_all_index(self, index, output_path):  
        index.storage_context.persist(persist_dir=output_path)

