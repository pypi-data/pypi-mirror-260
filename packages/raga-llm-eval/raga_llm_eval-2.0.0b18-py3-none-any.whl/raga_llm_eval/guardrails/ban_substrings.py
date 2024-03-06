import os
import re
from enum import Enum
from typing import Sequence, Union


class MatchType(Enum):
    STR = "str"
    WORD = "word"

    def match(self, text: str, substring: str) -> bool:
        if self == MatchType.STR:
            return substring in text

        if self == MatchType.WORD:
            return re.search(r"\b" + substring + r"\b", text) is not None


class BanSubstrings:
    """
    BanSubstrings class is used to ban certain substrings from appearing in the prompt.

    The match can be done either at a string level or word level.
    """

    def __init__(
        self,
        prompt: str,
        substrings: Sequence[str],
        case_sensitive: bool = False,
    ):
        self._prompt = prompt
        self._case_sensitive = case_sensitive
        self._substrings = substrings

    @staticmethod
    def remove_substrings(text, substrings, case_sensitive=False):
        substrings.sort(reverse=True)
        flags = 0 if not case_sensitive else re.IGNORECASE
        regex = re.compile("|".join(map(re.escape, substrings)), flags=flags)
        redacted_text = regex.sub("[REDACTED]", text)
        redacted_count = redacted_text.count("[REDACTED]")
        return redacted_text, redacted_count

    def run(self) -> dict:
        redacted_text, redacted_count = self.remove_substrings(
            self._prompt, self._substrings, self._case_sensitive
        )

        is_passed = True
        reason = "No banned substrings found in prompt."
        score = 1.0
        if redacted_count != 0:
            is_passed = False
            reason = "Banned substrings found in prompt."
            score = 0.0

        result = {
            "prompt": self._prompt,
            "is_passed": is_passed,
            "reason": reason,
            "score": score,
            "evaluated_with": {
                "substrings": self._substrings,
            },
            "sanitized_prompt": redacted_text,
        }

        return result
