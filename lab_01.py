
import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get "
    "from your OpenAI account."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    try:
        client = OpenAI(api_key=openai_api_key)
        _ = client.models.list()  # lightweight validation call
        st.success("API key validated. You can upload a file and ask a question.")
    except Exception as e:
        st.error("Invalid API key or network issue. Please check your key and try again.")
        st.caption(f"Details: {e}")
        st.stop()  # stop the app here if validation fails

    # ---- If validation passed, show the rest of the UI ----
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # Process the uploaded file and question.
        document = uploaded_file.read().decode(errors="ignore")
        messages = [
            {
                "role": "user",
                "content": f"Here's a document:\n\n{document}\n\n---\n\n{question}",
            }
        ]

        # Generate an answer using the OpenAI API (streaming).
        stream = client.chat.completions.create(
            model="gpt-5-chat-latest",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        # If your Streamlit version needs a generator, switch to a token generator.
        st.write_stream(stream)
