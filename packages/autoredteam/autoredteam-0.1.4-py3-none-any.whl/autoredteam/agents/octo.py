# makes all the functions in the module available to the autoredteam.generators package

import contextlib
import os
import openai
from garak.generators.octo import OctoGenerator, InferenceEndpoint
from ..engine.config import _get_default_agent_config

# from ..engine.config import AgentConfig, _get_default_agent_config


class OctoAPI(OctoGenerator):
    def __init__(self, name, generations: int = 10):
        # def __init__(self, name, generations: int = 10, config: AgentConfig=None):

        self.family = "OctoAI"
        print(f"Loading {self.family} Agent: {name}")
        with contextlib.redirect_stdout(None):
            super().__init__(name, generations)

        # if config is None:
        config = _get_default_agent_config(family="", name=self.name)
        for field in [
            "max_tokens",
            "presence_penalty",
            "temperature",
            "top_k",
            "seed",
            "presence_penalty",
            "supports_multiple_generations",
        ]:
            if hasattr(config, field):
                setattr(self, field, getattr(config, field))


class OctoEndpoint(InferenceEndpoint):
    def __init__(self, name, generations: int = 10):
        # def __init__(self, name, generations: int = 10, config: AgentConfig=None):

        self.family = "OctoAI"
        print(f"Loading {self.family} Agent: {name}")
        with contextlib.redirect_stdout(None):
            super().__init__(name, generations)

        # if config is None:
        config = _get_default_agent_config(family="", name=self.name)
        for field in [
            "max_tokens",
            "presence_penalty",
            "temperature",
            "top_k",
            "seed",
            "presence_penalty",
            "supports_multiple_generations",
        ]:
            if hasattr(config, field):
                setattr(self, field, getattr(config, field))

class OctoEmbeddings():
    def __init__(self, name="thenlper/gte-large"):
        # def __init__(self, name, generations: int = 10, config: AgentConfig=None):

        self.family = "OctoAI"
        self.name = name
        print(f"Loading {self.family} Embedding Agent: {self.name}")

        token_name = "OCTO_API_TOKEN"
        if token_name not in os.environ:
            raise ValueError(
                f'''Put the Together API token in the {token_name} environment variable\n \
                e.g.: export {token_name}="esecret_1234567890abcdefg"'''
            )
        # add api and base url to client to not conflict with other openai clients in the env
        self.agent = openai.OpenAI(
            api_key=os.getenv(token_name),
            base_url="https://text.octoai.run/v1",
        )

    def embed_documents(self, query: str):
        """Embed a query using the model.
        
        Args:
            query (str): The query to embed.
        """
        response = self.agent.embeddings.create(
            model=self.name,
            input=[query]
        )
        return response.data[0].embedding


# more stable option is enabled by default
default_class = "OctoAPI"
