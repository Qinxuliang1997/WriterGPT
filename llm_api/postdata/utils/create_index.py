import os
from llama_index import (VectorStoreIndex,
                          download_loader, 
                          SimpleDirectoryReader, 
                          ServiceContext, 
                          set_global_service_context,
                          set_global_handler,
                          global_handler)
from pathlib import Path
from llama_index.llms import OpenAI
from llama_index.node_parser import SimpleNodeParser
from llama_index.callbacks import CallbackManager, WandbCallbackHandler

# define LLM
# llm = OpenAI(model="gpt-3.5", temperature=0, max_tokens=256, api_key=os.getenv("OPENAI_API_KEY"))

# initialise WandbCallbackHandler and pass any wandb.init args
# set_global_handler("wandb", run_args={"project": "llamaindex"})
# wandb_callback = global_handler

# configure service context
# service_context = ServiceContext.from_defaults(llm=llm)
# set_global_service_context(service_context)

parser = SimpleNodeParser.from_defaults()
index = VectorStoreIndex([])

def index_documents(input_path):

    if isinstance(input_path, str):
        # Load data based on input type
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
        elif input_path.startswith('http'):
            SimpleWebPageReader = download_loader(loader_class="SimpleWebPageReader",
                                                  refresh_cache=False)
            loader = SimpleWebPageReader()
            documents = loader.load_data(urls=[input_path])
        elif input_path.endswith("/"):
             if len(os.listdir(input_path)) != 0:
                print(os.listdir(input_path))
                reader = SimpleDirectoryReader(
                    input_dir=input_path, recursive=True
                )
                documents = reader.load_data()
        else:
            raise ValueError("Unsupported input format")
        print("finished" , input_path)
        nodes = parser.get_nodes_from_documents(documents)
        index.insert_nodes(nodes)


def save_all_index(output_path):  
    index.storage_context.persist(persist_dir=output_path)