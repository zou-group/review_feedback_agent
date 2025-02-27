from .prompts import (
    ACTOR_PROMPT,
    ACTOR_SYSTEM_PROMPT,
    AGGREGATOR_PROMPT,
    AGGREGATOR_SYSTEM_PROMPT,
    CRITIC_PROMPT,
    CRITIC_SYSTEM_PROMPT,
    FORMATTER_PROMPT,
    FORMATTER_SYSTEM_PROMPT,
)
from review_feedback_agent.agents.base import Component
from review_feedback_agent.apis import LLM
from typing import List


class FeedbackActor(Component):
    def __init__(self, llm_api: LLM, system_prompt: str = ACTOR_SYSTEM_PROMPT):
        """Component to generate feedback

        Params:
            llm_api: The LLM API to be used for initializing components.
                type llm_api: LLM        
            system_prompt: Actor system prompt
                type system_prompt: str
        """
        super().__init__(llm_api, system_prompt)

    def __call__(self, paper: str, review: str) -> str:
        return self.forward(paper, review)

    def forward(self, paper: str, review: str) -> str:
        return self.llm_api(
            message=ACTOR_PROMPT.format(review=review, paper=paper),
            system_prompt=self.system_prompt,
        )


class Aggregator(Component):
    def __init__(self, llm_api: LLM, system_prompt: str = AGGREGATOR_SYSTEM_PROMPT):
        """Component to aggregate feedback from multiple FeedbackActor components

        Params:
            llm_api: The LLM API to be used for initializing components.
                type llm_api: LLM        
            system_prompt: Aggregator system prompt
                type system_prompt: str
        """
        super().__init__(llm_api, system_prompt)

    def __call__(self, feedbacks: List[str], paper: str, review: str) -> str:
        return self.forward(feedbacks, paper, review)

    def forward(self, feedbacks: List[str], paper: str, review: str) -> str:
        formatted_feedback_list = ""
        for i in range(len(feedbacks)):
            formatted_feedback_list += f"<feedback_list-{i}>"
            formatted_feedback_list += feedbacks[i]
            formatted_feedback_list += f"</feedback_list-{i}>\n"

        return self.llm_api(
            message=AGGREGATOR_PROMPT.format(
                feedbacks=formatted_feedback_list, review=review, paper=paper
            ),
            system_prompt=self.system_prompt,
        )


class FeedbackCritic(Component):
    def __init__(self, llm_api: LLM, system_prompt: str = CRITIC_SYSTEM_PROMPT):
        """Component to edit content of feedback

        Params:
            llm_api: The LLM API to be used for initializing components.
                type llm_api: LLM        
            system_prompt: Critic system prompt
                type system_prompt: str
        """
        super().__init__(llm_api, system_prompt)

    def __call__(self, paper: str, review: str, feedback: str) -> str:
        return self.forward(paper, review, feedback)

    def forward(self, paper: str, review: str, feedback: str) -> str:
        return self.llm_api(
            message=CRITIC_PROMPT.format(feedback=feedback, review=review, paper=paper),
            system_prompt=self.system_prompt,
        )


class Formatter(Component):

    def __init__(self, llm_api: LLM, system_prompt: str = FORMATTER_SYSTEM_PROMPT):
        """ Component to format final feedback

        Params:
            llm_api: The LLM API to be used for initializing components.
                type llm_api: LLM        
            system_prompt: Formatter system prompt
                type system_prompt: str
        """
        super().__init__(llm_api, system_prompt)

    def __call__(self, feedback: str) -> str:
        return self.forward(feedback)

    def forward(self, feedback: str) -> str:
        return self.llm_api(
            message=FORMATTER_PROMPT.format(feedback=feedback),
            system_prompt=self.system_prompt,
        )
