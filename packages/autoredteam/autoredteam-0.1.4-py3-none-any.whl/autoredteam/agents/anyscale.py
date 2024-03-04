import backoff
import os
import openai

# from .base import AgentAPI
from .base import Agent

# from ..engine.config import AgentConfig
from garak import _config


# class AnyscaleAPI(AgentAPI):
#     generator_family_name = "Anyscale"

#     def __init__(self, name, generations: int = 10):
#         anyscale_token = os.getenv("ANYSCALE_API_TOKEN", default=None)
#         if anyscale_token is None:
#             raise ValueError(
#                 'Put the Anyscale API token in the ANYSCALE_API_TOKEN environment variable\n \
#                 e.g.: export ANYSCALE_API_TOKEN="esecret_1234567890abcdefg"'
#             )

#         super().__init__(
#             base_url='https://api.endpoints.anyscale.com/v1/',
#             name=name,
#             token=anyscale_token,
#             family="Anyscale",
#             generations=generations
#         )


class AnyscaleAPI(Agent):
    """
    A generator that uses Anyscale APIs to generate text.
    """

    stream = True
    generator_family_name = "Anyscale"
    # supports_multiple_generations = True

    def __init__(self, name, generations: int = 10):
        # def __init__(self, name, config: AgentConfig=None):

        if hasattr(_config.run, "seed"):
            self.seed = _config.run.seed

        self.family = "Anyscale"
        super().__init__(name, generations)
        # super().__init__(name, config)
        token_name = "ANYSCALE_API_TOKEN"
        if token_name not in os.environ:
            raise ValueError(
                f'''Put the Anyscale API token in the {token_name} environment variable\n \
                e.g.: export {token_name}="esecret_1234567890abcdefg"'''
            )
        # add api and base url to client to not conflict with other openai clients in the env
        self.agent = openai.OpenAI(
            api_key=os.getenv(token_name),
            base_url="https://api.endpoints.anyscale.com/v1",
        )

    @backoff.on_exception(
        backoff.fibo,
        (
            openai.BadRequestError,
            openai.AuthenticationError,
            openai.PermissionDeniedError,
            openai.NotFoundError,
            openai.UnprocessableEntityError,
            openai.RateLimitError,
            openai.InternalServerError,
            openai.APIConnectionError,
        ),
        max_value=70,
    )
    def _call_model(self, prompt):
        response = self.agent.chat.completions.create(
            model=self.name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            # n=self.generations,
            # top_p=self.top_p,
            presence_penalty=self.presence_penalty,
            # stream=self.stream
        )
        return response.choices[0].message.content
        # res = [c.message.content for c in response.choices]
        # print(res)
        # return res


default_class = "AnyscaleAPI"
