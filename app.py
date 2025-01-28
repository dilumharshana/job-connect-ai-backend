from flask import Flask, request, jsonify
from sharpapi import SharpApiService
from flask_cors import CORS  # Import CORS
from openai import OpenAI
import os

app = Flask(__name__)
sharp_api = SharpApiService(api_key="UvizKo42mpx6ieSVOv3cdM4WidlyKmbyYCAJVnYH")
CORS(app)


openaiKey = "sk-proj-JNxacNZax8A02p_AHCE75Rsg_W3XaOmr-bctysHnrsp26BmosEYjywJlTyrVjwMIDP9up1DmYAT3BlbkFJkpaIsl - \
    fkAKt6-D5tovaSmZUHQD3bdnaRg6wlAr05ZKSdB3ZTOtACoYlcQ1bZr9C_OgJG7oKcA"


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save the file temporarily
        file_path = f"./{file.filename}"
        file.save(file_path)

        # Parse Resume using Sharp API
        status_url = sharp_api.parse_resume(
            file_path=file_path, language='English')

        # Fetch and return the parsed resume data
        parsed_resume = sharp_api.fetch_results(status_url)
        result = parsed_resume.get_result_json()
        return ({"message": "File processed successfully", "data": result})
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/chat', methods=['POST'])
def chat():
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=50,
        n=1,
        temperature=0,
        messages=[
            {"role": "user", "content": "hello"}
        ]
    )

    print(response)


if __name__ == '__main__':
    app.run(debug=True)
