import os
from pathlib import Path
from dotenv import load_dotenv
from services.test_list import TestList
from services.test_runner import TestRunner

API_KEY = 'AZURE_OPENAI_API_KEY'
ENDPOINT = 'AZURE_OPENAI_ENDPOINT'

# Configure Environment Variables
load_dotenv()
os.environ[API_KEY] = os.getenv(API_KEY)
os.environ[ENDPOINT] = os.getenv(ENDPOINT)
deployment = os.getenv('AZURE_OPEN_AI_DEPLOYMENT')
version = os.getenv('AZURE_OPEN_AI_API_VERSION')
prompt = os.getenv('SYSTEM_PROMPT')

# Get executing script's directory
script_path = Path(__file__).resolve()
script_dir = script_path.parent

# Creat a test list
test_list = TestList()

# Add tests
test_list.add_test(
    "first_example_test",
    "exact_match",
    f"{script_dir}/csvs/test.csv"
)

# Create runner
test_runner = TestRunner(
    azure_deployment=deployment,
    openai_api_version=version,
    system_prompt=prompt,
)

# Run Tests
test_runner.run_tests(test_list)
