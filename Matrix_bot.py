#import required packages
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os
import json
from langchain_summarizer import *
import pytz
import telegram

model = initialize()
flag1=False
flag2=False
flag3=False
js = {'data':[]}

#Dump messages from Telegram to JSON
def handle_messages(update, context):
    message = update.message
    ##get chat_id of the telegram group
    if message.chat_id == -1001830288540:
        chat_user = message.from_user.full_name
        text = message.text
        data = str('[' + message.date.astimezone(pytz.timezone('Asia/Kolkata')).strftime("%m-%d-%Y %H:%M:%S") + ']').rstrip("'")+' '+chat_user+' : '+text
        js['data'].append(data)
        print(data)

#Call LLM Model API to summarize the conversation
def handle_summarize(update, context):
    message = update.message
    data = js['data']
    if len(data)>=1:
        if len(data)>100:
            data = data[:-100]
    if message.chat_id == 2017185171:
            global suhas_history_model
            global flag1
            prompt = ' summarize the conversation'
            if len(context.args) >=1:
                prompt = ' '.join(context.args).lower()
                if prompt == 'end':
                    flag1 = False  
                if flag1:
                    conversation = None
                    response =summarize_model(prompt, conversation,suhas_history_model)
                    try:    
                        update.effective_chat.send_message(text=response)
                    except telegram.error.BadRequest:
                        update.effective_chat.send_message(text ='Could not fetch response from model, please try again'.upper())
                if prompt == 'hey matrix':
                    suhas_history_model = summarize_memory_initialize(model)
                    update.effective_chat.send_message(text ='summarizing the converation')
                    prompt = ' summarize the following set of  conversation'
                    conversation = ' \n '.join(data)
                    response =summarize_model(prompt, conversation,suhas_history_model)
                    update.effective_chat.send_message(text =response)
                    update.effective_chat.send_message(text ='Hi, how can i help you?')
                    flag1 =True 
                if flag1 ==False: 
                    update.effective_chat.send_message(text='Initialize the conversation using "/LLM hey matrix" command, Thank you') 
            else:
                update.effective_chat.send_message(text='enter a prompt with command')
    if message.chat_id == 5893878772:
        global sai_history_model
        global flag2
        prompt = ' summarize the conversation'
        if len(context.args) >=1:
            prompt = ' '.join(context.args).lower()
            if prompt == 'end':
                flag2 = False
            if flag2:
                conversation = None
                response =summarize_model(prompt, conversation,sai_history_model)
                try:    
                    update.effective_chat.send_message(text=response)
                    update.effective_chat.send_message(text ='what else can i help you with?')
                except telegram.error.BadRequest:
                    update.effective_chat.send_message(text ='Could not fetch response from model, please try again'.upper())
            if prompt == 'hey matrix':
                sai_history_model = summarize_memory_initialize(model)
                update.effective_chat.send_message(text ='summarizing the converation')
                prompt = ' summarize the following set of conversation'
                conversation = ' \n '.join(data)
                response =summarize_model(prompt, conversation,sai_history_model)
                update.effective_chat.send_message(text =response)
                update.effective_chat.send_message(text ='Hi, how can i help you?')
                flag2 =True
            if flag2 ==False:  
                update.effective_chat.send_message(text='Initialize the conversation using "/LLM hey matrix" command, Thank you')
            
        else:
            update.effective_chat.send_message(text='enter a prompt with command')
    if message.chat_id == 685113742:
        global flag3
        global mythili_history_model
        prompt = ' summarize the conversation'
        if len(context.args) >=1:
            prompt = ' '.join(context.args).lower()
            
            if prompt == 'end':
                flag3 = False 
            
            if flag3:
                conversation = None
                response =summarize_model(prompt, conversation,mythili_history_model)
                try:    
                    update.effective_chat.send_message(text=response)
                    update.effective_chat.send_message(text ='what else can i help you with?')
                except telegram.error.BadRequest:
                    update.effective_chat.send_message(text ='Could not fetch response from model, please try again'.upper())
                
            if prompt == 'hey matrix':
                mythili_history_model = summarize_memory_initialize(model)  
                update.effective_chat.send_message(text ='summarizing the converation')
                prompt = ' summarize the following set of conversation'
                conversation = ' \n '.join(data)
                response =summarize_model(prompt, conversation,mythili_history_model)
                update.effective_chat.send_message(text =response)
                update.effective_chat.send_message(text ='Hi, how can i help you?')
                flag3 =True
            if flag3 ==False: 
                update.effective_chat.send_message(text='Initialize the conversation using "/LLM hey matrix" command, Thank you') 
        else:
            update.effective_chat.send_message(text='enter a prompt with command')
              

# Take Token of telegram group chat and create the updater object
TOKEN = 'Your token'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Create a message handler and register it with the dispatcher
message_handler = MessageHandler(Filters.all, handle_messages)
dispatcher.add_handler(CommandHandler('LLM',handle_summarize))
dispatcher.add_handler(message_handler)
updater.start_polling()
updater.idle()