# Introduction
This is legal advisor chatboat which gives the legal advice based upon input prompt.
It is build on top of langchain, laggraph, streamlit and geminis "models/gemma-3-12b-it" model.

# Features
- Classifies legal issues (e.g., Property, Family, Contract, etc.)
- Provides short, guided legal suggestions.
- Saves full session logs in JSON format.

##  Project Setup and Structure

### Step 1: Cloning the repository
git clone https://github.com/swapnildata/Legal_chatbot.git

### Step 2: Creating a virtual environment
python -m venv legal_chatboat
source legal_chatboat/bin/activate  # On Linux/macOS
legal_chatboat\Scripts\activate     # On Windows

### Step 3: Install the dependencies from requirements.txt
pip install -r requirements.txt

### Step 4: Generating and passing the Gemini_API_key in .env file.
1. Go to the link https://aistudio.google.com/apikey and generate the API key.
2. Pass that API key as environment variable in .env file.

### Step 5: Configuring the app.
1. Add/remove legal categories as per requirement in params.yaml file in config folder.
2. Alter the LLM parameters in constants __init__.py file as per requirement.

### Step 6: Running the app.
python app.py

##  Architecture and Components
This project is a legal chatbot built using LangChain, LangGraph, Gemini Pro, and Streamlit, designed to classify user legal queries, provide legal advice, and track conversation summaries. 

### 1.Frontend:
Streamlit collects the username, prompt and returns legal advice, legal category with chat history. Button is provided to end the session and save the summary. 

### 2.Langchain Configuration:
With usage of ChatGoogleGenerativeAI from langchain LLM is configured through parameters from constants __init__py.

### 3.Langgraph Workflow:
A langgraph consists of following nodes:

1. Classify: Classifies user issue into legal categories.
2. Guide: Generates a legal response based on classification and query.
3. End: Terminates the graph.

State Definition (LegalBotState):
1. messages: Full list of user + AI messages.
2. category: Legal classification result.
3. response: Final legal advice generated.
4. timestamp: Datetime when the query was processed.

### 4.Chat Logging
All the conversation is being logged in artifacts folder in json format. For each day a new file will be created with its date. As soon as user press the end session button, all the summary, input, response, category, timestamp will get stored in the file.

### 5.Flow Summary:
1. User submits a query via Streamlit UI.
2. Query is added to LangChain memory.
3. Messages are passed into the LangGraph pipeline.
4. Issue is classified and a response is generated.
5. Response is stored, displayed, and can be summarized upon session end.

##  Testing Example for reference:
[
    {
        "user_name": "swapnil",
        "datetime": "2025-05-19 00:26:46.933793",
        "messages": [
            {
                "user_input": "Someone stollen my wallet during travel in metro.",
                "response": "Okay, here's some legal advice regarding your stolen wallet, focusing on immediate steps and potential actions:\n\n1. **File a Police Report Immediately:** This is crucial for insurance claims and potential investigation.  Most metro systems have police presence or designated reporting areas.\n2. **Cancel Credit/Debit Cards:** Contact your banks immediately to prevent fraudulent charges. Keep records of cancellation confirmations.\n3. **Replace Identification:**  Report lost IDs (driver's license, passport) and begin the replacement process.\n4. **Consider Travel Insurance:** If you have travel insurance, review your policy for theft coverage.\n5. **Relevant Links:**  [India's National Cyber Crime Reporting Portal](https://cybercrime.gov.in/) (for reporting) & your local police department's website for reporting procedures.\n\n\n\n**Disclaimer:** *I am an AI chatbot and cannot provide legal advice. This information is for general guidance only. Consult with a lawyer for advice specific to your situation.*",
                "category": "Criminal",
                "timestamp": "2025-05-19 00:26:29.866446"
            }
        ],
        "summary": "Here's a summary of the chatbot conversation:\n\nThe user reported their wallet was stolen during metro travel, expressing concern about financial loss and identity theft. The conversation falls under **theft/larceny** and potentially **identity theft** legal categories. The chatbot advised the user to prioritize immediate actions: filing a police report, canceling credit/debit cards, and replacing lost identification. It also suggested reviewing travel insurance policies for coverage.  The bot provided links to the National Cyber Crime Reporting Portal and the local police department. Crucially, the chatbot emphasized it's providing general guidance and not legal advice, urging consultation with a lawyer."
    }
]

