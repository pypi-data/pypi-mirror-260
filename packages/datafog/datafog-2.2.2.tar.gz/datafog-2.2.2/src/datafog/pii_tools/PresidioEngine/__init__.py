import json
from typing import Any, Dict, Iterable, List, Union

from presidio_analyzer import AnalyzerEngine, BatchAnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine, BatchAnonymizerEngine


def presidio_batch_init():
    analyzer = AnalyzerEngine()
    batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)
    batch_anonymizer = BatchAnonymizerEngine(anonymizer_engine=AnonymizerEngine())
    return analyzer, batch_analyzer, batch_anonymizer


def batch_scan(text: Dict[str, str], batch_analyzer: BatchAnalyzerEngine) -> List[str]:
    analyzer_results = batch_analyzer.analyze_dict(text, language="en")
    return [
        json.dumps(
            {
                "key": result.key,
                "value": result.value,
                "recognizer_results": serialize_recognizer_results(
                    result.recognizer_results
                ),
            }
        )
        for result in analyzer_results
    ]


from typing import Dict, Iterator, List, Optional, Union

from presidio_analyzer import RecognizerResult


def serialize_recognizer_results(
    recognizer_results: Union[
        List[RecognizerResult], List[List[RecognizerResult]], Iterator[RecognizerResult]
    ]
) -> Optional[
    Union[
        List[Dict[str, Union[str, int, float, None]]],
        List[List[Dict[str, Union[str, int, float, None]]]],
    ]
]:
    if isinstance(recognizer_results, list):
        if recognizer_results and isinstance(recognizer_results[0], RecognizerResult):
            return [
                {
                    "entity_type": r.entity_type,
                    "start": r.start,
                    "end": r.end,
                    "score": r.score,
                    "analysis_explanation": r.analysis_explanation,
                }
                for r in recognizer_results
            ]
        elif recognizer_results and isinstance(recognizer_results[0], list):
            return [serialize_recognizer_results(rr) for rr in recognizer_results]
    elif isinstance(recognizer_results, Iterator):
        return [serialize_recognizer_results(rr) for rr in recognizer_results]
    else:
        return None


from typing import Any, Dict, Iterable, List, Union

from presidio_anonymizer import AnonymizerEngine, BatchAnonymizerEngine
from presidio_anonymizer.entities import DictRecognizerResult, RecognizerResult


def batch_redact(
    input_data: Union[Dict[str, str], List[str]],
    results: List[str],
    anonymizer: BatchAnonymizerEngine,
    **kwargs
) -> Union[List[str], Dict[str, str]]:
    if isinstance(input_data, dict):
        # Input is a dictionary, perform anonymize_dict
        analyzer_results = [
            DictRecognizerResult(
                key=result_dict["key"],
                value=result_dict["value"],
                recognizer_results=[
                    RecognizerResult(
                        entity_type=r["entity_type"],
                        start=r["start"],
                        end=r["end"],
                        score=r["score"],
                    )
                    for recognizer_result in result_dict["recognizer_results"]
                    if recognizer_result
                    for r in recognizer_result
                ],
            )
            for result_dict in [json.loads(result) for result in results]
        ]

        anonymized_data = anonymizer.anonymize_dict(
            analyzer_results=analyzer_results, **kwargs
        )
        return anonymized_data

    elif isinstance(input_data, list):
        # Input is a list of strings, perform anonymize_list
        texts = input_data
        analyzer_results = []
        for result in results:
            result_dict = json.loads(result)
            recognizer_results = [
                RecognizerResult(
                    entity_type=r["entity_type"],
                    start=r["start"],
                    end=r["end"],
                    score=r["score"],
                )
                for recognizer_result in result_dict["recognizer_results"]
                if recognizer_result
                for r in recognizer_result
            ]
            analyzer_results.append(recognizer_results)

        anonymized_texts = anonymizer.anonymize_list(
            texts=texts, recognizer_results_list=analyzer_results, **kwargs
        )
        return anonymized_texts

    else:
        raise ValueError("Invalid input type. Expected Dict[str, str] or List[str].")
