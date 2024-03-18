from flask import Flask, render_template, request, flash, redirect, url_for
import cv2
from werkzeug.utils import secure_filename
import os 

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif'}


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

app.secret_key = '0001'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and the filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newFilename = f"static/{filename}"
        cv2.imwrite(newFilename, imgProcessed)
    elif operation == "cwebp":
        newFilename = f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(newFilename, img, [cv2.IMWRITE_WEBP_QUALITY, 100])
    elif operation == "cpng":
        newFilename = f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(newFilename, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    elif operation == "cjpg":
        newFilename = f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newFilename, img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return newFilename



@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/how")
def how():
    return render_template("how.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        # Check if the file part is present in the request
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/static/error.html")

        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")




        


app.run(debug=True, host="0.0.0.0", port = 5001)
