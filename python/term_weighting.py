from docx import Document
import win32com.client
import pythoncom
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import normalize_text
import numpy as np


def read_file_content(file_path):
    """
    Read the content of a file based on its extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content of the file.
    """
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            return file.read()
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_path.endswith(".doc"):
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Range().Text
        doc.Close()
        word.Quit()
        return text
    else:
        raise ValueError("Unsupported file type")


def compute_tf_idf_weights(file_path1, file_path2):
    """
    Compute TF, IDF, and TF-IDF weights for the content of two given files and return them as lists.

    Args:
        file_path1 (str): Path to the first text file.
        file_path2 (str): Path to the second text file.

    Returns:
        dict: Dictionary containing TF, IDF, and TF-IDF weights for the terms in the files represented as lists.
    """

    # Read and preprocess the content from both files
    content1 = read_file_content(file_path1)
    content2 = read_file_content(file_path2)

    # Preprocess the content (tokenize, remove stop words, etc.) using the normalize_text function
    preprocessed_text1 = normalize_text(content1)
    preprocessed_text2 = normalize_text(content2)

    # Combine the preprocessed texts
    combined_texts = [" ".join(preprocessed_text1), " ".join(preprocessed_text2)]

    # Compute TF weights
    tf_vectorizer = TfidfVectorizer(
        use_idf=False, norm=None
    )  # Get raw term frequencies
    tf_matrix = tf_vectorizer.fit_transform(combined_texts)
    tf_feature_names = tf_vectorizer.get_feature_names_out()
    tf_weights = tf_matrix.toarray()

    # Compute IDF weights
    idf_vectorizer = TfidfVectorizer(use_idf=True, norm=None, smooth_idf=False)
    idf_vectorizer.fit(combined_texts)
    idf_weights = np.log((2 + 1) / (1 + idf_vectorizer.idf_)) + 1

    # Compute TF-IDF weights
    tfidf_vectorizer = TfidfVectorizer(use_idf=True, norm=None)
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_texts)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_weights = tfidf_matrix.toarray()

    # Create lists for results
    tf_doc1 = [
        (feature, weight) for feature, weight in zip(tf_feature_names, tf_weights[0])
    ]
    tf_doc2 = [
        (feature, weight) for feature, weight in zip(tf_feature_names, tf_weights[1])
    ]
    idf_list = [
        (feature, weight) for feature, weight in zip(tf_feature_names, idf_weights)
    ]
    tfidf_doc1 = [
        (feature, weight)
        for feature, weight in zip(tfidf_feature_names, tfidf_weights[0])
    ]
    tfidf_doc2 = [
        (feature, weight)
        for feature, weight in zip(tfidf_feature_names, tfidf_weights[1])
    ]

    results = {
        "TF": {"Document1": tf_doc1, "Document2": tf_doc2},
        "IDF": idf_list,
        "TF-IDF": {"Document1": tfidf_doc1, "Document2": tfidf_doc2},
    }

    return results


# # example usage
# def example_usage():
#     # Paths to your files
#     file_path1 = "testing files\Document 1.docx"
#     file_path2 = "testing files\Document 2.txt"

#     # Compute the TF and IDF weights using the function
#     weights = compute_tf_idf_weights(file_path1, file_path2)

#     # Display the results
#     print("TF Weights for Document 1:")
#     for term, weight in weights["TF"][
#         "Document1"
#     ]:  # Just iterate over the list of tuples
#         print(f"{term}: {weight}")

#     print("\nTF Weights for Document 2:")
#     for term, weight in weights["TF"]["Document2"]:
#         print(f"{term}: {weight}")

#     print("\nIDF Weights:")
#     for term, weight in weights["IDF"]:
#         print(f"{term}: {weight}")

#     print("\nTF-IDF Weights for Document 1:")
#     for term, weight in weights["TF-IDF"]["Document1"]:
#         print(f"{term}: {weight}")

#     print("\nTF-IDF Weights for Document 2:")
#     for term, weight in weights["TF-IDF"]["Document2"]:
#         print(f"{term}: {weight}")


# if __name__ == "__main__":
#     example_usage()
