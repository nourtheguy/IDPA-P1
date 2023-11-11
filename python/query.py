import os
from preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

document_directory = "../testing_files"

def search_documents_in_directory(query, document_directory):
    # Initialize variables
    documents = []
    document_paths = []
    matched_documents = []

    # Load and preprocess documents
    for filename in os.listdir(document_directory):
        file_path = os.path.join(document_directory, filename)
        preprocessed_text = preprocess_document(file_path)
        documents.append(" ".join(preprocessed_text))
        document_paths.append(file_path)

    # Preprocess the query
    preprocessed_query = " ".join(normalize_text(query))

    # Vectorize documents + query
    vectorizer = TfidfVectorizer()
    all_texts = documents + [preprocessed_query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity between query and each document
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    for i in range(len(similarities[0])):
        for similarity in similarities[:, i]:  # Iterate over the elements in the similarities array
            if similarity > 0.0:  # Adjust the similarity threshold as needed
                matched_documents.append((document_paths[i], similarity))

    return matched_documents if matched_documents else [("No documents found", 0.0)]


