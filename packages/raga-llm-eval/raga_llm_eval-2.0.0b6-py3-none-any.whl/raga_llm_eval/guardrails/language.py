from enum import Enum
from typing import Dict, List, Optional, Sequence, Union

import nltk

from .anonymize_helpers.transformers_helpers import pipeline, get_tokenizer_and_model_for_classification
from .match_type import MatchType
from .utils import calculate_risk_score


def split_text_by_sentences(text: str) -> List[str]:
    nltk = lazy_load_dep("nltk")

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    return nltk.sent_tokenize(text.strip())


default_model_path = (
    "papluca/xlm-roberta-base-language-detection",
    "ProtectAI/xlm-roberta-base-language-detection-onnx",
)


class Language:
    """
    A class for scanning the prompt for language detection.

    Note: when no languages are detected above the threshold, the prompt is considered valid.
    """

    def __init__(
        self,
        prompt: str,
        valid_languages: Sequence[str] = ["en"],
        model_path: Optional[str] = None,
        threshold: float = 0.6,
        match_type: Union[MatchType, str] = MatchType.FULL,
        use_onnx: bool = False,
        model_kwargs: Optional[Dict] = None,
        pipeline_kwargs: Optional[Dict] = None,
    ):
        """
        Initializes the Language scanner with a list of valid languages.

        Parameters:
            prompt (str): The prompt to check for language.
            valid_languages (Sequence[str]): A list of valid language codes in ISO 639-1, default is ["en"].
            threshold (float): Minimum confidence score.
            match_type (str): Whether to match the "full" text or individual "sentences". Default is "full".
            use_onnx (bool): Whether to use ONNX for inference. Default is False.
            transformers_kwargs (Optional[Dict]): Optional keyword arguments for the transformers pipeline.
        """
        if isinstance(match_type, str):
            match_type = MatchType(match_type)

        self._prompt = prompt
        self._threshold = threshold
        self._valid_languages = valid_languages
        self._match_type = match_type

        default_pipeline_kwargs = {
            "max_length": 512,
            "truncation": True,
            "top_k": None,
        }
        if pipeline_kwargs is None:
            pipeline_kwargs = {}

        pipeline_kwargs = {**default_pipeline_kwargs, **pipeline_kwargs}
        model_kwargs = model_kwargs or {}
        onnx_model_path = model_path
        if model_path is None:
            model_path = default_model_path[0]
            onnx_model_path = default_model_path[1]
        tf_tokenizer, tf_model = get_tokenizer_and_model_for_classification(
            model=model_path, onnx_model=onnx_model_path, use_onnx=use_onnx, **model_kwargs
        )

        self._pipeline = pipeline(
            task="text-classification",
            model=tf_model,
            tokenizer=tf_tokenizer,
            **pipeline_kwargs,
        )

    def run(self) -> Dict[str, Union[str, bool, float]]:
        result = {
            "prompt": self._prompt,
            "is_passed": True,
            "score": 0.0,
            "evaluated_with": {
                "match_type": self._match_type.value,
                "valid_languages": self._valid_languages,
                "threshold": self._threshold,
            },
            "reason": "",
        }

        if self._prompt.strip() == "":
            return result

        prompt = self._prompt

        results_all = self._pipeline(self._match_type.get_inputs(prompt))

        for result_chunk in results_all:
            languages_above_threshold = [
                result["label"]
                for result in result_chunk
                if result["score"] > self._threshold
            ]

            highest_score = max([result["score"] for result in result_chunk])

            # Check if any of the languages above threshold are not valid
            if len(set(languages_above_threshold) - set(self._valid_languages)) >= 0:
                result["is_passed"] = False
                result["score"] = calculate_risk_score(highest_score, self._threshold)
                result["reason"] = f"Languages are found with high confidence{languages_above_threshold}"
                return result
        result["reason"] = "Only valid languages are found in the text."
        return result
