from typing import List, Dict, Any, Callable
import re
from review_feedback_agent.agents.components import (
    FeedbackActor,
    Aggregator,
    FeedbackCritic,
    Formatter
)
from review_feedback_agent.utils.utils import logger


class FeedbackAgent:
    def __init__(self, llm_api: Any, architecture: str = "Actor(2)->Aggregator->FeedbackCritic->Formatter"):
        """
        Initialize FeedbackAgent with a string-based architecture and LLM API

        Params:
            llm_api: The LLM API to be used for initializing components
            architecture: A string describing the architecture, set to the default: "Actor(2)->Aggregator->FeedbackCritic->Formatter"
        """
        self.llm_api = llm_api
        self.components = self._initialize_components()
        self.sequence = self._parse_architecture(architecture)

    def _initialize_components(self) -> Dict[str, Callable]:
        """
        Initialize all possible components with the LLM API

        Returns:
            dict: mapping component name (str) to initialized component
        """

        return {
            "Formatter": Formatter(self.llm_api),
            "Aggregator": Aggregator(self.llm_api),
            "FeedbackCritic": FeedbackCritic(self.llm_api),
            "Actor": FeedbackActor(self.llm_api),
        }

    def _parse_architecture(self, arch_string: str) -> List[Callable]:
        """
        Parse the architecture string into a list of callable components

        Params:
            arch_string: string representing desired architecture

        Returns:
            list: list of components in desired order based on arch_string
        """

        def parse_component(component_str):
            match = re.match(r"(\w+)(?:\((\d+)\))?", component_str)
            if not match:
                raise ValueError(f"Invalid component specification: {component_str}")
            name, count = match.groups()
            count = int(count) if count else 1
            if name not in self.components:
                raise ValueError(f"Unknown component: {name}")
            return [self.components[name]] * count

        return [
            comp
            for part in arch_string.split("->")
            for comp in parse_component(part.strip())
        ]

    def __call__(self, pdf_text: str, review_content: str) -> Dict[str, Any]:
        state = {
            "paper": pdf_text,
            "review": review_content,
            "feedback_list": [],
            "aggregated_feedback": None,
            "critiqued_feedback": None,
            "formatted_feedback": None,
        }

        for step, component in enumerate(self.sequence):
            logger.info(f"Running step {step + 1}: {component.__class__.__name__}")

            if isinstance(component, FeedbackActor):
                feedback = component(paper=state["paper"], review=state["review"])
                state["feedback_list"].append(feedback)
            elif isinstance(component, Aggregator):
                assert (
                    len(state["feedback_list"]) > 1
                ), f"Total feedback: {len(state['feedback_list'])}. Have at least 2 feedback to aggregate."
                state["aggregated_feedback"] = (
                    component(
                        feedbacks=state["feedback_list"],
                        paper=state["paper"],
                        review=state["review"],
                    )
                    if len(state["feedback_list"]) > 1
                    else state["feedback_list"][0]
                )
            elif isinstance(component, FeedbackCritic):
                assert (
                    state["aggregated_feedback"] or len(state["feedback_list"]) == 1
                ), "No feedback to critique. Have a single feedback or run Aggregator first."
                state["critiqued_feedback"] = component(
                    paper=state["paper"],
                    review=state["review"],
                    feedback=state["aggregated_feedback"] or state["feedback_list"][0],
                )
            elif isinstance(component, Formatter):
                assert (
                    state["critiqued_feedback"] or state["aggregated_feedback"]
                ), "No feedback to format. Run the FeedbackCritic or Aggregator first."
                state["formatted_feedback"] = component(
                    feedback=state["critiqued_feedback"] or state["aggregated_feedback"]
                )
                state["formatted_feedback"] = (
                    state["formatted_feedback"]
                    .replace("<quote>", "'")
                    .replace("</quote>", "'")
                )

        return {
            "initial feedback": state["feedback_list"],
            "aggregated feedback": state["aggregated_feedback"],
            "critiqued feedback": state["critiqued_feedback"],
            "formatted feedback": state["formatted_feedback"],
        }
