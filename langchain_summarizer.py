from langchain import OpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory 

def initialize():
    ## OpenAI API key
    OPENAI_API_KEY = "your api key"

    ## Initialize the OpenAI model using API key
    chat = OpenAI(temperature=0, openai_api_key = OPENAI_API_KEY)
    return chat



def summarize_memory_initialize(model):

    conversation_with_summary = ConversationChain(
        llm=model, 
        memory=ConversationSummaryMemory(llm=model),
        verbose=False
    )
    return conversation_with_summary

def summarize_model(user_q,conv,history): 
    if conv == None:
        prompt = user_q
    else:
        prompt = user_q+' \n '+ conv
    response = history.predict(input=prompt)
    return response


