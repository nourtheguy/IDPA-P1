import string
import os
from sklearn.feature_extraction.text import CountVectorizer
from preprocessing import preprocess_document
import spacy


def vectorize_documents(document_paths):
    # Load the English language model in spaCy
    nlp = spacy.load("en_core_web_sm")

    # Initialize lists to store feature names and document vectors
    feature_names_list = []
    document_vectors_list = []

    for document_path in document_paths:
        # Preprocess the document
        preprocessed_text = preprocess_document(document_path)

        # Join the preprocessed tokens into a string
        preprocessed_text = " ".join(preprocessed_text)

        # Vectorize the document using CountVectorizer
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform([preprocessed_text])

        # Get the feature names (words)
        feature_names = vectorizer.get_feature_names_out()

        # Convert the vector to a list of lists
        document_vector = X.toarray()

        # Append the feature names and document vector to the respective lists
        feature_names_list.append(feature_names)
        document_vectors_list.append(document_vector)

    return feature_names_list, document_vectors_list
