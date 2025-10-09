# 🖍️ Pencil Sketch with Python (OpenCV)

Convert any photo into a realistic **pencil sketch** using simple image processing techniques with **Python + OpenCV**.

---

## 📸 Overview

This project takes an input image, converts it to grayscale, inverts it, applies a **Gaussian Blur**, and then combines it with the original grayscale image using the **Color Dodge** (division) blend technique to create a pencil-drawing effect.

Inspired by [AmanXAI – Pencil Sketch with Python](https://amanxai.com/2020/09/30/pencil-sketch-with-python/).

---

## ⚙️ Features

✅ Converts any image to a pencil-style sketch  
✅ Adjustable **intensity** (brightness / contrast)  
✅ Adjustable **blur strength** (detail level)  
✅ Works both in **GUI mode** (shows image windows) or **CLI mode** (saves output)  
✅ Lightweight — only requires `opencv-python`

---

## 🗂️ Project Structure

pencil-sketch-project/
│
├── pencil_sketch.py # Main Python script
├── README.md # Project documentation
├── venv/ # (optional) virtual environment
└── images/
├── input.jpg
└── sketch.png



---

## 🧰 Requirements

- Python 3.8 or above  
- `opencv-python` library

Install dependencies:

```bash
pip install opencv-python
💡 If you’re running on a headless server (no display), install:

nginx
Copy code
pip install opencv-python-headless
🚀 How to Run (Step-by-Step)
1️⃣ Clone or download this repository
bash
Copy code
git clone https://github.com/Devil1187/Python_Scripts/pencil-sketch-python.git
cd pencil-sketch-python
2️⃣ Place your image
Add your photo (e.g., photo.jpg) in the project folder.

3️⃣ Run in VS Code Terminal (or any terminal)
bash
Copy code
python pencil_sketch.py -i photo.jpg -o sketch.png
This will save the output image sketch.png in the same folder.

🧩 Optional Arguments
Argument	Description	Example
-i or --input	Input image path (required)	-i photo.jpg
-o or --output	Output path (optional)	-o output.png
-k or --ksize	Gaussian blur kernel size (odd numbers only)	-k 21 21
-s or --scale	Intensity / brightness of the sketch	-s 256.0

Example command:

bash
Copy code
python pencil_sketch.py -i photo.jpg -o sketch.png -k 35 35 -s 180
🎨 Adjusting Sketch Intensity
You can fine-tune how strong or light your pencil sketch appears by:

Changing scale → lower = darker lines, higher = lighter sketch

Changing ksize → smaller = more detail, larger = smoother sketch

Parameter	Effect	Typical Range
scale	Brightness / sketch intensity	128 → 512
ksize	Blur strength (detail)	(7,7) → (41,41)

🧠 How It Works
Convert the input image to grayscale

Invert the grayscale image (white ↔ black)

Apply Gaussian blur to the inverted image

Invert the blurred image again

Use cv2.divide() to blend gray + inverted blur (color dodge)

This produces realistic pencil-style strokes from brightness differences in the original image.

📷 Example
Input	Output

🧩 Future Enhancements
Add real-time intensity sliders with OpenCV trackbars

Add a small GUI using Tkinter

Batch convert multiple images

Export as PDF art sheet

🪪 Author
Hariom Lokhandkar
📧 Email: [lokhandkarhariom1.com]
💻 Project based on AmanXAI Blog

📜 License
This project is open-source and free to use for learning or personal projects.

