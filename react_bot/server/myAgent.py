import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]

from langchain.tools import tool
#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
#from langchain.tools.render import format_tool_to_openai_function
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.schema.agent import AgentFinish
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory

import requests
import datetime
from pydantic import BaseModel, Field
import requests

class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    # Make the request
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")

    current_utc_time = datetime.datetime.utcnow()
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']
    
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]
    
    return f'The current temperature is {current_temperature}°C'


import wikipedia

@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)


# @tool
# def create_your_own(query: str) -> str:
#     """This function can do whatever you would like once you fill it in """
#     print(type(query))
#     return query[::-1]

class PersonalityTestInput(BaseModel):
    start_test: bool = Field(..., description="A flag to start the personality test.")

@tool(args_schema=PersonalityTestInput)
def personality_test(start_test: bool) -> str:
    """Conduct a personality test by asking predefined questions."""
    if not start_test:
        return "Personality test was not started."

    # Predefined personality test questions
    questions = [
        "Q1: On a scale of 1-10, how do you rate your openness to new experiences?",
        "Q2: On a scale of 1-10, how conscientious are you in your daily life?",
        "Q3: On a scale of 1-10, how extraverted do you consider yourself?",
        "Q4: On a scale of 1-10, how agreeable are you when interacting with others?",
        "Q5: On a scale of 1-10, how often do you experience feelings of anxiety or moodiness?"
    ]

    answers = {}
    for question in questions:
        #answer = input(f"{question}: ")
        url = "http://localhost:8000/chatbot/"
        data = {"message": question}
        answer = requests.post(url, json=data).json()["response"]
        print(answer)
        answers[question] = answer

    return f"Personality test completed. Your responses: {answers}"



#tools = [get_current_temperature, search_wikipedia]
tools = [get_current_temperature, search_wikipedia, personality_test]

def run_agent(query):
    #functions = [format_tool_to_openai_function(i) for i in tools]
    functions = [convert_to_openai_function(i) for i in tools]
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).bind(functions=functions)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you are golden retriever who can talk to humans"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    chain = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"]),
    ) | prompt | model | OpenAIFunctionsAgentOutputParser()
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    agent_executor = AgentExecutor(agent=chain, tools=tools, verbose=True, memory=memory)
    result = agent_executor.invoke({"input":query})

    return result

