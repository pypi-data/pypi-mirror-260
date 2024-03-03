from typing import Dict, Optional

from .utils import pipeline

model_path = (
    "papluca/xlm-roberta-base-language-detection",
    "ProtectAI/xlm-roberta-base-language-detection-onnx",
)


class LanguageSame:
    """
    LanguageSame class is responsible for detecting and comparing the language of given prompt and model output to ensure they are the same.
    """

    def __init__(
        self,
        prompt,
        response,
        threshold=0.1,
        use_onnx: bool = False,
        transformers_kwargs: Optional[Dict] = None,
    ):
        """
        Initializes the LanguageSame scanner.

        Args:
        - question: str, the question to be evaluated for contextual relevancy
        - retrieval_context: list of str, the retrieval context for the question
        - include_reason: bool, whether to include the reason for the evaluation (default True)
        - model: str, the name of the OpenAI model to be used (default 'gpt-3.5-turbo')
        - threshold: float, the threshold for the relevancy score (default 0.5)
        - use_onnx (bool): Whether to use ONNX for inference. Default is False.
        - transformers_kwargs (dict): Additional keyword arguments to pass to the transformers pipeline.
        """
        self.prompt = prompt
        self.output = response
        self._threshold = threshold
        self.use_onnx = use_onnx

        transformers_kwargs = transformers_kwargs or {}
        transformers_kwargs["max_length"] = 512
        transformers_kwargs["truncation"] = True
        transformers_kwargs["top_k"] = None

        self._pipeline = pipeline(
            task="text-classification",
            model=model_path[0],
            onnx_model=model_path[1],
            use_onnx=use_onnx,
            **transformers_kwargs,
        )

    def run(self):
        score = 1.0
        if self.prompt.strip() == "" or self.output.strip() == "":
            score = 1.0

        detected_languages = self._pipeline([self.prompt, self.output])
        prompt_languages = [
            detected_language["label"]
            for detected_language in detected_languages[0]
            if detected_language["score"] > self._threshold
        ]
        output_languages = [
            detected_language["label"]
            for detected_language in detected_languages[1]
            if detected_language["score"] > self._threshold
        ]

        if len(prompt_languages) == 0:
            score = 0.0

        if len(output_languages) == 0:
            score = 0.0

        common_languages = list(set(prompt_languages).intersection(output_languages))

        if len(common_languages) == 0:
            score = 0.0

        result = {
            "prompt": self.prompt,
            "context": self.output,
            "score": score,
            "threshold": self._threshold,
            "is_passed": "Passed" if score >= self._threshold else "Failed",
            "evaluated_with": {"task": self._pipeline.task, "onnx": self.use_onnx},
        }

        return result
