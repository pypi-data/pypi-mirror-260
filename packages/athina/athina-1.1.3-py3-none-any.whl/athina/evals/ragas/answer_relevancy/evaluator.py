from typing import List

from athina.interfaces.model import Model
from ..ragas_evaluator import RagasEvaluator
from athina.evals.eval_type import RagasEvalTypeId
from athina.metrics.metric_type import MetricType
from ragas.metrics import answer_relevancy

"""
RAGAS Answer Relevancy Docs: https://docs.ragas.io/en/latest/concepts/metrics/answer_relevance.html
RAGAS Answer Relevancy Github: https://github.com/explodinggradients/ragas/blob/main/src/ragas/metrics/_answer_relevance.py
"""
class RagasAnswerRelevancy(RagasEvaluator):
    """
    This evaluator focuses on assessing how pertinent the generated response is to the given prompt. 
    A lower score is assigned to responses that are incomplete or contain redundant information.
    """
    @property
    def name(self):
        return RagasEvalTypeId.RAGAS_ANSWER_RELEVANCY.value

    @property
    def display_name(self):
        return "Ragas Answer Relevancy"

    @property
    def metric_ids(self) -> List[str]:
        return [MetricType.RAGAS_ANSWER_RELEVANCY.value]
    
    @property
    def ragas_metric(self):
        return answer_relevancy
    
    @property
    def ragas_metric_name(self):
        return "answer_relevancy"

    @property
    def default_model(self):
        return Model.GPT35_TURBO.value

    @property
    def required_args(self):
        return ["query", "contexts", "response"]

    @property
    def examples(self):
        return None
    
    @property
    def grade_reason(self) -> str:
        return "A response is deemed relevant when it directly and appropriately addresses the original query. Importantly, our assessment of answer relevance does not consider factuality but instead penalizes cases where the response lacks completeness or contains redundant details"
    
    def generate_data_to_evaluate(self, query, contexts, response, **kwargs) -> dict:
        """
        Generates data for evaluation.

        :param contexts: list of strings of retrieved context
        :param query: user query
        :param response: llm response
        :return: A dictionary with formatted data for evaluation
        """
        data = {
            "contexts": [contexts],
            "question": [query],
            "answer": [response]
        }
        return data
