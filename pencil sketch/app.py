import os
import cv2
import uuid
import numpy as np
from flask import Flask, request, render_template, redirect, url_for

# -----------------------------
# Pencil Sketch Conversion Method
# -----------------------------
def convert_to_sketch(input_path: str, output_path: str, ksize=(21, 21), scale: float = 256.0):
    img = cv2.imread(input_path)
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, ksize, 0)
    inverted_blur = 255 - blurred
    sketch = cv2.divide(gray, inverted_blur, scale=scale)

    return cv2.imwrite(output_path, sketch)


# -----------------------------
# Flask App Configuration
# -----------------------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file part in request.")

        file = request.files["file"]

        if file.filename == "" or not allowed_file(file.filename):
            return render_template("index.html", error="Invalid or empty file.")

        # Generate unique names for uploaded and output files
        ext = file.filename.rsplit(".", 1)[1].lower()
        unique_id = uuid.uuid4().hex

        original_filename = f"original_{unique_id}.{ext}"
        sketch_filename = f"sketch_{unique_id}.png"

        original_path = os.path.join(app.config["UPLOAD_FOLDER"], original_filename)
        sketch_path = os.path.join(app.config["UPLOAD_FOLDER"], sketch_filename)

        # Save original file
        file.save(original_path)

        # Convert to sketch
        success = convert_to_sketch(original_path, sketch_path)

        if not success:
            return render_template("index.html", error="Image conversion failed.")

        sketch_url = url_for("static", filename=f"uploads/{sketch_filename}")
        return render_template("index.html", sketch_url=sketch_url)

    return render_template("index.html")


# -----------------------------
# Production Entry Point
# -----------------------------
if __name__ == "__main__":
    # Bind to all IPs so EC2 can access it
    app.run(host="0.0.0.0", port=5000)
