import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()  # loads the .env file

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",                     # or gemini-1.5-pro-latest
    temperature=0.7,
    google_api_key='AIzaSyC0rvwqlA8iWXG-jHASERku-iZxZceKslE'
)

# Example prompt
if __name__=="__main__":
    response = llm.invoke("WHich LLM model you are? are gemma or gemini?")
    print(response.content)
