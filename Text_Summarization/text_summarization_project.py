import streamlit as st
st.set_page_config(page_title="Text Summarization Tool", layout="wide")
try:
    from transformers import pipeline
except ImportError:
    raise ImportError("Please install the 'transformers' library: pip install transformers")
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
except ImportError:
    raise ImportError("Please install the 'sumy' library: pip install sumy")

@st.cache_resource
def load_model():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extractive_summary(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer_lsa = LsaSummarizer()
    summary = summarizer_lsa(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

def abstractive_summary(text):
    summarizer = load_model()
    summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
    return summary[0]['summary_text']

text_input = st.text_area("Enter your text here:", height=300)
method = st.selectbox("Choose summarization method:", ["Abstractive", "Extractive (LSA)"])

if st.button("Summarize"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Summarizing..."):
            result = abstractive_summary(text_input) if method=="Abstractive" else extractive_summary(text_input)
        st.subheader("Summary:")
        st.success(result)