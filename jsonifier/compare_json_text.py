import pandas as pd
import json
import os
import textdistance

## Script to compare the JSONIFIED Answer sheet and the parsed answer sheet
def extract_descriptions(json_filepath):
    """
    Extracts all descriptions from a JSON file, including question descriptions and subparts.

    Args:
        json_filepath: Path to the JSON file.

    Returns:
        A string containing all descriptions, or an empty string on error.
    """
    try:
        with open(json_filepath, 'r',encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return ""

    all_descriptions = ""

    for question in data.get("questions", []):
        if "reply" in question:  # Check for a main description
            all_descriptions += question["reply"] + "\n\n" # Extra newline for clarity

        if "subparts" in question:  # Check for subparts (regardless of main desc.)
            for subpart in question["subparts"]:
                all_descriptions += subpart["reply"] + "\n"  
            all_descriptions += "\n" # Extra newline between questions/subparts

    if "unclassified" in data:
        all_descriptions += data["unclassified"] + "\n"

    return all_descriptions.strip()



if __name__=='__main__':
     json_path = "5_HW1/JSON"
     text_path = "5_HW1/Parsed"
     file_list= sorted(os.listdir(json_path))
     results=[]
     file_l = []

     for file in file_list:
          path=json_path +'/'+ file
          try:
               extracted_text_json = extract_descriptions(path)
               path_t = text_path+'/'+os.path.splitext(file)[0]+'.txt'
          
               with open(path_t,'r',encoding='utf-8') as f:
                    extracted_text= f.read()
               print(path)
               jaccard=textdistance.jaccard.similarity(extracted_text,extracted_text_json)
               print(jaccard)
               results.append(jaccard)
               file_l.append(file)
          except:
               results.append(0)
               file_l.append(file)



 
#text_path=compare_json_mistral\text
#results=pd.DataFrame(list(zip(file_l,results)),columns=['filename','jaccard_index'])
#results.to_csv("compare_json_mistral/mistral_2step/results.csv",index='False')
