import unicodedata

class InvisibleText():
    """
    A class for scanning if the prompt includes invisible characters.

    This class uses the unicodedata library to detect invisible characters in the output of the language model.
    """

    def __init__(
            self, 
            prompt: str
            ):
        """
        Initializes InvisibleText.
        Args:
            prompt (str): The prompt to scan for invisible characters.
        Returns:
            dict: The result of the scan.
        """
        self._prompt = prompt
        self._banned_categories = ["Cf", "Cc", "Co", "Cn"]

    @staticmethod
    def contains_unicode(text: str):
        return any(ord(char) > 127 for char in text)

    def run(self) -> dict:
        result = {
                    'prompt': self._prompt, 
                    'reason': "No Invisible characters detected", 
                    'is_passed': True,
                    'score': 0.0,
                    'sanitized_prompt': self._prompt
                }
        prompt = self._prompt
        if not self.contains_unicode(prompt):
            return result

        chars = []
        for char in prompt:
            if unicodedata.category(char) not in self._banned_categories:
                continue

            chars.append(char)
            prompt = prompt.replace(char, "")

        if chars:
            result["sanitized_prompt"] = prompt
            result['reason'] = "Invisible characters found and removed."
            result['is_passed'] = False
            result['score'] = 1.0

        return result



