"""Configuration loader for environment variables."""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the HuggingFace API token
HF_TOKEN = os.getenv("HF_TOKEN")
