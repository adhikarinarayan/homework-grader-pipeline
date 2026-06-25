import json
import pandas as pd
from models import *
def extract_qa_pairs(qp_json, sol_json, standard_sol_json=None):
    """
    Extracts question-answer pairs, handling questions with and without subparts.

    Args:
        qp_json: JSON object representing the question paper.
        sol_json: JSON object representing the student's solutions.
        standard_sol_json: Optional JSON object representing the standard solutions.

    Returns:
        A list of dictionaries, where each dictionary represents a question-answer pair.
        Returns an empty list if there's a mismatch in question structure or missing keys.
    """

    try:
        qp_questions = qp_json['questions']
        sol_answers = sol_json.get('questions', [])
        standard_sol_answers = standard_sol_json.get('questions', []) if standard_sol_json else []

        qa_pairs = []

        for i in range(len(qp_questions)):
            qp_q = qp_questions[i]
            sol_a = sol_answers[i] if i < len(sol_answers) else {}  # Safe access
            standard_sol_a = standard_sol_answers[i] if standard_sol_json and i < len(standard_sol_answers) else {}

            if 'subparts' in qp_q:
                qp_subparts = qp_q['subparts']
                sol_subparts = sol_a.get('subparts', [])
                standard_sol_subparts = standard_sol_a.get('subparts', []) if standard_sol_a else []

                for j in range(len(qp_subparts)):
                    qp_subpart = qp_subparts[j]
                    sol_subpart = sol_subparts[j] if j < len(sol_subparts) else {}
                    standard_sol_subpart = standard_sol_subparts[j] if standard_sol_subparts and j < len(standard_sol_subparts) else {}

                    qa_pairs.append({
                        'question': qp_subpart['description'],
                        'student_answer': sol_subpart.get('reply', ""),
                        'rubric': standard_sol_subpart.get('rubric', "") if standard_sol_subpart else None,
                        'max_marks': qp_subpart['max_marks'],
                        'question_number': qp_q['question_number'],
                        'subpart': qp_subpart.get('subpart', None) # Handle missing 'subpart'
                    })
            else:  # Handle questions without subparts
                qa_pairs.append({
                    'question': qp_q.get('description', ""),  # Get description directly
                    'student_answer': sol_a.get('reply', ""),  # Get reply directly
                    'rubric': standard_sol_a.get('rubric', "") if standard_sol_a else None,
                    'max_marks': qp_q['max_marks'],
                    'question_number': qp_q['question_number'],
                    'subpart': None  # No subpart for these questions
                })

        return qa_pairs

    except (KeyError, IndexError) as e:
        print(f"Error accessing data: {e}")
        return []
    
def extract_marks_and_reasoning(df, text_column='text'):
    """
    Extracts marks and reasoning from a dataframe containing JSON strings
    enclosed in triple backticks.

    Args:
        df: The input dataframe.
        text_column: The name of the column containing the JSON strings.

    Returns:
        A Pandas DataFrame with 'marks' and 'reasoning' columns.
        Returns the original dataframe if errors occur.
    """
    try:
        err=True
        marks = []
        reasoning = []

        for index, row in df.iterrows():
            text = row[text_column]
            try:
                # Remove backticks and any leading/trailing whitespace
                start = text.find("{")
                end = text.rfind("}")+1
                cleaned_text =text[start:end]

                data = json.loads(cleaned_text)
                marks.append(data.get("marks_awarded"))
                reasoning.append(data.get("reasoning"))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON at index {index}: {e}")
                marks.append(None)
                reasoning.append(None)
                err=False
            except AttributeError as e: # In case text is None/NaN
                print(f"Error processing text at index {index}: {e}")
                marks.append(None)
                reasoning.append(None)
                err=False

        df['marks'] = marks
        df['reasoning'] = reasoning
        return df,err

    except Exception as e:
        print(f"A general error occurred: {e}")
        return df


def persona_qree():
    persona_text = """
    Persona: QRee, the Nuclear Physics Undergraduate TA
    Background:
    - Student-Focused: Qree values understanding and effort, remembering her own student experiences.
    - Deep Knowledge Base: Highly knowledgeable in nuclear physics, with a strong grasp of concepts and calculations.
    - Methodical: Organized and consistent in grading, valuing structure but remaining flexible.
    - Experience: Several semesters of TA experience , understanding common student pitfalls.

    Personality:
    - Approachable: Supportive and encouraging, making students feel comfortable.
    - Patient: Sees mistakes as learning opportunities, not frustrations.
    - Encouraging: Acknowledges strengths as much as addressing weaknesses. 
    - Fair and Liberal: Lenient in grading, focusing on the process and maintaining high standards.

    TA Style:
    - Grading Style: Evaluate the solution based on the provided rubric/own knowledge.
    - Detailed Reasoning: Provides clear reasoning behind awarded marks, explaining what was correct and where points were deducted.
    - Follows 'Instructions for evaluation' or 'Rubric'.
    
    Special Instructions:
    - Keep in mind that this is OCR'd text. You have to carefully think if some text is not clear due to bad parsing.
      the student's marks should not be deducted for that part even if mentioned in rubric.
    - If the issue is not due to bad parsing, you can deduct appropriate marks. 
    """
    return persona_text


def grading_instructions_ocr():
    inst_text="""
    1.Evaluate Student's Answer and return the total marks(marks_awarded) and brief reasoning behind awarded marks. 
    2.TA Will Step by Step Reason the answer of the question and then evaluate the solution. 
    3. For numerical values in Student's Answer, use a range to judge the correctness of answer.
    4. If numerical values look close to original and reasoning of the student is correct
    then even if the final answer looks wrong due to bad parsing, don't deduct marks.
    5. If the Student's Answer is empty string award then award 0
    6. Don't deduct full marks unless the answer is completely unrelated/wrong.
    7. Awarded marks shouldn't exceed maximum marks.
    8. Provide output in Output JSON Template without any commentary
    """
    return inst_text
    
    
