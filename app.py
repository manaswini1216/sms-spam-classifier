import streamlit as st
import pickle
import string
import nltk
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()

stopwords = {"a","an","and","the","is","in","it","to","of","on","with","this","that","at","by","for","from","up","down","out",
             "as","if","or","you","did","my","do"}

def transform_text(text):
    text = text.lower()
    text = text.split()

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title('Email/SMS Spam Classifier')

input_sms = st.text_area('Enter the message')

if st.button('predict'):
    transformed_sms = transform_text(input_sms)
    vector_input = tf.transform([transformed_sms])
    result = model.predict(vector_input)[0]

    if result == 1:
        st.header('Spam')
    else:
        st.header('Not Spam')