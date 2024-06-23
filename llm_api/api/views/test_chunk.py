from evaluation import LlamaEvaluator
from llama_index.core import VectorStoreIndex
from llama_index.core import download_loader
from llama_index.core.retrievers import VectorIndexRetriever,AutoMergingRetriever
from llama_index.core import ServiceContext
from llama_index.core.callbacks import CallbackManager
from llama_index.callbacks.wandb import WandbCallbackHandler
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.evaluation import QueryResponseDataset
import os
import time
import asyncio
# # initialise WandbCallbackHandler and pass any wandb.init args
# wandb_args = {"project":"llama-index-report"}
# wandb_callback = WandbCallbackHandler(run_args=wandb_args)
# # pass wandb_callback to the service context
# callback_manager = CallbackManager([wandb_callback])

# Data Loader
def data_loader():
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=os.path.join("../../media", "test_1", 'original_files', 'c049b19a-34c3-482f-bec4-09338e5f1e46.pdf' ))
    return documents

# Chunking and Embedding of the chunks.
def chunk_v0(documents):
    from llama_index.core.node_parser import SentenceSplitter
    splitter = SentenceSplitter(
        chunk_size=1024,
        chunk_overlap=20,
    )
    nodes = splitter.get_nodes_from_documents(documents)
    # index = VectorStoreIndex.from_documents(documents)
    return nodes

def chunk_v1(documents):
    from llama_index.core.node_parser import SemanticSplitterNodeParser
    from llama_index.embeddings.openai import OpenAIEmbedding
    embed_model = OpenAIEmbedding()
    splitter = SemanticSplitterNodeParser(
        buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
    )
    nodes = splitter.get_nodes_from_documents(documents)
    return nodes

def chunk_v2(documents):
    import nltk
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.core.node_parser import SentenceWindowNodeParser
    splitter = SentenceSplitter(
        chunk_size=1024,
        chunk_overlap=20,
    )
    node_parser = SentenceWindowNodeParser.from_defaults(
        # how many sentences on either side to capture
        window_size=3,
        # the metadata key that holds the window of surrounding sentences
        window_metadata_key="window",
        # the metadata key that holds the original sentence
        original_text_metadata_key="original_sentence",
    )
    nodes = node_parser.get_nodes_from_documents(documents)
    return nodes

def chunk_v3(documents):
    from llama_index.core.node_parser import HierarchicalNodeParser
    node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 1014, 512]
    )
    nodes = node_parser.get_nodes_from_documents(documents)
    return nodes

def retrieval(nodes):
    index = VectorStoreIndex(nodes)
    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3,
    )
    nodes = retriever.retrieve("低空经济的定义")
    return nodes

def automereging_retriever(nodes):
    # construct base retriver
    from llama_index.core.storage.docstore import SimpleDocumentStore
    from llama_index.core import StorageContext
    docstore = SimpleDocumentStore()
    # insert nodes into docstore
    docstore.add_documents(nodes)
    # define storage context (will include vector store by default too)
    storage_context = StorageContext.from_defaults(docstore=docstore)    
    from llama_index.core.node_parser import get_leaf_nodes, get_root_nodes
    leaf_nodes = get_leaf_nodes(nodes)
    base_index = VectorStoreIndex(
        leaf_nodes,
        storage_context=storage_context,
        )
    base_retriever = base_index.as_retriever(similarity_top_k=3)
    retriever = AutoMergingRetriever(base_retriever, storage_context, verbose=True)
    nodes = retriever.retrieve("深圳低空经济的发展情况")
    return nodes

# Retrieval, node poseprocessing, response synthesis.
def query_engine_v0(nodes):
    index = VectorStoreIndex(nodes)
    query_engine = index.as_query_engine()
    return query_engine

def query_engine_v1(nodes):
    index = VectorStoreIndex(nodes)
    query_engine = index.as_query_engine()
    return query_engine

def query_engine_v2(nodes):
    index = VectorStoreIndex(nodes)
    query_engine = index.as_query_engine(
        similarity_top_k=2,
        # the target key defaults to `window` to match the node_parser's default
        node_postprocessors=[
            MetadataReplacementPostProcessor(target_metadata_key="window")
        ],
    )
    return query_engine

def query_engine_v3(nodes):
    from llama_index.core.query_engine import RetrieverQueryEngine
    retriever = automereging_retriever(nodes)
    query_engine = RetrieverQueryEngine.from_args(retriever)
    return query_engine

def visualization(nodes):
    print(len(nodes))
    print(nodes[0].get_content())
    # print(retrieval(nodes))
    # from llama_index.core.response.notebook_utils import display_source_node
    # for node in nodes:
    #     display_source_node(node, source_length=10000)

if __name__ == "__main__":
    documents = data_loader()

    start_time = time.time()
    nodes_v0 = chunk_v0(documents)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"chunk执行时间(v0): {execution_time:.2f} 秒")
    text = ' '.join([node.text for node in nodes_v0])
    print(text)
    # start_time = time.time()
    # nodes_v1 = chunk_v1(documents)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"chunk执行时间(v1): {execution_time:.2f} 秒")

    # start_time = time.time()
    # nodes_v2 = chunk_v2(documents)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"chunk执行时间(v2): {execution_time:.2f} 秒")

    # start_time = time.time()
    # nodes_v3 = chunk_v0(documents)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"chunk执行时间(v3): {execution_time:.2f} 秒")
    # print(automereging_retriever(nodes_v3))

    # query_engine_list = {'Sentence spliter': query_engine_v0(nodes_v0),
                        #  'Semantic splitter': query_engine_v1(nodes_v1),
                        #  'Sentence Window and metadata replacement': query_engine_v2(nodes_v2),
                        #  'Hierarchical': query_engine_v3(nodes_v3)
                        #  }

    # base_nodes = chunk_v0(documents)
    # evaluator = LlamaEvaluator(model="gpt-4", max_samples=1)

    # evaluator.generate_eval_samples(nodes_v0, num_nodes_eval=5, first_num_sample=15, num_questions_per_chunk=2)
    # eval_dataset = QueryResponseDataset.from_json("data/ipcc_eval_qr_dataset.json")
    # evaluator.compare_results(eval_dataset=eval_dataset, query_engines=query_engine_list)

   

