from typing import List
from autoredteam.agents.base import Agent
from autoredteam.agents.anyscale import AnyscaleAPI
from autoredteam.agents.openai import OpenaiAgent

class AIConfigAgent(Agent):

    def __init__(self, name, provider, generations):
        self.name = name
        self.provider = provider
        self.generations = generations
        self.model = None
        self.fullname = 'autoredteam.agents.aiconfig.AIConfigAgent'
        
        try:
            if self.provider == 'Anyscale':
                self.model = AnyscaleAPI(name=name, generations=self.generations)
            elif self.provider == 'OpenAI':
                self.model = OpenaiAgent(name=name, generations=self.generations)
            else:
                raise ValueError("Invalid provider specified.")
        except Exception as e:
            print(f"An error occurred during initialization: {e}")
    
    def _call_model(self, prompt: str) -> List[str] | str | None:
        return self.model._call_model(prompt)
    