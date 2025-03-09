from flask import Flask, render_template, request, jsonify, send_file
import os
import requests

app = Flask(__name__)

OUTPUT_FILE = "static/generated_model.glb"

def text_to_3d(api_key, text_prompt, api_choice):
    """ Calls the selected API (ZOOCAD or KITTYCAD) to generate a 3D model from text. """
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"prompt": text_prompt}

    if api_choice == "zoocad":
        url = "https://api.zoo.dev/v1/generate-3d"
    elif api_choice == "kittycad":
        url = "https://api.kittycad.io/v1/models/generate"
    else:
        return None

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        model_url = response.json().get("model_url")
        model_data = requests.get(model_url)

        with open(OUTPUT_FILE, "wb") as file:
            file.write(model_data.content)

        return OUTPUT_FILE
    else:
        print("API ERROR:", response.status_code, response.text)  # Debugging
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_prompt = request.form.get("text_prompt")
        api_choice = request.form.get("api_choice")
        api_key = request.form.get("api_key")  # Manually entered API key

        if not api_key:
            return jsonify({"error": "API key is required"}), 400

        model_file = text_to_3d(api_key, text_prompt, api_choice)

        if model_file:
            return jsonify({"download_url": model_file})
        else:
            return jsonify({"error": "Failed to generate model"}), 500

    return render_template("index.html")

@app.route("/download")
def download():
    return send_file(OUTPUT_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
