import contextlib

from .base import Perturbation
from ..agents.openai import OpenaiAgent
import garak.buffs.paraphrase as pp_buff

"""This module contains perturbations that generate paraphrases of a prompt or prompts in a test."""

# this = sys.modules[__name__]


class PegasusT5(Perturbation):
    """Perturbations that generate paraphrases of a prompt or prompts in a test."""

    name = "paraphrase.PegasusT5"
    description = "Paraphrase perturbation using PegasusT5"

    def __init__(self, num_paraphrases=6):
        self.num_paraphrases = num_paraphrases
        with contextlib.redirect_stdout(None):
            self.buff = pp_buff.PegasusT5()
        self.buff.num_return_sequences = self.num_paraphrases
        self.buff.num_beams = self.num_paraphrases
        self.uri = self.buff.uri
        self.__doc__ = self.buff.__doc__

        super().__init__()

    def perturb_prompt(self, prompt: str):
        return self.buff._get_response(prompt)
    

# PP_TEMPLATE = """Today I want you to learn the ways of paraphrasing a sentence. Below are few methods with examples. Go through them carefully.

# 1. Use synonyms
# Sentence: Can you explain the attempts made by the research to discover reasons for this phenomenon?
# Paraphrase: Can you clarify the efforts undertaken by the research to unearth the causes behind this phenomenon?

# 2. Change word forms (parts of speech)
# Sentence: How did the teacher assist the students in registering for the course?
# Paraphrase: In what manner did the teacher support the students in completing the course registration?

# 3. Change the structure of a sentence
# Sentence: Which of the discussed spectroscopic methods is the most recently developed technique?
# Paraphrase: Among the spectroscopic methods discussed, which technique has been developed most recently?

# 4. Change conjunctions
# Sentence: Did you want to go to the store, but were you too busy?
# Paraphrase: Although you were busy, did you still want to go to the store?

# 5. Use idioms
# Sentence: How would you describe his emotional state as being very sad?
# Paraphrase: How would you depict him feeling down in the dumps?

# Now you have to paraphrase a given sentence using one of the techniques mentioned above. I will provide you the number of the technique to use.
# Technique Number: {method}
# Sentence: {sentence}
# Paraphrase:"""


# class llm(Perturbation):
#     """Paraphrase perturbation using Language Model"""

#     name = "paraphrase.llm"
#     description = "Paraphrase perturbation using Language Model"

#     def __init__(self, name='gpt-3.5-turbo', num_paraphrases=6):
#         self.num_paraphrases = num_paraphrases
#         self.name = name
#         super().__init__()

#     def perturb_prompt(self, prompt: str):
#         pp_agent = OpenaiAgent(name=self.name, generations=1)
        
#         return [
#             pp_agent.generate(
#                 PP_TEMPLATE.format(
#                     method=i + 1,
#                     sentence=prompt)
#             )
#             for i in range(5)
#         ]


# # TODO: make Fast work
# buff_list = ["PegasusT5", "Fast"]
# for buff_name in buff_list:
#     buff_instance = getattr(buff_module, buff_name)()

#     setattr(
#         this,
#         buff_name,
#         type(
#             buff_name,
#             (Perturbation,),
#             {
#                 "__init__": local_constructor,
#                 "__doc__": buff_instance.__doc__,
#                 "buff": buff_instance,
#                 "uri": buff_instance.uri,
#                 "num_return_sequences": buff_instance.num_return_sequences,
#                 "num_beams": buff_instance.num_beams,
#                 "perturb_prompt": perturb_prompt
#             },
#         ),
#     )
