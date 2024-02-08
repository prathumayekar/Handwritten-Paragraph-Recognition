from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import google.ai.generativelanguage as glm
import tensorflow as tf
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

generation_config = {
  "temperature": 0.1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]


API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
# app routes and api endpoints

# for index
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/handwriting-ocr")
def ocrHandwriting():
    return render_template("ocr-recognition.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    temp_path = r"static\uploads\file.jpg"  # Specify a path to save the uploaded file temporarily
    file.save(temp_path)
    
    # # Read the image bytes
    with open(temp_path, 'rb') as file:
        bytes_data = file.read()

    # Create and configure the model
    # model = genai.GenerativeModel('gemini-pro-vision')
    model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

    # Generate content
    response = model.generate_content(
        glm.Content(
            parts=[
                glm.Part(text="The input image contains handwritten English text. You need to extract the text from the image"),
                glm.Part(inline_data=glm.Blob(mime_type='image/jpeg', data=bytes_data)),
            ],
        ),
        stream=True
    )

    # Resolve the response
    response.resolve()
        
    return jsonify({'extracted_text': response.text})

@app.route("/eda-analysis")
def edaAnalysis():
    return render_template("eda-analysis.html")

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
