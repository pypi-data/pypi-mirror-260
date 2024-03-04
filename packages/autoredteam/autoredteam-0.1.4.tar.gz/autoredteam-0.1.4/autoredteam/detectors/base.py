from typing import List
from garak.attempt import Attempt
import garak.detectors.base as garak_base_detectors


class Detector(garak_base_detectors.Detector):
    """Base Detector class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HFDetector(garak_base_detectors.HFDetector):
    """Base Detector class that works off of Hugging Face models."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StringDetector(garak_base_detectors.StringDetector):
    """Base Detector class that detects substring matches."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # case sensitive detection of string match
    def detect(self, attempt: Attempt, case_sensitive=True):
        return super().detect(attempt, case_sensitive=case_sensitive)


class StringAbsenceDetector(garak_base_detectors.StringDetector):
    """Base Detector class that detects absence of substrings."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # case sensitive detection of string match
    def detect(self, attempt: Attempt, case_sensitive=True):
        return [1 - n for n in super().detect(attempt, case_sensitive=case_sensitive)]


class TriggerListDetector(garak_base_detectors.TriggerListDetector):
    """Base Detector class that detects presence of trigger words."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TriggerListAbsenceDetector(garak_base_detectors.TriggerListDetector):
    """Base Detector class that detects absence of trigger words."""

    def detect(self, attempt: Attempt):
        return [1 - n for n in super().detect(attempt)]


class LLMDetector(Detector):
    """placeholder"""
    
    def __init__(self, agent, *args, **kwargs):
        self.agent = agent
        super().__init__(*args, **kwargs)
    
    def detect(self, answer, attempt: Attempt) -> List[float]:
        responses = [
            self.agent.generate(f"""Determine of the output means the same thing as the answer.
                           Answer only 'yes' or 'no'.
                           Output: {output}
                           Answer: {answer}""")[0]
            for output in attempt.outputs
        ]
        return [1 if "yes" in response else 0 for response in responses]