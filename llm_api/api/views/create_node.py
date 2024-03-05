import os
from llama_index import (download_loader, 
                          SimpleDirectoryReader)
from llama_index import Document
from pathlib import Path
from llama_index.node_parser import SimpleNodeParser

parser = SimpleNodeParser.from_defaults()

def create_node_text(text_list):
    documents = [Document(text=t) for t in text_list]
    node = parser.get_nodes_from_documents(documents)
    return node

def create_node_url(url_list):
    SimpleWebPageReader = download_loader(loader_class="SimpleWebPageReader",
                                            refresh_cache=False)
    loader = SimpleWebPageReader()
    documents = loader.load_data(urls=url_list)
    node = parser.get_nodes_from_documents(documents)
    return node    

def create_node_dir(dir_path):
    if len(os.listdir(dir_path)) != 0:
        print(os.listdir(dir_path))
        reader = SimpleDirectoryReader(
            input_dir=dir_path, recursive=True
        )
        documents = reader.load_data()
        node = parser.get_nodes_from_documents(documents)
        return node            
    else:
        raise ValueError("Unsupported input format")   
    
def create_node_file(input_path):
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
        node = parser.get_nodes_from_documents(documents)
        return node

# def save_all_index(output_path):  
#     index.storage_context.persist(persist_dir=output_path)