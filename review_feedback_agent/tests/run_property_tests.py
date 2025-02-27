from review_feedback_agent.tests.property_tests import PropertyTester
from typing import Tuple, List

def run_property_tests(feedback: str, review_text: str) -> Tuple[bool, List[str]]:
    """
    Runs all property tests on feedback, returns boolean representing if all tests passed or not and a list of names that failed

    Params:
        feedback: generated feedback
        review_text: review content

    Returns:
        bool: True if test passed, False otherwise
        List[str]: list of property test names we fail on, empty list if all tests passed
    """

    property_tester = PropertyTester()

    property_tests = ['praise_feedback', 'addressed_to_author', 'restate_reviewer', 'comments_in_review']
    failed_tests = []

    for test in property_tests:
        if not property_tester.test_property(test, feedback, review_text):
            failed_tests.append(test)

    return (len(failed_tests) == 0, failed_tests)
