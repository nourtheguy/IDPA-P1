import spacy
from sklearn.metrics.pairwise import cosine_similarity
import os
from docx import Document
import win32com.client
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


def read_document_content(file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        content = None  # Initialize content to None
        try:
            if file_extension == ".txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            elif file_extension == ".docx":
                doc = Document(file_path)
                content = " ".join([paragraph.text for paragraph in doc.paragraphs])
            elif file_extension == ".doc":
                word = win32com.client.Dispatch("Word.Application")
                doc = word.Documents.Open(file_path)
                content = doc.Content.Text
                doc.Close()
                word.Quit()
            else:
                print(f"Unsupported file format: {file_extension}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        return content

def calculate_cosine_similarity(text1, text2):
    # Combine the tokenized text into sentences for CountVectorizer
    combined_text = [" ".join(text1), " ".join(text2)]

    # Use CountVectorizer to create a bag-of-words representation
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(combined_text)

    # Calculate cosine similarity between the two document vectors
    similarity_matrix = cosine_similarity(vectors)

    # The similarity between the two documents is in the top right element of the matrix
    similarity = similarity_matrix[0, 1]

    return similarity


def calculate_pcc_similarity(text1, text2):

     # Combine the tokenized text into sentences for CountVectorizer
    combined_text = [" ".join(text1), " ".join(text2)]

    # Use CountVectorizer to create a bag-of-words representation
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(combined_text).toarray()

    # Calculate Pearson correlation coefficient between the two document vectors
    similarity = pearsonr(vectors[0], vectors[1])[0]

    return similarity