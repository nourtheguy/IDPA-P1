import os
from preprocessing import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

document_directory = "testing files"


# Combined function to load, preprocess, vectorize the documents, and calculate cosine similarity
def search_documents(query, document_directory):
    # Initialize variables
    documents = []
    document_paths = []

    # Load and preprocess documents
    for filename in os.listdir(document_directory):
        file_path = os.path.join(document_directory, filename)
        preprocessed_text = preprocess_document(file_path)
        documents.append(" ".join(preprocessed_text))
        document_paths.append(file_path)

    # Preprocess the query
    preprocessed_query = " ".join(
        normalize_text(query)
    )  # Assuming normalize_text is defined in preprocessing.py

    # Vectorize documents + query
    vectorizer = TfidfVectorizer()
    all_texts = documents + [preprocessed_query]
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity between query and each document
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Pair each similarity score with the corresponding document path
    similarity_scores = list(zip(document_paths, similarities[0]))

    # Sort the documents based on similarity scores
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    return similarity_scores


# Example usage:
query_text = input("Enter your search query: ")

# Call the combined search function
results = search_documents(query_text, document_directory)

# Display the results
print("Documents ranked by similarity to the query:")
for path, score in results:
    print(f"Document: {path}, Similarity: {score}")
