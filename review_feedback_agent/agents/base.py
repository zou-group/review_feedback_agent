from abc import ABC, abstractmethod
from review_feedback_agent.apis import LLM
import textgrad as tg


class Component(tg.autograd.Module):
    def __init__(self, llm_api: LLM, system_prompt: str):
        self.llm_api = llm_api
        self.system_prompt = system_prompt

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
