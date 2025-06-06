


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

file_path = "spam.csv"
df = pd.read_csv(file_path, encoding='latin-1')[['Category', 'Message']]
df.head()

df['Category'] = df['Category'].map({'spam': 1, 'ham': 0})


X_train, X_test, y_train, y_test = train_test_split(df['Message'], df['Category'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:\n", report)


import streamlit as st
import joblib


joblib.dump(model, 'spam_classifier.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

model = joblib.load("spam_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Streamlit App
st.title("Email Spam Classifier")
st.write("Enter an email message below and the model will classify it as Spam or Ham.")

# Input text box
email_text = st.text_area("Enter email text here:")

if st.button("Classify"):
    if email_text:
        # Transform input text
        email_tfidf = vectorizer.transform([email_text])

        # Predict (1 = spam, 0 = ham)
        prediction = model.predict(email_tfidf)[0]
        result = "🚨 Spam" if prediction == 1 else "✅ Ham"

        st.subheader("Prediction:")
        st.write(result)
    else:
        st.warning("Please enter some text to classify.")
