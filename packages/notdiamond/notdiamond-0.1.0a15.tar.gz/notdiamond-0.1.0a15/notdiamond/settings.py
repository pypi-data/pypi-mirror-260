import os

from dotenv import load_dotenv
load_dotenv(os.getcwd() + '/.env')

NOTDIAMOND_API_KEY = os.getenv('NOTDIAMOND_API_KEY', default='')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', default='')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', default='')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', default='')

ND_BASE_URL = "https://not-diamond-server.onrender.com"

PROVIDERS = {
    'openai': {
        'models': ['gpt-3.5-turbo', 'gpt-4'],
        'api_key': OPENAI_API_KEY
    },
    'anthropic': {
        'models': ['claude-2.1'],
        'api_key': ANTHROPIC_API_KEY
    },
    'google': {
        'models': ['gemini-pro'],
        'api_key': GOOGLE_API_KEY
    }
}
