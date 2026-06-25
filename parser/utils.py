import json
import string
import fitz  # PyMuPDF
import os


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

def gemini_output_to_json(gemini_response):
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
    
    


    """Converts a PDF file to images, using the PDF filename as a base.

    Args:
        pdf_path: Path to the PDF file.
        output_folder: Path to the folder where images will be saved.
        zoom_x: Zoom factor for the x-axis (resolution multiplier).
        zoom_y: Zoom factor for the y-axis (resolution multiplier).
        image_format: Output image format (png, jpg, etc.). Defaults to png.
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        doc = fitz.open(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0] # Extract filename without extension

        for page_num in range(doc.page_count):
            page = doc[page_num]
            mat = fitz.Matrix(zoom_x, zoom_y)
            pix = page.get_pixmap(matrix=mat)

            img_path = os.path.join(output_folder, f"{pdf_name}_{page_num + 1}.{image_format}") # Use PDF name
            pix.save(img_path)

        print(f"Successfully converted {pdf_path} to images in {output_folder}")
        return True

    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return False
    except RuntimeError as e:
        print(f"Error converting {pdf_path}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
        

    
    
def remove_gemini_cache():
    x= []
    for n,f in enumerate(genai.list_files()):
        print(n, "  ", f.name)
        print(f.display_name)
        print(f.uri)
        print()
        x.append(f.display_name)
    for f in genai.list_files():
        if f.display_name in x:
            f.delete()
        
    

