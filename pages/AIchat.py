#from nt import environ
import streamlit as st
import openai, os, requests
import base64
# from dotenv import load_dotenv
# load_dotenv()

st.subheader("AI Chat Support")

openai.api_type = "azure"
# openai.api_version = "2024-02-15-preview"
openai.api_version = "2024-05-01-preview"
# api_key = os.getenv("api_key")
# azapi_key = os.getenv("azapi_key")

openai.api_base = "https://headstarterproj3.openai.azure.com/"
endpoint_id = "https://headstarter-new.openai.azure.com/"
# openai.api_key = INSERT API KEY
# azapi_key= INSERT API KEY

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", "content": "I'm the Project3 Bot!"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = """Your name is Project3 bot. You only respond to customer support questions related to pc troubleshooting and hardware. Anything else you must deny answering.

"""

client = openai.AzureOpenAI(
    azure_endpoint = endpoint_id,
    api_key = azapi_key,
    # api_version = "2024-02-15-preview"
    api_version = "2024-05-01-preview"
    )

user_prompt = st.chat_input()
finalprompt=[{"role": "user", "content": f"{user_prompt}"}]

if user_prompt is not None:
    st.session_state.messages.append(
        {"role": "user", "content": f"{user_prompt}"}
    )
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    completion = client.chat.completions.create(
        model="gpt-4o",
        # model="gpt-4o-mini",
        temperature=0.7,
        top_p=0.95,
        max_tokens = 80,
        stream=False,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": finalprompt}
        ]
    )

    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            st.write(completion.choices[0].message.content)

    new_message = {"role": "assistant", "content": completion.choices[0].message.content}
    st.session_state.messages.append(new_message)