from flask import Flask, request, jsonify
from sharpapi import SharpApiService
from flask_cors import CORS  # Import CORS
from openai import OpenAI
import os
import google.generativeai as genai


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

        quiz = chat(str(result)).replace("```json", "").replace("```", "")
        print(quiz)
        return jsonify({"message": "File processed successfully", "data": quiz})
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/chat', methods=['POST'])
def chat(data):
    # print("request.json =>", request.json['cvData']['data'])
    genai.configure(api_key="AIzaSyAH2uWYbDoq2Yify7v0iFaNQTnG7JGguQI")
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "You are an AI specialized in HR and recruitment. You will analyze a given JSON object containing parsed CV data of a job applicant. This JSON object includes the applicant's personal details, education history, work experience, projects, and relevant industry-related skills. Your task is to carefully analyze the applicant’s experience level, industry background, and project work. Then, based on this analysis, generate 10 highly relevant and industry-specific job interview questions.Requirements:Relevance: The questions must be tailored to the applicant’s years of experience in the industry.Depth: Ensure the questions assess the applicant's technical expertise, problem-solving skills, and past project involvement.Project-Based: If the CV includes projects, generate at least 3 questions directly related to their project work.Validity: Avoid vague or generic questions. Each question should be precisely framed based on the data provided.Output Format: Always return the response as an array of 10 structured questions." + data
    response = model.generate_content(prompt)
    return response.text


if __name__ == '__main__':
    app.run(debug=True)
