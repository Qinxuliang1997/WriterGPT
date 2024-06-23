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

# import llama_index.core
# llama_index.core.set_global_handler("simple")
# import logging
# import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# initialise WandbCallbackHandler and pass any wandb.init args
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.core.callbacks import LlamaDebugHandler
from llama_index.callbacks.wandb import WandbCallbackHandler
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
run_args = dict(
    project="llamaindex",
)
wandb_callback = WandbCallbackHandler(run_args=run_args)
Settings.callback_manager = CallbackManager([wandb_callback])

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
reader = SimpleDirectoryReader(
                input_dir=os.path.join("../../media", "user_1", "original_files")
        )
documents = reader.load_data()
# Chunking and Embedding of the chunks.
index = VectorStoreIndex([])
node = pipeline.run(documents=documents)
index.insert_nodes(node)
# Retrieval, node poseprocessing, response synthesis.
query_engine = index.as_query_engine()

# Run the query engine on a user question.
response = query_engine.query("Who wrote this paper?")

print(response)