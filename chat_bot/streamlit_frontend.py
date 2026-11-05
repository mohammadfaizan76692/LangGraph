import streamlit as st

from langraph_backend import chatbot

from langchain_core.messages import HumanMessage

CONFIG  = {'configurable': {'thread_id':'thead-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# loading the conversation history and display it

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.write(message['content'])

# {'role' :'user', 'content':'Hello'}
# {'role':'assistant', 'content':'Hi!'}


user_input = st.chat_input("Type Here")

if user_input:

    # first add the message to history
    st.session_state['message_history'].append({'role':'user', 'content':user_input})
    with st.chat_message('user'):
        st.write(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config =  CONFIG)

    ai_response = response['messages'][-1].content

    ## first add AI response to history
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_response})
    with st.chat_message('assistant'):
        st.write(ai_response)