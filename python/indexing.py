from preprocessing import normalize_text


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

    def query(self, word):
        word = word.lower()  # Ensure case-insensitivity
        return self.index.get(word, [])


# # Testing the functionality of the InvertedIndex class.
# if __name__ == "__main__":
#     idx = InvertedIndex()

#     doc1_content = "I love coding"
#     doc2_content = "I love music"

#     idx.add_document("doc1", doc1_content)
#     idx.add_document("doc2", doc2_content)

#     print(idx.query("love"))
#     print(idx.query("coding"))

#     print(normalize_text(doc1_content))
#     print(normalize_text(doc2_content))

#     print(idx.index)
