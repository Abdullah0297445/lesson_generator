import os
import base64

from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def get_image_description(b64_image):
    """
    Uses OpenAI's Vision API to generate a caption (description) for the uploaded image.
    According to the Vision API guide, we pass the image file and specify the task.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is in this image?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0]


def generate_lesson_plan(image_description):
    """
    Call the OpenAI text API to generate a lesson plan based on the image description.
    """
    prompt = (
        f"Given the following image description enclosed in the triple backticks create a creative and "
        "engaging children's lesson plan.\n"
        "List several activities a child can do with these objects, including steps and details.\n\n"
        f"```{image_description}```"
    )

    completion = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Given the following image description enclosed in the triple backticks create a creative and "
                    "engaging children's lesson plan.\n"
                    "List several activities a child can do with these objects, including steps and details.\n\n"
                    f"```{image_description}```"
                )
            },
            {
                "role": "developer",
                "content": (
                    "1 - You should always answer in bullet points."
                    "2 - Do not output more than ten bullet points."
                    "3 - For each bullet point do not output more than 3 to 4 sentences."
                )
            }
        ]
    )

    return completion.choices[0].message.content


@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    b64_file = base64.b64encode(file.read()).decode("utf-8")

    # Generate a description of the image using OpenAI's Vision API
    try:
        image_description = get_image_description(b64_file)
    except Exception as e:
        return jsonify({'error': f'Vision API error: {e}'}), 500

    # Use the generated description to create a lesson plan
    try:
        lesson_plan = generate_lesson_plan(image_description)
    except Exception as e:
        return jsonify({'error': f'Lesson plan generation error: {e}'}), 500

    return jsonify({'lesson_plan': lesson_plan})


if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get("FLASK_PORT"))
