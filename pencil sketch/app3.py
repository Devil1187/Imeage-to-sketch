import os
import cv2
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import uuid

# --- 1. Your Pencil Sketch Conversion Function (Modified) ---
# NOTE: Added 'scale' parameter to function signature
def convert_to_sketch(input_path: str, output_path: str, ksize=(21, 21), scale: float = 256.0):
    """
    Converts an input image file to a pencil sketch and saves it to output_path.
    The 'scale' parameter adjusts sketch intensity/line thickness.
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

    # 5. Create pencil sketch using Color Dodge (division) with the adjustable scale
    sketch = cv2.divide(gray, inverted_blur, scale=scale)

    # Save the output image
    success = cv2.imwrite(output_path, sketch)
    return success
# ------------------------------------------------------------------


app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # --- NEW: Retrieve the scale value from the form ---
    # Default to 256.0 if not provided or invalid
    sketch_scale = 256.0
    if request.method == 'POST':
        try:
            # Get scale from form data, convert to float
            user_scale = request.form.get('scale', 256.0)
            sketch_scale = float(user_scale)
        except ValueError:
            pass # Use default scale if conversion fails

        # Check for file upload logic (rest of the original code)
        if 'file' not in request.files:
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)

        if file:
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_id = uuid.uuid4().hex
            original_filename = f"original_{unique_id}.{ext}"
            sketch_filename = f"sketch_{unique_id}.png"

            original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            file.save(original_path)
            
            sketch_path = os.path.join(app.config['UPLOAD_FOLDER'], sketch_filename)
            
            # --- NEW: Pass the retrieved scale to the function ---
            success = convert_to_sketch(original_path, sketch_path, scale=sketch_scale)
            
            if success:
                sketch_url = url_for('static', filename=f'uploads/{sketch_filename}')
                return render_template('index.html', sketch_url=sketch_url, current_scale=sketch_scale)
            else:
                return render_template('index.html', error="Image processing failed.", current_scale=sketch_scale)
    
    # Render the initial upload page (GET request)
    return render_template('index.html', current_scale=sketch_scale)

if __name__ == '__main__':
    app.run(debug=True)