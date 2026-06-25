import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import *

#LLM -> later we can create a single class for all models

#main file path
main_path='03/3_HW5'

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-exp')
config = genai.GenerationConfig(
        max_output_tokens=4096, temperature=0.6,
        )

#=====================================================================#
#Extract the Text from QP PDF
#=====================================================================#

prompt="Transcribe this document in markdown and use ascii for equations. Output should be only markdown without any additional commentary."
qp_rubric_path=main_path+'/QP_Rubric'
qp_path=qp_rubric_path+'/QP.pdf'

file_name='QP'
file_path = os.path.join(qp_rubric_path, f"{file_name}.txt")
#if the parsed text is  not there the parse it
if not os.path.exists(file_path):
    
    sample_file = genai.upload_file(path=qp_path, display_name="QPPDF")
    
    # Generate content using the uploaded document
    response = model.generate_content([sample_file, prompt],
                                    generation_config=config
        )
    pdf_text=response.text

    with open(file_path, "w",encoding="utf-8") as f:
        f.write(pdf_text)
else:
    with open(file_path, "r",encoding="utf-8") as f:
        pdf_text=f.read()
     


#=====================================================================#
#Create a JSON of QP_Schema
#=====================================================================#
#read standard qp schema
qp_path_schema='cleaned_code/QP_Rubric/sample_schema_QP.txt'
with open(qp_path_schema, 'r',encoding="utf-8") as f:
        schema_qp = f.read()

prompt_qp_schema=(f"You are given a QP and a schema, Strictly return the whole QP in the given JSON schema."
f"Don't add any new subkeys if not mentioned in QP.If marks are not mentioned in subparts, divide the marks appropriately"
f"#QP:{pdf_text}\n #JSON schema:{schema_qp}")

response = model.generate_content(prompt_qp_schema,
                                  generation_config=config)
schema_qp_text=response.text
file_name='QP_schema'
file_path = os.path.join(qp_rubric_path, f"{file_name}.txt")
file_path_qp = os.path.join(qp_rubric_path, f"{file_name}.json")
with open(file_path, "w",encoding="utf-8") as f:
    f.write(schema_qp_text) 
json_data, error = output_to_json(schema_qp_text)

try:
    with open(file_path_qp,'w',encoding='utf8') as f:
        json.dump(json_data, f, indent=2,ensure_ascii=False)
except Exception as e: # Handle potential file writing errors
        print(f"Error saving JSON Schema QP to file: {e}")

#=====================================================================#
#Create a Standard Answer Schema out of Paper using sample JSON
#=====================================================================#
ans_path_schema='cleaned_code/QP_Rubric/sample_schema_ans.txt'
#with open(ans_path_schema, 'r',encoding="utf-8") as f:
#    schema_ans = f.read()

#prompt_rubric=(f"you are given a QP, convert it to given JSON schema format."
#               f"Strictly fill the reply key with empty strings"
#f"#QP:{pdf_text}\n #JSON schema:{schema_ans}")


#response = model.generate_content(prompt_rubric,
#                                generation_config=config)

response_text = modify_key_and_clear_value(json_data,'max_marks','reply')

file_path = os.path.join(qp_rubric_path, f"{file_name}_answer.txt")

with open(file_path, "w",encoding="utf-8") as f:
    json.dump(response_text, f, indent=2,ensure_ascii=False) 
    
    
#=====================================================================#
#Create a Rubric JSON
#=====================================================================#
rubric_path_schema='cleaned_code/QP_Rubric/sample_schema_rubric.txt'
with open(rubric_path_schema, 'r',encoding="utf-8") as f:
        schema_rubric = f.read()


prompt_rubric=(f"You are a Nuclear Physics Teaching Assistant. Your task is to create a detailed rubric for evaluating the given question paper(QP)."
f"The rubric should holistically assess each question, dividing the points based on the maximum marks(max_marks) allocated for each question. For numerical values, provide a range for the correct answer."
f"Rubric should be Very Lenient while deducting marks to encourage learning and understanding."
f"Add the Rubric in the 'rubric' key in the given JSON schema for each question in QP."
f"Don't create any new key or subkey inside rubric, keep it as a single text for each question"
f"#QP:{schema_qp_text}\n #Rubric schema:{schema_rubric}")

response = model.generate_content(prompt_rubric,
                                  generation_config=config)
schema_qp_text=response.text
file_name='rubric'
file_path = os.path.join(qp_rubric_path, f"{file_name}.txt")
file_path_rub = os.path.join(qp_rubric_path, f"{file_name}.json")
with open(file_path, "w",encoding="utf-8") as f:
    f.write(schema_qp_text) 
json_data, error = output_to_json(schema_qp_text)

try:
    with open(file_path_rub,'w',encoding='utf8') as f:
        json.dump(json_data, f, indent=2,ensure_ascii=False)
except Exception as e: # Handle potential file writing errors
        print(f"Error saving JSON Schema QP to file: {e}")

    