import json
import pandas as pd
import os
import time
from utils import *


#main path
main_path='03/3_HW5'

qp_path=main_path+'/QP_Rubric/QP_schema.json'
rubric_path= main_path+'/QP_Rubric/rubric.json'


#load qp
with open(qp_path, 'r',encoding='utf-8') as f:
    qp_data = json.load(f)
    
#load rubric
with open(rubric_path, 'r',encoding='utf-8') as f:
    standard_sol_data = json.load(f)


#files
input_json=main_path+'/JSON'
files=os.listdir(input_json)
#save results
res_out=main_path+'/Grades'

if not os.path.exists(res_out):
    os.makedirs(res_out)

#Grading Instructions
instructions=grading_instructions_ocr()
# Grader Persona - QRee, Nuclear Physics TA
persona=persona_qree()


# WITH RUBRIC: PERSONA+RUBRIC, WITHOUT RUBRIC:PERSONA + GRADING INSTRUCTIONS
def evaluator_function(row,persona,instructions):
    """
    Evaluator function that takes a DataFrame row as input.
    '#Rubric':
    {}
    
    """
    question = row['question']
    answer = row['student_answer']
    max_marks = row['max_marks']
    standard_ans = row['rubric'] if row.get('rubric') else ""

    prompt=f"""You are -{persona}\n
    #Instructions for evaluation:
    {instructions}
{{
'#Question':
{question}
,
'#Student's Answer':
{answer}
,
'#Maximum Marks':
{max_marks}
,
'#Rubric':
{standard_ans}
}}

## Output Format:

```json
{{
  "marks_awarded": marks,
  "reasoning": reasoning behind grading
}}
```

"""
    time.sleep(2)
    #return call_gemini(prompt)
    return call_mistral(prompt)

marks_data=[]
for file in files:
    
    err=False
    filename=input_json+'/'+file
    with open(filename, 'r',encoding='utf-8') as f:
        sol_data = json.load(f)
    print(filename)
    qa_pairs = extract_qa_pairs(qp_data, sol_data,standard_sol_data)
    df_qa =pd.DataFrame(qa_pairs)
    while err==False:
        df_marks = pd.DataFrame(qa_pairs).apply(lambda row: evaluator_function(row,persona,instructions), axis=1)
        dff,err = extract_marks_and_reasoning(pd.DataFrame(pd.DataFrame(df_marks,columns=['text'])))
    df_qa[['marks','reasoning']] = dff[['marks','reasoning']]
    _,x=os.path.split(filename)
    save_path=res_out+'/'+x[:-5]+'.csv'
    df_qa.to_csv(save_path, index=False,encoding='utf-8')
    marks=dff['marks'].sum()
    marks_data.append({"filename": file, "marks": marks})
    print(f'Grading of {file} complete, marks- {marks}')

df_all_marks = pd.DataFrame(marks_data)
df_all_marks.to_csv(res_out+'/total_marks.csv', index=False, encoding='utf-8')