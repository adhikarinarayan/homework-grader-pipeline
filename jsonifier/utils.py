import json
import string
import fitz  # PyMuPDF
import os
import base64

## compare output and json text
def compare_texts(text_answer, text_json):
    """
    Compares two texts, one containing answers and another a JSON-like string, 
    by counting words and characters after cleaning punctuation and JSON structures.

    Args:
        text_answer: The plain text string containing the answers.
        text_json:  The string containing JSON-like data (not a valid JSON object).

    Returns:
        A tuple containing:
            - answer_word_count: The number of words in the cleaned answer text.
            - answer_char_count: The number of characters in the cleaned answer text.
            - json_word_count: The number of words in the cleaned JSON-like text.
            - json_char_count: The number of characters in the cleaned JSON-like text.
            - is_same: if the words and char counts match (after cleaning).
    """


   # Clean the answer text (using replace)
    answer_text_cleaned = text_answer.lower()
    for char in string.punctuation:
        answer_text_cleaned = answer_text_cleaned.replace(char, "")

    # Clean the JSON-like text (using replace)
    json_text_cleaned = text_json.lower()
    for char in ['{', '}', '[', ']', '"']:
        json_text_cleaned = json_text_cleaned.replace(char, "")
    for char in string.punctuation:  # Also remove punctuation from JSON-like string.
        json_text_cleaned = json_text_cleaned.replace(char, "")

    # Count words and characters
    answer_word_count = len(answer_text_cleaned.split())
    answer_char_count = len(answer_text_cleaned)  # No need to subtract spaces as they're counted as characters
    json_word_count = len(json_text_cleaned.split())
    json_char_count = len(json_text_cleaned)
    
    
    return answer_word_count, answer_char_count, json_word_count, json_char_count


## output to json object

def output_to_json(gemini_response):
    """
    Attempts to parse the output of the Gemini API into a JSON object.

    Args:
        gemini_response: The raw text string returned by the Gemini API.

    Returns:
        A JSON object (Python dictionary) if parsing is successful,
        or None if a JSONDecodeError occurs.  Includes error messages 
        to aid in debugging.
    """
    try:
        # Find the start and end markers for the JSON
        start = gemini_response.find("{")
        end = gemini_response.rfind("}") + 1 # +1 to include the closing brace

        if start == -1 or end == -1 or start >= end:
            return None, "No valid JSON object found in the response."  # Or raise an exception

        json_string = gemini_response[start:end]  # Extract the JSON string


        json_data = json.loads(json_string)
        return json_data, None # Success

    except json.JSONDecodeError as e:
        error_message = f"JSONDecodeError: {e}.  Raw response: {gemini_response}"
        return None, error_message
    except Exception as e:  # Catch other potential errors (e.g., unexpected format)
        error_message = f"An unexpected error occurred: {e}.  Raw response: {gemini_response}"
        return None, error_message


def extract_replies(json_data):
    """Flattens all reply fields from a structured answer JSON into a single string."""
    text = ""
    for q in json_data.get("questions", []):
        if "reply" in q:
            text += str(q["reply"]) + "\n"
        for sp in q.get("subparts", []):
            if "reply" in sp:
                text += str(sp["reply"]) + "\n"
    return text.strip()


def jaccard_similarity(text1, text2):
    """Token-level Jaccard similarity between two strings."""
    tokens1 = set(text1.lower().split())
    tokens2 = set(text2.lower().split())
    if not tokens1 and not tokens2:
        return 1.0
    return len(tokens1 & tokens2) / len(tokens1 | tokens2)
    
    




