import os
from flask import Flask, render_template, request
from preprocessing import normalize_text, preprocess_document
from term_weighting import *
from vectorization import *
from similarity import *
from query import *

app = Flask(__name__)

# Configure the upload folder for documents
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "docx", "doc"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to check if the file extension is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        # Check if file1 and file2 are included in the request
        if "file1" not in request.files or "file2" not in request.files:
            return render_template("search.html", error="Please upload two files.")

        file1 = request.files["file1"]
        file2 = request.files["file2"]
        term_weighting = request.form.get("weighting")
        similarity_method = request.form.get("similarity")

        if file1.filename == "" or file2.filename == "":
            return render_template("search.html", error="Please select two files.")

        if (
            file1
            and allowed_file(file1.filename)
            and file2
            and allowed_file(file2.filename)
        ):
            
            # Save the uploaded files to the upload folder
            file1_path = os.path.join(app.config["UPLOAD_FOLDER"], file1.filename)
            file2_path = os.path.join(app.config["UPLOAD_FOLDER"], file2.filename)
            file1.save(file1_path)
            file2.save(file2_path)

            # Preprocess the content using the imported methods
            preprocessed_text1 = preprocess_document(file1_path)
            preprocessed_text2 = preprocess_document(file2_path)

            # Vectorize each document individually
            document_paths = [file1_path, file2_path]
            feature_names_list, document_vectors_list = vectorize_documents(
                document_paths
            )

            # Compute term weights based on the user's choice
            term_weights = None
            if term_weighting in ["Both", "TF", "IDF"]:
                term_weights = compute_tf_idf_weights(file1_path, file2_path)

                # Calculate similarity based on the selected method

            similarity_method = request.form['similarity']

            # Calculate similarity based on the selected method
            similarity_score = calculate_similarity(preprocessed_text1, preprocessed_text2, similarity_method)



            message = (
                "Files are accepted. Term Weighting: {}, Similarity Method: {}".format(
                    term_weighting, similarity_method
                )
            )

            return render_template(
                "search.html",
                message=message,
                preprocessed_text1=preprocessed_text1,
                preprocessed_text2=preprocessed_text2,
                term_weights=term_weights,
                weighting=term_weighting,
                v1=document_vectors_list[0],  # Use the first document's feature names
                v2=document_vectors_list[1],  # Use the second document's feature names
                similarity_score=similarity_score,
            )
        else:
            return render_template("search.html", error="Unsupported file type")

    return render_template("search.html", error=None)


@app.route("/search", methods=["GET", "POST"])
def search_documents():
    
        
    document_directory = "../testing_files"

    if request.method == "POST":
        query = request.form.get("query")  # Get the search query from the form
        results = search_documents_in_directory(query, document_directory)  # Call the search function

        # Filter documents based on similarity threshold
        filtered_results = [(path, score) for path, score in results if score > 0.0]

        if not filtered_results:
            # No matching documents found
            return render_template("search.html", search_results=[("No documents found", 0.0)], query=query)

        return render_template("search.html", search_results=filtered_results, query=query)



def calculate_similarity(preprocessed_text1,preprocessed_text2, similarity_method):
    if similarity_method == 'cosine':
        return calculate_cosine_similarity(preprocessed_text1,preprocessed_text2 )
    elif similarity_method == 'pcc':
        return calculate_pcc_similarity(preprocessed_text1,preprocessed_text2 )
    else:
        return None  # Handle unsupported similarity method
    
if __name__ == "__main__":
    app.run(debug=True)
