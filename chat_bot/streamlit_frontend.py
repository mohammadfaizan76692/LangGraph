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
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in
              chatbot.stream(
                  {'messages': [HumanMessage(content=user_input)]},
                    config =  CONFIG,
                    stream_mode = 'messages')

        )
    ## storing in session state
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})