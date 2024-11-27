from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_pdf_to_docx():
    # Get uploaded file
    pdf_file = request.files["pdf_file"]
    if pdf_file:
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        docx_filename = pdf_file.filename.rsplit(".", 1)[0] + ".docx"
        docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)

        # Save the uploaded PDF
        pdf_file.save(pdf_path)

        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        # Provide the DOCX file for download
        return send_file(docx_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
