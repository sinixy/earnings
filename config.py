from os import getenv
from dotenv import load_dotenv
import json

load_dotenv()

OPENAI_API_KEY = getenv('OPENAI_API_KEY')
EDGAR_IDENTITY = getenv('EDGAR_IDENTITY')
RECEIVER_ID = getenv('RECEIVER_ID')
BOT_TOKEN = getenv('BOT_TOKEN')
FILINGS_WS = getenv('FILINGS_WS')

with open('prompts.json') as file:
    PROMPTS = json.load(file)