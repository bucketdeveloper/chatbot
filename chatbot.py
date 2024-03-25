import streamlit as st
import boto3
import json

region = boto3.Session().region_name
session = boto3.Session(region_name=region)
lambda_client = session.client('lambda')

st.set_page_config(page_title="WellArchitectedBot for AnyCompany")

st.title("WellArchitectedBot for AnyCompany")

with st.sidebar:
    st.title('WellArchitectedBot')
    st.divider()
    st.markdown('You can ask WAB questions about the AWS WellArchitected Framework, to help guide your decisions when choosing new technologies.\n')

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

sessionId = ""
#sessionId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
print(sessionId)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

sessionId = ""
#sessionId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
print(sessionId)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session id
if 'sessionId' not in st.session_state:
    st.session_state['sessionId'] = sessionId

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What can Well Architected Bot do for you today?"):

    # Display user input in chat message container
    question = prompt
    st.chat_message("user").markdown(question)

    # Call lambda function to get response from the model
    payload = json.dumps({"question":prompt,"sessionId": st.session_state['sessionId']})
    print(payload)
    result = lambda_client.invoke(
                FunctionName='InvokeKnowledgeBase',
                Payload=payload
            )

    result = json.loads(result['Payload'].read().decode("utf-8"))
    print(result)

    citationBlurb = ""

    answer = result['body']['answer'].replace("$","\$")
    sessionId = result['body']['sessionId']
    citation_text = result['body']['citationText']
    citation_src = result['body']['citationSrc']
    st.session_state['sessionId'] = sessionId
    citationBlurb = citation_text + "\n\n*Source*: " + citation_src
    citationBlurb = citationBlurb.replace("$","\\$")

    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": question})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer, help=citationBlurb)
        # st.markdown(answer)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})