from pypdf import PdfReader
import os
import openreview
from typing import Tuple
import logging
import urllib.request

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PaperNotFoundError(Exception):
    """Raised when a paper ID cannot be found"""
    pass


class PDFParsingError(Exception):
    """Raised when there's an error parsing a PDF"""
    pass


class ReviewNotFoundError(Exception):
    """Raised when a review ID cannot be found"""
    pass


def pdf_to_text(pdf_path: str) -> str:
    """
    Converts paper PDF to a text string

    Params:
        pdf_path: local path to paper PDF

    Returns:
        paper_text: paper PDF's text
    """
    try:
        paper_text = ""
        logger.info(f"Parsing the pdf {pdf_path}")
        reader = PdfReader(pdf_path)
        number_of_pages = len(reader.pages)
        for p in range(number_of_pages):
            page = reader.pages[p].get_object()
            text = page.extract_text()
            paper_text += text.encode('utf-8', errors='ignore').decode('utf-8') # removes invalid characters by ignoring encoding errors

        return paper_text
    except Exception as e:
        logger.error(f"Error parsing PDF {pdf_path}: {str(e)}")
        raise PDFParsingError(f"Failed to parse PDF: {str(e)}")


def get_openreview_paper(paper_id: str) -> str:
    """
    Retrieve text from paper pdf using desired paper ID

    Params:
        paper_id: str representing paper ID

    Returns:
        pdf_text: paper PDF's text
    """
    
    pdf_path = f"./{paper_id}.pdf"
    paper_url = f"https://openreview.net/pdf?id={paper_id}"

    try:
        urllib.request.urlretrieve(paper_url, pdf_path)
    except urllib.error.URLError as e:
        logger.error(f"Failed to download paper with ID {paper_id}: {str(e)}")
        raise PaperNotFoundError(f"Failed to download paper with ID {paper_id}")

    try:
        pdf_text = pdf_to_text(pdf_path)
        return pdf_text
    except PDFParsingError as e:
        raise
    finally:
        print('Removing downloaded PDF')
        os.remove(pdf_path)  # Clean up the downloaded PDF file


def get_openreview_paper_and_review(review_id: str, paper_id: str) -> Tuple[str, str]:
    """
    Retrieve review text from paper pdf using desired paper ID and review ID

    Params:
        review_id: str representing review ID
        paper_id: str representing paper ID

    Returns:
        review_content_formatted: formatted review text
        pdf_text: paper PDF's text
    """
    
    try:
        openreview_client = openreview.api.OpenReviewClient(
            baseurl="https://api2.openreview.net"
        )
    except openreview.OpenReviewException as e:
        raise e

    try:
        review = openreview_client.get_note(review_id)
        review_content = review.content
    except openreview.OpenReviewException:
        logger.error(f"Review {review_id} not found")
        raise ReviewNotFoundError(f"Review {review_id} not found")

    # Reformat review content
    headers_to_keep = ['Summary', 'Strengths', 'Weaknesses', 'Questions']

    review_content_formatted = []
    for section, content in review_content.items():
        header = section.replace("_", " ").title()
        if header in headers_to_keep:
            review_content_formatted.append(f"**{header}**: {content['value']}")
    review_content_formatted = "\n\n".join(review_content_formatted)

    try:
        pdf_text = get_openreview_paper(paper_id)
    except PaperNotFoundError as e:
        raise e

    return review_content_formatted, pdf_text


def get_review_id(paper_id: str, reviewer_id: str) -> str:
    """
    Retrieve review ID from reviewer ID

    Params:
        paper_id: str representing paper ID
        reviewer_id: str representing reviewer ID

    Returns:
        review_id: str representing review ID
    """
    
    try:
        openreview_client = openreview.api.OpenReviewClient(
            baseurl="https://api2.openreview.net"
        )
    except openreview.OpenReviewException as e:
        raise e

    try:
        note = openreview_client.get_notes(paper_id, details='replies')[0]
    except openreview.OpenReviewException:
        logger.error(f"Error getting note from paper_id: {paper_id}")
        raise PaperNotFoundError(f"Error getting note from paper_id: {paper_id}")

    desired_review = next(
            i
            for i, entry in enumerate(note.details["replies"])
            if entry["signatures"][0].split("_")[-1] == reviewer_id
        )

    review_id = note.details['replies'][desired_review]['id']

    return review_id


def parse_uploaded_paper(pdf_path: str) -> Tuple[str, str]:
    """
    Returns paper's text given the path to pdf

    Params:
        pdf_path: path to pdf (locally)

    Returns:
        pdf_text: paper's PDF text
    """
    try:
        pdf_text = pdf_to_text(pdf_path)
        return pdf_text
    except PDFParsingError as e:
        raise e
