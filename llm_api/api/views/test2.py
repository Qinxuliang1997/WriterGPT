import os
import logging
from pathlib import Path
from llama_index.core import (download_loader, 
                          SimpleDirectoryReader)
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

from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager 

# Data Loader
DEFAULT_SUMMARY_EXTRACT_TEMPLATE = """\
Here is the content of the section:
{context_str}

Summarize the key topics and entities of the section in Chinese. \

Summary: """
pipeline = IngestionPipeline(
                transformations=[
                    SentenceSplitter(chunk_size=2048, chunk_overlap=0),
                    SummaryExtractor(summaries=["prev", "self", "next"],prompt_template=DEFAULT_SUMMARY_EXTRACT_TEMPLATE),
                    # OpenAIEmbedding(),
                ]
            )
SimpleWebPageReader = download_loader(loader_class="SimpleWebPageReader",
                                        refresh_cache=False)
loader = SimpleWebPageReader()
documents = loader.load_data(urls=['https://www.sohu.com/a/699520214_468661'])
print(documents)

# Chunking the docs.
pipeline = IngestionPipeline(
                transformations=[
                    SentenceSplitter(chunk_size=2048, chunk_overlap=0),
                    # SummaryExtractor(summaries=["prev", "self", "next"],prompt_template=DEFAULT_SUMMARY_EXTRACT_TEMPLATE),
                    # OpenAIEmbedding(),
                ]
            )
node = pipeline.run(documents=documents)
print(node[0].get_content(metadata_mode="all"))  

