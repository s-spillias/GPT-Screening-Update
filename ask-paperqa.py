from paperqa import Settings, ask, Docs
import os
from litellm import embedding

def get_all_file_paths(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return tuple(file_paths)

# Set Azure OpenAI environment variables for ModelBot
os.environ['AZURE_API_KEY'] = os.getenv('MODELBOT_AZURE_OPENAI_KEY')
os.environ['AZURE_API_BASE'] = os.getenv('MODELBOT_AZURE_OPENAI_ENDPOINT')
os.environ['AZURE_API_VERSION'] = os.getenv('MODELBOT_AZURE_OPENAI_VERSION')

# Configure Azure OpenAI for LLM (using ModelBot-gpt4)
azure_llm_config = dict(
    model_name="azure/ModelBot-gpt4",
    litellm_params=dict(
        model="azure/ModelBot-gpt4",
        api_base=os.environ['AZURE_API_BASE'],
        api_key=os.environ['AZURE_API_KEY'],
        api_version=os.environ['AZURE_API_VERSION'],
        temperature=0.1,
        max_tokens=512,
    )
)

# Configure Azure OpenAI for embeddings (using ModelBot-Embedding)
azure_embedding_config = {
    # "model": "azure/ModelBot-Embedding",
    # "api_deployment": os.getenv('MODELBOT_AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT'),
    "api_base": os.environ['AZURE_API_BASE'],
    "api_key": os.environ['AZURE_API_KEY'],
    "api_version": os.environ['AZURE_API_VERSION'],
}

directory_path = 'Social_accounting/all_pdfs'
all_files = get_all_file_paths(directory_path)

# Initialize settings
settings = Settings(
    llm="azure/ModelBot-gpt4",
    llm_config={"model_list": [azure_llm_config]},
    embedding="azure/ModelBot-Embedding",
    embedding_config=azure_embedding_config
)

# Create Docs object and add documents
docs = Docs()
for doc in all_files:
    docs.add(doc, settings=settings)

# Query the documents
answer = docs.query(
    "What manufacturing challenges are unique to bispecific antibodies?",
    settings=settings,
)

print(answer.formatted_answer)