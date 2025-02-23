from flask import Flask, request, jsonify
from sharpapi import SharpApiService
from flask_cors import CORS  # Import CORS
import os
import google.generativeai as genai
from quiz_prompt import prompt_text
from answer_prompt import answer_prompt


sharp_api = SharpApiService(api_key="UvizKo42mpx6ieSVOv3cdM4WidlyKmbyYCAJVnYH");

app = Flask(__name__)
CORS(app)


openaiKey = "sk-proj-JNxacNZax8A02p_AHCE75Rsg_W3XaOmr-bctysHnrsp26BmosEYjywJlTyrVjwMIDP9up1DmYAT3BlbkFJkpaIsl - \
    fkAKt6-D5tovaSmZUHQD3bdnaRg6wlAr05ZKSdB3ZTOtACoYlcQ1bZr9C_OgJG7oKcA"


@app.route('/upload', methods=['POST'])
def upload_file():
    print("routed")
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
        print("cv =>", result)

        quiz = chat(str(result)).replace("```json", "").replace("```", "")
        print(quiz)
        return jsonify({"message": "File processed successfully", "data": {"quiz":quiz, "cvData":result}})
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/chat', methods=['POST'])
def chat(data):
    # print("request.json =>", request.json['cvData']['data'])
    genai.configure(api_key="AIzaSyAH2uWYbDoq2Yify7v0iFaNQTnG7JGguQI")
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = prompt_text + data
    response = model.generate_content(prompt)
    return response.text


@app.route('/submit-answers', methods=['POST'])
def report():
    # print("request.json =>", request.json['cvData']['data'])
    genai.configure(api_key="AIzaSyAH2uWYbDoq2Yify7v0iFaNQTnG7JGguQI")
    model = genai.GenerativeModel("gemini-1.5-flash")
    data = request.json['answers']
    prompt = answer_prompt + str(data)
    response = model.generate_content(prompt)
    return jsonify({"message": "data processed successfully", "data": response.text.replace("```json", "").replace("```", "")})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
