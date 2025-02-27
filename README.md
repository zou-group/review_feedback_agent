# Review Feedback Agent

This codebase implements the Review Feedback Agent, which is designed to provide feedback on peer-reviews at AI conferences. The input to our agent is a review to provide feedback on and the corresponding paper it was written about. The output is feedback to enhance the review quality by making it more specific and actionable for the authors.

We provide a tutorial of how to use the system and generate feedback for a review in our [example notebook](https://github.com/zou-group/review_feedback_agent/Example.ipynb). You will need to provide your own Anthropic API key in order to generate feedback.

## Setup
To run our notebook, you will need to set up a new environment. To do so, run the following commands:
```bash
git clone https://github.com/zou-group/review_feedback_agent.git
cd review_feedback_agent
conda create -n feedback_agent_env python=3.11
conda activate feedback_agent_env
pip install -r requirements.txt
```

<!-- ## Citation -->