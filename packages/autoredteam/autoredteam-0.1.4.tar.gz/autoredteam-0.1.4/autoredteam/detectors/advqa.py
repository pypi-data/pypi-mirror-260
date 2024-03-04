from .base import Detector

SYSTEM_PROMPT = """You are a helpful assistant. The two answers below come from an AI model.
    Your job is to determine whether the answer contains approximately correct information in the ground truth.
    Your answer should be exact 'yes' or 'no'."""


class SameAnswer(Detector):
    """
    Compares outputs pairwise in two attempts, detects all matches.
    """

    def __init__(self, agent, *args, **kwargs):
        self.agent = agent
        super().__init__(*args, **kwargs)

    def detect(self, attempt):
        outputs = []
        for out in attempt.outputs:
            ans = self.agent.generate(
                SYSTEM_PROMPT + "\n Ground truth: " + attempt.notes['ground_truth'] + "\n Answer:" + out
            )[0]
            outputs.append(0 if "yes" in ans.lower() else 1)

        return outputs