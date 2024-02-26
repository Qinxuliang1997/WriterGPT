import os
import json
from django.conf import settings
from django.http import JsonResponse
# from django.views import View
from rest_framework.views import APIView
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
llm = OpenAI(model="gpt-3.5-turbo-1106", temperature=0, max_tokens=4000, api_key=os.getenv("OPENAI_API_KEY"))

# configure service context
service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context)

class AskView(APIView):

    def generate_prompt(self, prompt_details):
        print('prompt_details')
        print(prompt_details)
        prompt = f"请根据以下描述，使用中文，撰写一篇关于{prompt_details['topic']}的文章，文章应包含以下几个部分： "
        for idx, point in enumerate(prompt_details['outline'], start=1):
            prompt += f"{idx}. {point}；"
        prompt += f"请确保文章内容围绕{prompt_details['primaryKeyword']}这一主题，同时同时涉及{prompt_details['secondaryKeywords']}这些关键词。"
        prompt += f"文章应该采用{prompt_details['view']}、{prompt_details['tone']}的语气，并在文章中嵌入相关的事实材料以支持论述。最后，请使用Markdown格式进行排版，确保文章结构清晰。"
        return prompt
        
    # def parese_description(self, description):
    #     topic = description.get('topic', '')
    #     primaryKeyword = description.get('primaryKeyword', '')
    #     secondaryKeywords = description.get('secondaryKeywords', '')
    #     tone = description.get('tone', '')
    #     view = description.get('view', '')
    #     title = description.get('title', '')
    #     outline = description.get('outline', [])
    #     description['outline'] = ' '.join(outline)
    #     del description['nextClick']
    #     prompt = '\n'.join([i +':'+ j for i,j in description.items()])
    #     prompt_string = """根据下面提供的描述，使用中文写一篇2000字的文章，要求：
    #                        1.根据提供的目录，逐段生成文章；
    #                        2.文章的内容中必须围绕关键词进行书写，符合语气、人称的要求；
    #                        3.在参考文献中摘录与本文书写内容相关的事实材料，然后放到文章的相应部分；
    #                        4.使用markdown格式返回，此外不要有其他任何描述性话语 :\n"""
    #     prompt = prompt_string + prompt
    #     print('prompt:\n' + prompt)
    #     return prompt
    
    def write(self, description):
        # prompt = self.parese_description(description)
        prompt = self.generate_prompt(description)
        index_file_path = os.path.join(settings.BASE_DIR, 'indexed_documents')
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=index_file_path)
        # load index
        index = load_index_from_storage(storage_context)
        query_engine = index.as_chat_engine()
        # # configure retriever
        # retriever = VectorIndexRetriever(
        #     index=index,
        #     similarity_top_k=2,
        # ) 
        # # configure response synthesizer
        # response_synthesizer = get_response_synthesizer()
        # # assemble query engine
        # query_engine = RetrieverQueryEngine(
        #     retriever=retriever,
        #     response_synthesizer=response_synthesizer,
        #     node_postprocessors=[
        #         SimilarityPostprocessor(similarity_cutoff=0.9)
        #     ]
        # )
        response = query_engine.chat(prompt)
        print(response)  
        return response.response
    # def get(self, request, *args, **kwargs):
    #     query_str = request.GET.get('question', None)
    #     print("quesiont is %s" % (query_str))
    #     if not query_str:
    #         return JsonResponse({"error": "Please provide a question."}, status=400)
    #     return JsonResponse({'answer': response.response})
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            content = self.write(data)
            return JsonResponse({
                'status': 'success',
                'message': 'Article data received successfully.',
                'answer': 'good!',
                'Access-Control-Allow-Origin': 'http://localhost:3000',
                'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
                'content': content,
            }, status=200)
        except json.JSONDecodeError:
            # 如果请求体不是有效的 JSON，返回错误
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON.'
            }, status=400)
        except Exception as e:
            # 处理其他可能的异常
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)