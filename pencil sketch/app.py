import os
import cv2
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import uuid # Used to generate unique filenames

# --- 1. Your Pencil Sketch Conversion Function (Modified for Web) ---
def convert_to_sketch(input_path: str, output_path: str, ksize=(21, 21), scale: float = 256.0):
    """
    Converts an input image file to a pencil sketch and saves it to output_path.
    Logic adapted directly from your pencil_sketch.py script.
    """
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        return False

    # 1. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Invert grayscale image
    inverted = 255 - gray

    # 3. Blur the inverted image (Gaussian)
    blurred = cv2.GaussianBlur(inverted, ksize, 0)

    # 4. Invert the blurred image
    inverted_blur = 255 - blurred

    # 5. Create pencil sketch using Color Dodge (division)
    sketch = cv2.divide(gray, inverted_blur, scale=scale)

    # Save the output image
    success = cv2.imwrite(output_path, sketch)
    return success
# ------------------------------------------------------------------


app = Flask(__name__)
# Configure static directory where images will be saved and served
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)

        if file:
            # Create a unique filename to prevent clashes
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_id = uuid.uuid4().hex
            original_filename = f"original_{unique_id}.{ext}"
            sketch_filename = f"sketch_{unique_id}.png" # Save sketch as PNG

            # Save the original file
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(original_path)
            
            # Define output path
            sketch_path = os.path.join(app.config['UPLOAD_FOLDER'], sketch_filename)
            
            # Process the image using your function
            success = convert_to_sketch(original_path, sketch_path)
            
            if success:
                # Pass the URL of the resulting sketch to the template
                sketch_url = url_for('static', filename=f'uploads/{sketch_filename}')
                return render_template('index.html', sketch_url=sketch_url)
            else:
                # Handle conversion failure
                return render_template('index.html', error="Image processing failed.")
    
    # Render the initial upload page (GET request)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)