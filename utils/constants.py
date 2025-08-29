from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()


class PINECONE(Enum):
    API_KEY = os.environ.get("PINECONE_API_KEY")


# class GOOGLE_GENAI(Enum):
#     API_KEY = os.environ.get("GEMINI_API_KEY")
#     EMBEDDING_MODEL = "models/gemini-embedding-001"


class MISTRAL_AI(Enum):
    API_KEY = os.environ.get("MISTRAL_API_KEY")
    EMBEDDING_MODEL = "mistral-embed"
