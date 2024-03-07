#VERSION FUNCIONAL
from flask import Flask, render_template, request, send_from_directory
import numpy as np
import cv2
import easyocr

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_image", methods=["POST"])
def process_image():
    if "image" in request.files:
        image_file = request.files["image"]
        image_stream = image_file.read()


        nparr = np.frombuffer(image_stream, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        language = request.form.get("language", "es")  # Valor predeterminado: español

   
        reader = easyocr.Reader([language], gpu=False)
        result = reader.readtext(image, paragraph=False)

  
        for res in result:
            pt1 = tuple(map(int, res[0][0])) 
            pt2 = tuple(map(int, res[0][2])) 
            cv2.rectangle(image, pt1, pt2, (166, 56, 242), 2)


        image_path = "static/processed_image.jpg"
        cv2.imwrite(image_path, image)

        return render_template("result.html", result=result, image_path=image_path)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(debug=True)
