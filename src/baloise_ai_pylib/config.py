from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# General OpenAI configuration
TEMPERATURE = 0.7
TOP_P = 1.0

# Run configuration
RUN_WAIT_TIME = 5       # time to wait between OpenAI API run update requests
RUN_MAX_RETRIES = 10    # maximum number of retries to get the run status from the OpenAI API

# Parallelization configuration
PARALLEL_REQUEST_LIMIT = 100

# Rate limiting
RATE_LIMIT = 5000  # requests per minute
TOKENS_LIMIT = 2000000  # tokens per minute
