import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from garak import _config
from .base import Agent


class MistralAPI(Agent):
    """
    A generator that uses Mistral APIs to generate text.
    """

    # stream = True
    generator_family_name = "Mistral"

    def __init__(self, name, generations: int = 10):
        # def __init__(self, name, config: AgentConfig=None):

        if hasattr(_config.run, "seed"):
            self.seed = _config.run.seed

        self.family = "Mistral"
        super().__init__(name, generations)
        # super().__init__(name, config)
        token_name = "MISTRAL_API_TOKEN"
        if token_name not in os.environ:
            raise ValueError(
                f'''Put the Together API token in the {token_name} environment variable\n \
                e.g.: export {token_name}="esecret_1234567890abcdefg"'''
            )
        self.agent = MistralClient(api_key=os.getenv(token_name))

    def _call_model(self, prompt):
        response = self.agent.chat(
            model=self.name,
            messages=[
                ChatMessage(role="system", content="You are a helpful assistant."),
                ChatMessage(role="user", content=prompt),
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            # stream=self.stream
        )

        # TODO: add streaming: https://docs.mistral.ai/platform/client/
        return response.choices[0].message.content.strip()


default_class = "MistralAPI"
