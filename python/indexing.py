import os
from preprocessing import normalize_text
import win32com.client  # for handling .doc files
from docx import Document  # for handling .docx files

class InvertedIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, content):
        terms = normalize_text(content)
        for term in terms:
            term = term.lower()  # Ensure case-insensitivity
            if term in self.index:
                if doc_id not in self.index[term]:  # Avoid duplicate entries
                    self.index[term].append(doc_id)
            else:
                self.index[term] = [doc_id]

    def build_index_from_directory(self, document_directory):
        for root, _, files in os.walk(document_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith(".txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                elif file.lower().endswith(".doc"):
                    word = win32com.client.Dispatch("Word.Application")
                    doc = word.Documents.Open(file_path)
                    content = doc.Content.Text
                    doc.Close()
                    word.Quit()
                elif file.lower().endswith(".docx"):
                    doc = Document(file_path)
                    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                else:
                    continue  # Skip unsupported file types

                self.add_document(file_path, content)

    def query(self, word):
        word = word.lower()  # Ensure case-insensitivity
        return self.index.get(word, [])

if __name__ == "__main__":
    index = InvertedIndex()
    document_directory = "IDPA-P1/testing_files"
    index.build_index_from_directory(document_directory)

    # Test the indexing table
    query_term = "nader"
    results = index.query(query_term)

    if results:
        print(f"Documents containing '{query_term}':")
        for result in results:
            print(result)
    else:
        print(f"No documents containing '{query_term}' found.")
