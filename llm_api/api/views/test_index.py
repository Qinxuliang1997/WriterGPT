import os
from llama_index.llms.openai import OpenAI
from llama_index.core import download_loader, SummaryIndex, Settings

Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo")

# Data Loader
def data_loader():
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=os.path.join("../../media", "test_1", 'original_files', '4fb2e8b3-7416-4dd7-a2c8-9076208de77c.pdf' ))
    print(documents, len(documents))
    return documents

# Chunking and Embedding of the chunks.
def chunk(documents):
    from llama_index.core.node_parser import SentenceSplitter
    splitter = SentenceSplitter(
        chunk_size=1024,
        chunk_overlap=20,
    )
    nodes = splitter.get_nodes_from_documents(documents)
    # index = VectorStoreIndex.from_documents(documents)
    return nodes

def summary_query_engine(nodes):
    summary_index = SummaryIndex(nodes)
    summary_query_engine = summary_index.as_query_engine(response_mode="tree_summarize", llm=Settings.llm)
    return summary_query_engine

if __name__ == "__main__":
    documents = data_loader()
    nodes = chunk(documents)
    query_engine = summary_query_engine(nodes)
    summary = str(query_engine.query("请你用一段话介绍这篇文章的全部内容"))
    print(summary)