from flask import Flask, request, jsonify
import os
import base64
from pred import run_prediction
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/SAI GANESH S/Desktop/ultra_analytics/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    except Exception as e:
        print(f"Error converting image to base64: {str(e)}")
        return None

@app.route('/upload', methods=["POST"])
def upload():
    try:
        data = request.get_json()

        base64_image = data.get('image', '')
        email = data.get('Email_ID', 'default')  # Use a default value if Email_ID is not provided

        if not base64_image:
            return jsonify({"error": "No image provided"}), 400

        # Decode base64 image data
        image_data = base64.b64decode(base64_image)

        # Generate a unique filename for the image
        unique_filename = f"{email}.jpg"

        # Save the image to the specified folder with the unique filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        with open(image_path, 'wb') as f:
            f.write(image_data)


        if os.path.exists("C:/Users/SAI GANESH S/Desktop/ultra_analytics/results/train"):
            shutil.rmtree("C:/Users/SAI GANESH S/Desktop/ultra_analytics/results/train")

        print(image_path)
        run_prediction(image_path, "C:/Users/SAI GANESH S/Desktop/ultra_analytics/results/")


        output_path="C:/Users/SAI GANESH S/Desktop/ultra_analytics/results/train"
        predicted_image_path = os.path.join(output_path, f"{email}.jpg")
        encoded_predicted_image = image_to_base64(predicted_image_path)


        return jsonify({
            "message": "Image Uploaded Successfully",
            "image_path": predicted_image_path,
            "predicted_image_base64": encoded_predicted_image,
        })

    except Exception as e:
        print(f"Error during upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
