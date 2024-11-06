import json

def load_config():
    """Load configuration from JSON file"""
    with open('screening_config.json', 'r') as f:
        return json.load(f)

def get_ai_model_name(model_to_use):
    """Convert frontend model names to ask_ai model names"""
    model_mapping = {
        'azure-gpt-4-turbo': 'gemini',  # Default to gemini since Azure isn't in new ask_ai
        'mixtral-8x7b-32768': 'mixtral',
        'llama2-70b-4096': 'llama3',
        'claude': 'claude'
    }
    return model_mapping.get(model_to_use, 'gemini')
