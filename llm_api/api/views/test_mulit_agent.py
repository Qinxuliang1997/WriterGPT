import asyncio

class MultiDocAgent:
    def __init__(self) -> None:
        # create the pipeline with transformations
        DEFAULT_SUMMARY_EXTRACT_TEMPLATE = """\
        Here is the content of the section:
        {context_str}

        Summarize the key topics and entities of the section in Chinese. \

        Summary: """

        extractors = [
            # TitleExtractor(nodes=5),
            # QuestionsAnsweredExtractor(questions=3),
            # EntityExtractor(prediction_threshold=0.5),
            SummaryExtractor(summaries=["prev", "self", "next"],prompt_template=DEFAULT_SUMMARY_EXTRACT_TEMPLATE),
            # KeywordExtractor(keywords=10, llm=llm),
            # CustomExtractor()
        ]
        self.pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=1024, chunk_overlap=20),
                # SummaryExtractor(summaries=["prev", "self", "next"],prompt_template=DEFAULT_SUMMARY_EXTRACT_TEMPLATE),
                OpenAIEmbedding(),
            ]
        )


    def load(self, url_list, text_list, files_dir):
        # index = VectorStoreIndex([])
        documents = []
        if url_list:
            doc = self.load_url(list(url_list))
            documents.extend(doc)
            # index.insert_nodes(node)
        if text_list:
            doc = self.load_text(list(text_list))
            documents.extend(doc)
            # self.index.insert_nodes(node)
        if os.listdir(files_dir):
            for file in os.listdir(files_dir):
                doc = self.load_file(os.path.join(files_dir, file))
                documents.extend(doc)
                # index.insert_nodes(node)
        return documents


    def index(self, documents, output_path):
        nodes = self.pipeline.run(documents=documents)
        logging.info('References are indexed!')
        index = VectorStoreIndex(nodes=nodes)
        self.save_all_index(index, output_path)
        return index
    
    async def build_doc_agent(self, url_list, text_list, files_dir):
        agents_dict = {}
        extra_info_dict = {}
        if url_list:
            for url in list(url_list):
                doc = self.load_url([url])
                nodes = self.ingestion(doc)
                file_base = url
                agent, summary = await self.build_agent_per_doc(nodes, file_base)
                agents_dict[file_base] = agent
                extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}
        if text_list:
            for text in text_list:
                doc = self.load_text([text])
                nodes = self.ingestion(doc)
                file_base = text[0:10]
                agent, summary = await self.build_agent_per_doc(nodes, file_base)
                agents_dict[file_base] = agent
                extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}
        if os.listdir(files_dir):
            for file in os.listdir(files_dir):
                doc = self.load_file(os.path.join(files_dir, file))
                nodes = self.ingestion(doc)
                text = ' '.join([node.text for node in nodes])
                if len(text) < 10:
                    print(f'读取文件{file}失败！')
                    continue
                file_base = file
                agent, summary = await self.build_agent_per_doc(nodes, file_base)
                agents_dict[file_base] = agent
                extra_info_dict[file_base] = {"summary": summary, "nodes": nodes}   
        return agents_dict, extra_info_dict

    async def build_agent_per_doc(self, nodes, file_base):
        vi_out_path = f"./data/llamaindex_docs/{file_base}"
        summary_out_path = f"./data/llamaindex_docs/{file_base}_summary.pkl"
        if not os.path.exists(vi_out_path):
            Path("./data/llamaindex_docs/").mkdir(parents=True, exist_ok=True)
            # build vector index
            vector_index = VectorStoreIndex(nodes)
            vector_index.storage_context.persist(persist_dir=vi_out_path)
        else:
            vector_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=vi_out_path),
            )

        # build summary index
        summary_index = SummaryIndex(nodes)

        # define query engines
        vector_query_engine = vector_index.as_query_engine(llm=OpenAI(temperature=0, model="gpt-3.5-turbo"))
        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize", llm=OpenAI(temperature=0, model="gpt-3.5-turbo")
        )

        # extract a summary
        if not os.path.exists(summary_out_path):
            Path(summary_out_path).parent.mkdir(parents=True, exist_ok=True)
            summary = str(
                await summary_query_engine.aquery(
                    "使用中文，给出这篇文章的框架"
                )
            )
            pickle.dump(summary, open(summary_out_path, "wb"))
        else:
            summary = pickle.load(open(summary_out_path, "rb"))

        # define tools
        query_engine_tools = [
            QueryEngineTool(
                query_engine=vector_query_engine,
                metadata=ToolMetadata(
                    name=f"vector_tool_{file_base[:2]}",
                    description=f"功能是获取关于特定主题的资料",
                ),
            ),
            QueryEngineTool(
                query_engine=summary_query_engine,
                metadata=ToolMetadata(
                    name=f"summary_tool_{file_base[:2]}",
                    description=f"功能是总结一篇文章",
                ),
            ),
        ]

        # build agent
        function_llm = OpenAI(model="gpt-4")
        agent = OpenAIAgent.from_tools(
            query_engine_tools,
            llm=function_llm,
            verbose=True,
            system_prompt=f"""\
    You are a specialized agent designed to answer queries about the `{file_base}` part of the LlamaIndex docs.
    You must ALWAYS use at least one of the tools provided when answering a question; do NOT rely on prior knowledge.\
    """,
        )

        return agent, summary

    async def agent_builder(self, url_list, text_list, files_dir):
        agents, extra_info = await self.build_doc_agent(url_list, text_list, files_dir)
        return agents, extra_info

    def build_tool(self, agents_dict):
        # define tool for each document agent
        all_tools = []
        for file_base, agent in agents_dict.items():
            summary = extra_info_dict[file_base]["summary"]
            doc_tool = QueryEngineTool(
                query_engine=agent,
                metadata=ToolMetadata(
                    name=f"tool_{file_base[:2]}",
                    description=summary,
                ),
            )
            all_tools.append(doc_tool)
        return all_tools

    def build_top_agent(self, all_tools):
        # define an "object" index and retriever over these tools
        obj_index = ObjectIndex.from_objects(
            all_tools,
            index_cls=VectorStoreIndex,
        )
        top_agent = OpenAIAgent.from_tools(
            tool_retriever=obj_index.as_retriever(similarity_top_k=3),
            system_prompt=""" \
You are an agent designed to answer queries.
Please always use the tools provided to answer a question. Do not rely on prior knowledge.\
""",
            verbose=True,
        )
        return obj_index.as_retriever(similarity_top_k=3), top_agent
    