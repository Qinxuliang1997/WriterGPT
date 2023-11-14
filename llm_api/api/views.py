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
# from trulens_eval import TruLlama, Feedback, Tru, feedback
# tru = Tru()

# set_global_handler("wandb", run_args={"project": "llamaindex"})
# wandb_callback = global_handler

llama_index.set_global_handler("simple")

# define LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=200, api_key=os.getenv("OPENAI_API_KEY"))

# configure service context
service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context)

class AskView(View):
    
    def get(self, request, *args, **kwargs):
        query_str = request.GET.get('question', None)
        print("quesiont is %s" % (query_str))
        if not query_str:
            return JsonResponse({"error": "Please provide a question."}, status=400)

        index_file_path = os.path.join(settings.BASE_DIR, 'indexed_documents')
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=index_file_path)
        # load index
        index = load_index_from_storage(storage_context)

        # query_engine = index.as_query_engine()
        # configure retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=2,
        )
     
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
        response = query_engine.query(query_str)
        print(response)
        return JsonResponse({'answer': response.response})

    def post(self, request, *args, **kwargs):
        # Handle POST requests if needed
        pass