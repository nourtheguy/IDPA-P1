import string
import nltk
from docx import Document
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import os 
import win32com.client

# Download necessary datasets from NLTK
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")


# Function to normalize and preprocess text
def normalize_text(text):
    # Tokenize the input text into individual words
    tokens = word_tokenize(text)

    # Convert all tokens to lowercase
    tokens = [w.lower() for w in tokens]

    # Create a translation table to remove punctuation
    table = str.maketrans("", "", string.punctuation)

    # Remove punctuation from each token using the translation table
    stripped = [w.translate(table) for w in tokens]

    # Filter out tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]

    # Define a set of English stopwords
    stop_words = set(stopwords.words("english"))

    # Remove stopwords from the list of tokens
    words = [w for w in words if not w in stop_words]

    # Initialize an empty list to store lemmatized words
    lemmatized = []

    # Initialize the WordNet lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Iterate over each word and its part-of-speech tag
    for word, tag in pos_tag(words):
        # Check the part-of-speech tag and lemmatize accordingly
        if tag.startswith("V"):  # Verb
            word = lemmatizer.lemmatize(word, "v")
        elif tag.startswith("J"):  # Adjective
            word = lemmatizer.lemmatize(word, "a")
        elif tag.startswith("N"):  # Noun
            word = lemmatizer.lemmatize(word, "n")
        elif tag.startswith("R"):  # Adverb
            word = lemmatizer.lemmatize(word, "r")

        # Append the lemmatized word to the list
        lemmatized.append(word)

    # Return the list of lemmatized words
    return lemmatized

# Function to preprocess a document
def preprocess_document(file_path):
    # Extract the file extension using the os module
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".txt":
        with open(file_path, "r") as file:
            content = file.read()
    elif file_extension == ".docx":
        doc = Document(file_path)
        content = " ".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_extension == ".doc":
        # Use win32com.client to extract text from .doc files
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        content = doc.Content.Text
        doc.Close()
        word.Quit()
    else:
        print("Unsupported file format")
        return None

    # Preprocess the content using the normalize_text function
    preprocessed_text = normalize_text(content)
    return preprocessed_text

# # Example usage
# input_file = "testing files\Document 1.docx"
# preprocessed_text = preprocess_document(input_file)

# # Print the preprocessed text
# print("\ntokens:\n", preprocessed_text)
