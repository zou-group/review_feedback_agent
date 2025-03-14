# Review Feedback Agent

This codebase implements the Review Feedback Agent, which is designed to provide feedback on peer-reviews at AI conferences. The input to our agent is a review to provide feedback on and the corresponding paper it was written about. The output is feedback to enhance the review quality by making it more specific and actionable for the authors.

We provide a tutorial of how to use the system and generate feedback for a review in our [example notebook](https://github.com/zou-group/review_feedback_agent/blob/main/Example.ipynb). You will need to provide your own Anthropic API key in order to generate feedback.

## Setup
To run our notebook, you will need to set up a new environment. To do so, run the following commands:
```bash
git clone https://github.com/zou-group/review_feedback_agent.git
cd review_feedback_agent
conda create -n feedback_agent_env python=3.11
conda activate feedback_agent_env
pip install -r requirements.txt
```

## Running our code
See our [example notebook](https://github.com/zou-group/review_feedback_agent/blob/main/Example.ipynb) for a complete walkthrough of running Review Feedback Agent.

We initialize our agent using the Claude Sonnet-3.5 model:
```python
llm_api = LLM("sonnet-3.5")
agent = FeedbackAgent(llm_api)
```

The agent takes as input a review and paper and generates feedback for that review. You can either specify an existing review on OpenReview or upload your own. 

To specify a review using its OpenReview ID, use the following:
```python
# Insert your OpenReview paper ID (e.g. xC8xh2RSs2) and reviewer ID (e.g. gNxe) here

paper_id = ''
reviewer_id = ''

# Get review text and paper PDF text

review_id = get_review_id(paper_id, reviewer_id)
review_text, pdf_text = get_openreview_paper_and_review(review_id, paper_id)
```

Or if you want to input your own review text directly, run the following:
```python
review_text = ''
path_to_pdf = '' # Note: paper needs to be downloaded locally

pdf_text = parse_uploaded_paper(path_to_pdf)
```
Then, once you have the parsed review and paper text, you can generate feedback for the review by running:

```python
feedback_dict = agent(pdf_text, review_text)
formatted_feedback = feedback_dict["formatted feedback"]
```
Finally, you can check if the feedback will pass our reliability tests by running:

```python
reliability_test_output = run_reliability_tests(formatted_feedback, review_text)
```

Where `reliability_test_output[0]` is a boolean representing whether the feedback passed all tests or not, and `reliability_test_output[1]` is a list of the test names that failed (if any did).

<!-- ## Citation -->