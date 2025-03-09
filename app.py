from flask import Flask, render_template, request, send_file, jsonify
import os
import requests

app = Flask(__name__)

# Set your API keys (You should use environment variables in production)
ZOOCAD_API_KEY = "your_zoocad_api_key"
KITTYCAD_API_KEY = "your_kittycad_api_key"

OUTPUT_FILE = "static/generated_model.glb"

def generate_3d_model(api_key, text_prompt):
    """ Call the ZOOCAD or KITTYCAD API to generate a 3D model from text. """
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"prompt": text_prompt}

    response = requests.post("https://api.zoo.dev/generate-3d", headers=headers, json=data)
    
    if response.status_code == 200:
        model_url = response.json().get("model_url")
        model_data = requests.get(model_url)

        with open(OUTPUT_FILE, "wb") as file:
            file.write(model_data.content)

        return OUTPUT_FILE
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_prompt = request.form.get("text_prompt")
        api_choice = request.form.get("api_choice")

        if api_choice == "zoocad":
            api_key = ZOOCAD_API_KEY
        elif api_choice == "kittycad":
            api_key = KITTYCAD_API_KEY
        else:
            return jsonify({"error": "Invalid API choice"})

        model_file = generate_3d_model(api_key, text_prompt)

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
