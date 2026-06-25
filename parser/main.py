## PDFs should be inside - main_path/Ungraded_Cleaned


import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import remove_gemini_cache

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-exp')


#Prompt for parsing
prompt="TASK - Transcribe this physics document. Output- ```Transcribed document``` "

#Directory of HW PDFs
main_path="03/3_HW1"
hw_path= main_path+'/Ungraded_Cleaned'
files= os.listdir(hw_path)


#save responses as txt file
hw_parsed_path = main_path+'/Parsed'

# Check if the "cleaned" directory exists, and create it if it doesn't
if not os.path.exists(hw_parsed_path):
    os.makedirs(hw_parsed_path)

for file in files:
    path = hw_path+'/'+file
    try:
        sample_file = genai.upload_file(path=path, display_name=f"{file}")
    except:
        print(file)
        continue
    # Generation Config
    config = genai.GenerationConfig(
    max_output_tokens=5120, temperature=0.6,
    )
    # Generate content using the uploaded document
    response = model.generate_content([sample_file, prompt],
                                  generation_config=config
    )
    file_name,_=os.path.splitext(file)
    file_path = os.path.join(hw_parsed_path, f"{file_name}.txt")
    with open(file_path, "w",encoding="utf-8") as f:
        f.write(response.text) 
    


#delete the file in gemini cache

remove_gemini_cache()
        
print("parsing complete")

    