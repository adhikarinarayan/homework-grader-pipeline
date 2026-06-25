#convert llm generated json to standard format json

import json
import os

def fill_descriptions(standard_json, llm_json):
    """
    Fills descriptions, handling extra fields and adding them to 'unclassified'.
    """

    standard = standard_json
    llm = llm_json
    extra_data = [] # List to hold the extra fields

    for i, std_answer in enumerate(standard['answers']):
        try:
            llm_answer = llm['answers'][i]
            std_answer['reply'] = llm_answer.get('reply', '')

            std_subparts = std_answer.get('subparts', [])
            llm_subparts = llm_answer.get('subparts', [])

            for j, std_subpart in enumerate(std_subparts):
                try:
                    std_subpart['reply'] = llm_subparts[j].get('reply', '')
                except IndexError:  # std has more subparts than llm
                    pass

            # Handle extra subparts
            for k in range(len(std_subparts), len(llm_subparts)):
                extra_subpart = llm_subparts[k]
                extra_data.append({
                    "answer_number": i + 1,
                    "subpart": extra_subpart.get("subpart", "unknown"),
                    "answer": extra_subpart.get("answer", "")
                })


        except IndexError:  # std has more answers than llm
            pass

    # Handle extra answers
    for m in range(len(standard['answers']), len(llm['answers'])):
        extra_answer = llm["answers"][m]
        extra_data.append(extra_answer) # Append the entire extra answer


    standard["unclassified"] = {
        "original": llm.get("unclassified", ""),  # Preserve original unclassified content
        "extra_fields": extra_data  # Add the list of extra fields
    }


    return standard


#Directory of parsed HW 
json_path="compare_json_mistral/mistral_2step/json"
files= os.listdir(json_path)
#patht to save json
standard_json_path = "compare_json_mistral/mistral_2step/standard_json"
for file in files:
    filepath = json_path+'/'+file
    try:
        with open("qp_sol/standard_qp.json", 'r',encoding='utf-8') as f:
            standard_json_data = json.load(f)

        with open(filepath, 'r',encoding='utf-8') as f:
            llm_json_data = json.load(f)

        filled_json = fill_descriptions(standard_json_data, llm_json_data)
        file_name,_=os.path.splitext(file)
        json_file_path=os.path.join(standard_json_path, f"{file_name}.json")
        with open(json_file_path, 'w',encoding='utf-8') as f:
            json.dump(filled_json, f, indent=4,ensure_ascii=False)
        print('success')

    except FileNotFoundError:
        print("Error: One or both JSON files not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in one of the files.")