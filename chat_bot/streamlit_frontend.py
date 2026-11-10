import streamlit as st

from langraph_backend import chatbot

from langchain_core.messages import AIMessage, HumanMessage
import uuid

##################### utility functions

def generate_thread_id():
    ## universally unique identifirt 
    thread_id = uuid.uuid4()
    return str(thread_id)

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []
    


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config = {'configurable': {'thread_id': thread_id}})
    messages = state.values.get('messages', [] )
    return messages


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []





# {'role' :'user', 'content':'Hello'}
# {'role':'assistant', 'content':'Hi!'}

## if chat threads not in session state
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []        

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

add_thread(st.session_state['thread_id'])


## ****************************************************** SIDE BAR UI
st.sidebar.title("FakeGPT")

## on clicking it new chat create and session have new thread id and clear history
if st.sidebar.button("New Chat"):
    reset_chat()


st.sidebar.header("Recents")

## if we click the side bar button, switch thread and storing all the messages to that thread
## using langgraph get_state to get messages for thread
## and assign them with role and store in history
for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread):
        st.session_state['thread_id'] = thread
        messages = load_conversation(thread)

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                temp_messages.append({'role':'user', 'content':message.content})
            else:
                temp_messages.append({'role':'assistant', 'content':message.content})

        ## now update history
        st.session_state['message_history'] = temp_messages

# st.sidebar.write(st.session_state['thread_id'])


############################# MAIN UI
# loading the conversation history and display it
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
user_input = st.chat_input("Type Here")

if user_input:

    # first add the message to history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.write(user_input)

    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config =  CONFIG)

    # ai_response = response['messages'][-1].content

    # ## first add AI response to history
    # st.session_state['message_history'].append({'role':'assistant', 'content':ai_response})

    ## adding streaming functionality here so messages write in stream
    with st.chat_message('assistant'):

        ## going to call function that streams response
        ## st.write_stream() is streamlit functionality
        ## chatbot.stream() is langgraph functionality
        ## printing messages in streams and saving them
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                  {'messages': [HumanMessage(content=user_input)]},
                    config =  CONFIG,
                    stream_mode = 'messages'):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(
            ai_only_stream()
        )
    ## storing in session state
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})