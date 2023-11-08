import spacy
from sklearn.metrics.pairwise import cosine_similarity
import os
from docx import Document
import win32com.client


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


def calculate_cosine_similarity(file_path1, file_path2):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Read the contents of the two files
    document1 = read_document_content(file_path1)
    document2 = read_document_content(file_path2)

    # Process the documents using spaCy
    doc1 = nlp(document1)
    doc2 = nlp(document2)

    # Calculate the cosine similarity
    similarity = cosine_similarity([doc1.vector], [doc2.vector])[0][0]

    return similarity
