def text_to_3d(api_key, text_prompt, api_choice):
    """ Calls the selected API (ZOOCAD or KITTYCAD) to generate a 3D model from text. """
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    if api_choice == "zoocad":
        url = "https://api.zoo.dev/v1/generate-3d"
        data = {"prompt": text_prompt}

    elif api_choice == "kittycad":
        url = "https://api.kittycad.io/v1/models"
        data = {
            "prompt": text_prompt,
            "format": "glb"  # Make sure the output format is valid
        }

    else:
        return None

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        model_url = response.json().get("model_url")
        model_data = requests.get(model_url)

        with open("static/generated_model.glb", "wb") as file:
            file.write(model_data.content)

        return "static/generated_model.glb"
    
    else:
        print("API ERROR:", response.status_code, response.text)  # Debugging
        return None
