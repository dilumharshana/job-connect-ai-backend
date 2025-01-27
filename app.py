from flask import Flask, request, jsonify
from sharpapi import SharpApiService
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
sharp_api = SharpApiService(api_key="UvizKo42mpx6ieSVOv3cdM4WidlyKmbyYCAJVnYH")
CORS(app)


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

        print(result)

        return ({"message": "File processed successfully", "data": result})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
