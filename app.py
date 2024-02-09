from flask import Flask, request, render_template, jsonify,flash,redirect,url_for,session
import google.generativeai as genai
import google.ai.generativelanguage as glm
import tensorflow as tf
from dotenv import load_dotenv
import os
from flask_mysqldb import MySQL
import secrets
from passlib.hash import sha256_crypt

# Generate a secure random secret key
secret_key = secrets.token_hex(16)
load_dotenv()


app = Flask(__name__)
app.secret_key = 'secret_key'
# connnection to database
app.config['MYSQL_HOST'] = os.getenv("HOST_NAME")
app.config['MYSQL_USER'] = os.getenv("HOST_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("HOST_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("HOST_DB")

mysql = MySQL(app)

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
    # checking if connection is successful
    cur = mysql.connection.cursor()
    cur.close()
    return render_template("home.html",data=cur)


@app.route("/handwriting-ocr")
def ocrHandwriting():
    if 'loginid' in session:
       
      return render_template("recognition.html")
    else:
       flash("To use OCR you need to login first","warning")
       return redirect(url_for("login"))

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
    return render_template("edaAnalyze.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]
      cur = mysql.connection.cursor()

      # exceuting query to get specific username,password
      cur.execute("SELECT username,password FROM users WHERE username=%s",(username,))
      user_exists = cur.fetchone()

      # checking if username is present in db
      if user_exists:
          store_username,store_password = user_exists

          # if present check user entered password with stored hash password
          if sha256_crypt.verify(password, store_password):
            # Password is correct

            # if password is correct redirect to home page
            session['loginid'] = True
            return redirect(url_for("index"))
          else:

            # if password does not match with stored password give error
            flash("username or password incorrect", "error")
            return redirect(url_for('login'))

      else:
          # if user is not found in database generated error
          flash("No Account Found with this username", "error")
          return redirect(url_for('login'))


    else:
      return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
      username = request.form['username']
      password = request.form['password']
      cpassword = request.form['cpassword']
      hashed_password = sha256_crypt.hash(password)
      cur = mysql.connection.cursor()
      

      # checking if password and cpassword matched
      if password != cpassword:
        flash("Password and Confirm password should match", "error")
        return redirect(url_for('signup'))
      else:
        # checking if username is already taken
        cur.execute("SELECT username from users WHERE username=%s",(username,))
        is_taken = cur.fetchone()
        print(is_taken)

        if is_taken:
            flash("Username Already Taken", "error")
            return redirect(url_for('signup'))
        

      
        #if everything is alright Proceed with registration
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash("Registration Successful! Login", "success")
        return redirect(url_for("login"))
    else:
        return render_template("signup.html")

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect the user to the login page or any other desired page
    return redirect(url_for('login'))

    
if __name__ == '__main__':
    app.run(debug=True)