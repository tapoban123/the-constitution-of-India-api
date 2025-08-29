from fastapi import FastAPI, Body
from typing import Annotated

from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI

from utils.pinecone_db_mng import PineconeManager
from utils.constants import MISTRAL_AI

app = FastAPI()
pinecone_mgr = PineconeManager(index_name="indian-constitution")


def get_llm() -> ChatMistralAI:
    llm = ChatMistralAI(
        api_key=MISTRAL_AI.API_KEY.value,
        model_name="mistral-large-latest",
        temperature=0,
    )
    return llm


def get_prompt():
    return PromptTemplate(
        template="""
Given the CONTEXT and the QUERY below:

- Answer only using information from the provided CONTEXT.  
- Do NOT add any information that is not explicitly present in the CONTEXT.  
- Summarize and present the information in direct response to the QUERY.  
- Use simple language and clear explanations to make your response easy to understand for anyone, regardless of their background.

CONTEXT: {context}
QUERY: {query}

YOUR TASK:  
Write a summary or answer to the QUERY, using only relevant facts and details from the CONTEXT.
Do NOT use any external knowledge or make assumptions.  
Keep the answer very simple, clear, and easy to read.
""",
        input_variables=["context", "query"],
    )


class QueryModel(BaseModel):
    query: str


class ContentOutputModel(BaseModel):
    answer: str
    page_nos: list[int]


@app.get("/")
def home():
    return "Welcome to Indian Constitution API."


@app.get("/content", response_model=ContentOutputModel)
def get_content(query: QueryModel):
    context, page_nos = pinecone_mgr.perform_similarity_search(query=query.query)
    llm = get_llm()
    prompt = get_prompt()
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    result = chain.invoke({"context": context, "query": query.query})
    return ContentOutputModel(answer=result, page_nos=page_nos)
