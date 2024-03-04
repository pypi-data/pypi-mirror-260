from typing import List, TypedDict, Optional
from athina.helpers.athina_logging_helper import AthinaLoggingHelper
from athina.evals.llm.llm_evaluator import LlmEvaluator
from athina.interfaces.result import EvalResult, BatchRunResult
from athina.interfaces.data import DataPoint
from athina.interfaces.athina import AthinaExperiment
from athina.services.athina_api_service import AthinaApiService
import pandas as pd
import json
import hashlib


class DataPointWithEvalResults(TypedDict):
    """A data point with its evaluation results."""

    data_point: DataPoint
    eval_results: List[EvalResult]


class LlmEvaluatorDescription(TypedDict):
    """A description of an LLM evaluator."""

    name: str
    display_name: str


class LlmBatchEvalResult(TypedDict):
    """Result of running a batch of LLM evaluations."""

    results: List[EvalResult]
    total_runtime: float
    passed_evals: int
    failed_evals: int
    total_evals: int
    total_datapoints: int


class EvalRunner:
    @staticmethod
    def eval_results_link(eval_request_id: str):
        return f"https://app.athina.ai/develop/request/{eval_request_id}"

    @staticmethod
    def flatten_eval_results(batch_eval_results):
        # Flatten the list of lists into a single list of evaluation results
        flattened_results = [item for sublist in batch_eval_results for item in sublist]
        return flattened_results

    @staticmethod
    def to_df(batch_eval_results):
        # Initialize a dictionary to hold the aggregated data
        aggregated_data = {}
        flattened_results = EvalRunner.flatten_eval_results(
            batch_eval_results=batch_eval_results
        )

        # Process each evaluation result
        for eval_result in flattened_results:
            # Serialize and hash the datapoint dictionary to create a unique identifier
            datapoint_hash = hashlib.md5(
                json.dumps(eval_result["data"], sort_keys=True).encode()
            ).hexdigest()

            # Initialize the datapoint in the aggregated data if not already present
            if datapoint_hash not in aggregated_data:
                aggregated_data[datapoint_hash] = eval_result[
                    "data"
                ]  # Include datapoint details

            # Update the aggregated data with metrics from this evaluation
            for metric in eval_result["metrics"]:
                metric_name = metric["id"]
                metric_value = metric["value"]
                aggregated_data[datapoint_hash][eval_result["display_name"] + " " + metric_name] = metric_value

        # Convert the aggregated data into a DataFrame
        df = pd.DataFrame(list(aggregated_data.values()))

        return df

    @staticmethod
    def batch_eval_result(
        eval_results: List[EvalResult],
    ) -> LlmBatchEvalResult:
        """
        Calculate metrics for a batch of LLM evaluations.

        Args:
            datapoints_with_eval_results: A list of DataPointWithEvalResults objects.

        Returns:
            A LlmBatchEvalResult object.
        """
        total_runtime = 0
        passed_evals = 0
        failed_evals = 0
        total_evals = 0

        # Iterate through each DataPointWithEvalResults
        for eval_result in eval_results:
            total_evals += 1
            total_runtime += eval_result.get("runtime", 0)

            # Counting passed and failed evaluations
            if eval_result.get("failure"):
                failed_evals += 1
            else:
                passed_evals += 1

        total_datapoints = len(eval_result)

        return LlmBatchEvalResult(
            results=eval_result,
            total_runtime=total_runtime,
            passed_evals=passed_evals,
            failed_evals=failed_evals,
            total_evals=total_evals,
            total_datapoints=total_datapoints,
        )

    @staticmethod
    def run_suite(
        evals: List[LlmEvaluator],
        data: List[DataPoint],
        experiment: Optional[AthinaExperiment] = None,
        max_parallel_evals: int = 1,
    ) -> List[LlmBatchEvalResult]:
        """
        Run a suite of LLM evaluations against a dataset.

        Args:
            evals: A list of LlmEvaluator objects.
            data: A list of data points.

        Returns:
            A list of LlmBatchEvalResult objects.
        """
        # Create eval request
        eval_suite_name = "llm_eval_suite" + "_" + ",".join(eval.name for eval in evals)
        eval_request_id = AthinaLoggingHelper.create_eval_request(
            eval_name=eval_suite_name,
            request_data={"data": data},
            request_type="suite",
        )

        # Log experiment
        if experiment is not None:
            AthinaLoggingHelper.log_experiment(
                eval_request_id=eval_request_id,
                experiment=experiment,
            )

        AthinaApiService.log_usage(eval_name=eval_suite_name, run_type="suite")

        batch_results = []
        for eval in evals:
            # Validate the dataset against the required args
            eval._validate_batch_args(data)

            # Run the evaluations
            if max_parallel_evals > 1:
                eval_results = eval._run_batch_generator_async(data, max_parallel_evals)
            else:
                eval_results = list(eval._run_batch_generator(data))

            # Log evaluation results to Athina
            AthinaLoggingHelper.log_eval_results(
                eval_request_id=eval_request_id,
                eval_results=eval_results,
            )

            batch_results.append(eval_results)

        print(
            f"You can view the evaluation results at {EvalRunner.eval_results_link(eval_request_id)}"
        )
        return EvalRunner.to_df(batch_results)
