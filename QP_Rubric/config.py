import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Get the main path (where the PDFs and output will be)
#MAIN_PATH = os.getenv("MAIN_PATH", os.path.dirname(os.path.abspath(__file__)))

MAIN_PATH = '3_HW1'
# Define project root directory (where the code and sample schemas are)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Define default paths inside the project root
QP_RUBRIC_DIR = os.path.join(PROJECT_ROOT,'QP_Rubric')

# Sample schemas are inside QP_Rubric directory
SAMPLE_SCHEMA_DIR = QP_RUBRIC_DIR


# Create directories if they don't exist - inside MAIN_PATH where data and output files will reside
DATA_DIR = os.path.join(MAIN_PATH, 'data')
os.makedirs(DATA_DIR, exist_ok=True)


# Define paths for other files
QP_PATH = os.path.join(MAIN_PATH, "QP.pdf") # PDF is in MAIN_PATH now
SAMPLE_QP_SCHEMA_PATH = os.path.join(SAMPLE_SCHEMA_DIR, "sample_schema_QP.txt")
SAMPLE_ANS_SCHEMA_PATH = os.path.join(SAMPLE_SCHEMA_DIR, "sample_schema_ans.txt")
SAMPLE_RUBRIC_SCHEMA_PATH = os.path.join(SAMPLE_SCHEMA_DIR, "sample_schema_rubric.txt")