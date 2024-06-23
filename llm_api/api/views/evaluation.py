import asyncio
import nest_asyncio
from llama_index.core.evaluation import (
    CorrectnessEvaluator, SemanticSimilarityEvaluator, RelevancyEvaluator,
    FaithfulnessEvaluator, BatchEvalRunner
)
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation.eval_utils import get_responses, get_results_df
import numpy as np
import pandas as pd
from IPython.display import display

class LlamaEvaluator:
    def __init__(self, model="gpt-4", max_samples=30):
        nest_asyncio.apply()

        self.llm = OpenAI(model=model)
        self.max_samples = max_samples

        # Initialize evaluators
        self.evaluators = {
            "correctness": CorrectnessEvaluator(llm=self.llm),
            "semantic_similarity": SemanticSimilarityEvaluator(),
            "relevancy": RelevancyEvaluator(llm=self.llm),
            "faithfulness": FaithfulnessEvaluator(llm=self.llm),
        }

    def generate_eval_samples(self, base_nodes, num_nodes_eval, first_num_sample, num_questions_per_chunk):
        asyncio.run(self._generate_eval_samples(base_nodes, num_nodes_eval, first_num_sample, num_questions_per_chunk))

    async def _generate_eval_samples(self, base_nodes, num_nodes_eval, first_num_sample, num_questions_per_chunk):
        from llama_index.core.evaluation import DatasetGenerator, QueryResponseDataset
        from llama_index.llms.openai import OpenAI
        import random
        # there are 428 nodes total. Take the first 200 to generate questions (the back half of the doc is all references)
        sample_eval_nodes = random.sample(base_nodes[:first_num_sample], num_nodes_eval)
        # NOTE: run this if the dataset isn't already saved
        # generate questions from the largest chunks (1024)
        dataset_generator = DatasetGenerator(
            sample_eval_nodes,
            llm=OpenAI(model="gpt-4"),
            show_progress=True,
            num_questions_per_chunk=num_questions_per_chunk,
        )
        eval_dataset = await dataset_generator.agenerate_dataset_from_nodes()
        eval_dataset.save_json("data/ipcc_eval_qr_dataset.json")
        # optional
        # eval_dataset = QueryResponseDataset.from_json("data/ipcc_eval_qr_dataset.json")

    def compare_results(self, eval_dataset, query_engines):
        asyncio.run(self._compare_results(eval_dataset, query_engines))

    async def _compare_results(self, eval_dataset, query_engines):
        eval_qs = eval_dataset.questions
        ref_response_strs = [r for (_, r) in eval_dataset.qr_pairs]
        results = {}

        # Evaluate all query engines
        for key, engine in query_engines.items():
            pred_responses = get_responses(eval_qs[:self.max_samples], engine, show_progress=True)
            pred_response_strs = [str(p) for p in pred_responses]
            batch_runner = BatchEvalRunner(self.evaluators, workers=1, show_progress=True)
            eval_results = await batch_runner.aevaluate_responses(
                queries=eval_qs[:self.max_samples],
                responses=pred_responses[:self.max_samples],
                reference=ref_response_strs[:self.max_samples],
            )
            results[key] = eval_results
            print(eval_qs[:self.max_samples] , pred_response_strs, eval_results)

        # Collect all results into a DataFrame
        results_df = get_results_df(
            list(results.values()),
            list(results.keys()),
            ["correctness", "relevancy", "faithfulness", "semantic_similarity"],
        )
        display(results_df)
