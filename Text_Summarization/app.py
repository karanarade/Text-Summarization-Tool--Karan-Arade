# app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Text_Summarization.Summarization import summarize_text




st.title("📝 Text Summarization Tool")
st.markdown("Summarize lengthy articles using NLP")

st.write("DEBUG: app loaded")


# Input box
text_input = st.text_area("Enter your article or paragraph below:", height=500)

# Number of sentences in summary
num_sentences = st.slider("Number of sentences in summary:", 1, 10, 3)

if st.button("Summarize"):
    if text_input.strip():
        summary = summarize_text(text_input, num_sentences=num_sentences)


        st.subheader("🔍 Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")
