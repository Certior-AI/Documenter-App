import streamlit as st
from docx import Document
import pandas as pd
from collections import Counter
import re

#1. Function to extract text from the Word Doc
def get_docx_text(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

#2. Page Configuration
st.set_page_config(page_title="Doc Stats Pro", page_icon="📊")
st.title("📄 Word Doc Analyser")
st.write("Upload a .docx file to see summary statistics.")

#3. File Uploader
uploaded_file = st.file_uploader("Choose a Word file", type="docx")

if uploaded_file is not None:
    # Process the text
    text = get_docx_text(uploaded_file)
    words = re.findall(r'\w+', text.lower())

    #4. Metric Columns
    # We define 3 columns so col3 is recognised by Python
    col1, col2, col3 = st.columns(3)

    # Column 1: Word Count
    word_count = len(words)
    col1.metric("Word Count", len(words))

    #Column 2: Character Count
    col2.metric("Character Count", len(text))

    # Column 3: Character Count
    # (Assuming 200 words per minute) 
    reading_time = round(word_count / 200) #Use 'reading_time' here
    display_time = reading_time if reading_time >= 1 else "< 1"
    col3.metric("Reading Time", f"{reading_time} min") #Now they match

    #5. Visualisations
    st.markdown("---") #Adds a horizontal line
    st.subheader("Top 10 Most Frequent Words")

    # Filter out common short words to make the chart more interesting
    stop_words = ["the", "and", "to", "of", "a", "in", "is", "it", "that", "with", "as", "for", "on","or","this"]
    filtered_words = [w for w in words if w not in stop_words]

    word_freq = Counter(filtered_words).most_common(10)
    df_freq = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])
    
    # Display the bar chart
    st.bar_chart(df_freq.set_index('Word'))

    # 6. Text Preview
    with st.expander ("View Document Preview"):
        st.write(text)
