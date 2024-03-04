import os
import requests
from .base import Agent


class RestAPI(Agent):
    """
    Generic class for creating an Agent based on an URL and API token.
    Takes as input a json file or dict.
    """

    # def __init__(self, name, config: AgentConfig=None):
    def __init__(
        self,
        config,
        generations: int = 10
    ):

        print("Loading REST Agent: ", config['name'])
        self.family = "REST"

        # check for the environment variable
        if config['token_name'] not in os.environ:
            raise ValueError(
                f"Put the {self.family} API token in the {config['token_name']} environment variable\n \
                e.g.: export {config['token_name']}='abc123'"
            )
        os.environ["REST_API_TOKEN"] = os.getenv(config['token_name'])

        self.config = config
        self.generations = generations
        self.fullname = "autoredteam.agents.rest.RestAPI"

        # define response parser
        exec(self.config['output_handler'])
        self.parse = locals()["parse"]

    def _call_model(self, prompt: str):

        # add prompt to payload
        payload = self.config['prompt_handler'].copy()
        for k, v in payload.items():
            if isinstance(v, str) and "$PROMPT" in v:
                payload[k] = v.replace("$PROMPT", prompt)
                
        response = requests.post(
            self.config['url'],
            headers={
                "Accept": "application/json",
                "Authorization": f"""Bearer {os.environ["REST_API_TOKEN"]}""",
                "Content-Type": "application/json"
            },
            json=payload
        )
        # return response
        return self.parse(response)

        # return self.config['response_handler'](response.json())

            #     """
    #     Initializes the Agent class, given a `name`.
    #     """
    #     print(f"Loading {self.family} Agent: {name}")
    #     with contextlib.redirect_stdout(None):
    #         super().__init__(name=name, generations=generations)

    #     # determine base uri
    #     self.uri = self.name + "https://bauzn496g1fv9lv0.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions"

    #     # determine model
    #     self.model = 'tgi'        

    #     # add api and base url to client to not conflict with other openai clients in the env
    #     self.agent = openai.OpenAI(api_key=os.getenv(token), base_url=self.uri)

    # @backoff.on_exception(
    #     backoff.fibo,
    #     (
    #         openai.BadRequestError,
    #         openai.AuthenticationError,
    #         openai.PermissionDeniedError,
    #         openai.NotFoundError,
    #         openai.UnprocessableEntityError,
    #         openai.RateLimitError,
    #         openai.InternalServerError,
    #         openai.APIConnectionError,
    #     ),
    #     max_value=70,
    # )
    # def _call_model(self, prompt):
    #     response = self.agent.chat.completions.create(
    #         model=self.model,
    #         messages=[
    #             # {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": prompt},
    #         ],
    #         stream = True,
    #         max_tokens=self.max_tokens,
    #         temperature=self.temperature,
    #         presence_penalty=self.presence_penalty,
    #     )
    #     return response.choices[0].message.content.strip()


default_class = "RestAPI"

# headers = {
# 	"Accept" : "application/json",
# 	"Authorization": f"""Bearer {REST_API_TOKEN}""",
# 	"Content-Type": "application/json" 
# }

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()

# output = query({
# 	"inputs": "<s>[INST] <<SYS>> You are a helpful assistant. You keep your answers short. <</SYS>> What is your favourite condiment? [/INST] My favorite condiment is ketchup. It is versatile, tasty, and goes well with a variety of foods. </s><s>[INST] And what do you think about it? [/INST]",
# 	"parameters": {
# 		"max_new_tokens": 150
# 	}
# })
