import os
from utils import *
import pandas as pd
from prompts import *
from models import *
import json
import time
#Directory of parsed HW 
main_path='03/3_HW5'
hw_path=main_path+"/Parsed"
files= os.listdir(hw_path)

#path to save json object
hw_json =main_path+ "/JSON"

#temporary -> path to save segregated text
hw_json_seg= main_path+ "/JSON_Seg"
#path to save json as text
hw_json_text= main_path+ "/JSON_Text"


# Check if these directories exists, and create it if it doesn't.
if not os.path.exists(hw_json_text):
    os.makedirs(hw_json_text)

if not os.path.exists(hw_json_seg):
    os.makedirs(hw_json_seg)
    
if not os.path.exists(hw_json):
    os.makedirs(hw_json)


#prompt for segregation of solutions based on the Question paper
qp_path=main_path + "/QP_Rubric/QP.txt"
with open(qp_path, 'r',encoding="utf-8") as f:
        qp = f.read()
prompt_seg=prompt_segregation(qp)
        

#prompt to create a standard json out of these segregated Solutions
qp_path=main_path + "/QP_Rubric/QP_schema_answer.txt"
with open(qp_path, 'r',encoding="utf-8") as f:
        schema = f.read()
prompt_json= prompt_schema(schema)

results=[]
#Main loop
for file in files:
    filepath = hw_path+'/'+file
    
    #read parsed files
    with open(filepath, 'r',encoding="utf-8") as f:
        data = f.read()
        
    #1.segregation
    input = prompt_seg + data
    response_seg = call_mistral(input)
    
    #2.to json
    final_input=prompt_json+response_seg
    error='x'
    count=0
    temp=0.6
    while error!=None:
        response=call_mistral(final_input, temperature=temp)
        file_name,_=os.path.splitext(file)

        #save json as text
        file_path = os.path.join(hw_json_text, f"{file_name}.txt")
        with open(file_path, "w",encoding="utf-8") as f:
            f.write(response)

        #save as json object
        json_data, error = output_to_json(response)
        json_file_path=os.path.join(hw_json, f"{file_name}.json")

        # Jaccard check: verify parsed content is preserved in the JSON
        if error is None:
            extracted = extract_replies(json_data)
            similarity = jaccard_similarity(data, extracted)
            if similarity < 0.5:
                error = f"Low Jaccard similarity ({similarity:.2f}); retrying."

        count+=1
        if count==4:
            break
        if error is not None:
            temp = min(0.6 + count * 0.05, 0.9)
    #save segregated text
    seg_file_path=os.path.join(hw_json_seg, f"{file_name}.txt")
    with open(seg_file_path, "w",encoding="utf-8") as f:
        f.write(response_seg)
    
    try:
        with open(json_file_path, 'w',encoding='utf8') as f:
            json.dump(json_data, f, indent=2,ensure_ascii=False)
    except Exception as e: # Handle potential file writing errors
            print(f"Error saving JSON to file: {e}")
            
print("parsing complete")

