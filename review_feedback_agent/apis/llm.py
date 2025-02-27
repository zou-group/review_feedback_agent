import os
from typing import Union, List, Dict, Any
import textgrad as tg


class LLM:
    def __init__(self, model_name: str = "sonnet-3.5"):
        self.model_name = model_name
        self.engine = tg.get_engine(model_name, cache_or_not=False)

    def __call__(self, message: Union[List[Dict[str, str]], str], system_prompt: str):
        return self.engine(message, system_prompt=system_prompt)
