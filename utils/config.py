
from dotenv import load_dotenv
import os

load_dotenv()

def get_config():
    return {
        "api_key": os.getenv("AZURE_API_KEY"),
        "api_base": os.getenv("AZURE_API_BASE"),
        "api_version": os.getenv("AZURE_API_VERSION"),
        "deployment": os.getenv("AZURE_DEPLOYMENT_NAME")
    }
