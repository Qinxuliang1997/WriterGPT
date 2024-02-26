import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
import llama_index
from llama_index import (StorageContext, 
                         load_index_from_storage, 
                         ServiceContext, 
                         set_global_service_context,
                         get_response_synthesizer)
from llama_index.llms import OpenAI
from llama_index.retrievers import VectorIndexRetriever,SummaryIndexLLMRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.callbacks import CallbackManager, WandbCallbackHandler
from llama_index import set_global_handler,global_handler
from llama_index.prompts import PromptTemplate
from IPython.display import Markdown, display

llama_index.set_global_handler("simple")

# define LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=200, api_key=os.getenv("OPENAI_API_KEY"))

# configure service context
service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context)

# define prompt viewing function
def display_prompt_dict(prompts_dict):
    for k, p in prompts_dict.items():
        text_md = f"**Prompt Key**: {k}<br>" f"**Text:** <br>"
        display(Markdown(text_md))
        print(p.get_template())
        display(Markdown("<br><br>"))

index_file_path = os.path.join('../indexed_documents')
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir=index_file_path)
# load index
index = load_index_from_storage(storage_context)

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2,
)

nodes = retriever.retrieve("国有资产管理的问题有哪些？")

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.9)
    ]
)

new_summary_tmpl_str = (
    "The necessary materials and information are provided below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Utilizing the provided materials and your knowledge, "
    "compose a detailed report.\n"
    "Task: {query_str}\n"
    "Answer: "
)

new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": new_summary_tmpl}
)
prompts_dict = query_engine.get_prompts()
display_prompt_dict(prompts_dict)
