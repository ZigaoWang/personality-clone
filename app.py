from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# In-memory cache for user data
user_data = {
    "initial_answers": {},
    "additional_answers": {}
}

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/submit_initial_answers', methods=['POST'])
def submit_initial_answers():
    answers = request.json
    user_data["initial_answers"].update(answers)
    additional_questions = generate_additional_questions(user_data["initial_answers"])
    return jsonify({"message": "Initial answers received!", "additional_questions": additional_questions})

@app.route('/submit_additional_answers', methods=['POST'])
def submit_additional_answers():
    answers = request.json
    user_data["additional_answers"].update(answers)
    profile = generate_profile(user_data)
    return jsonify({"message": "Additional answers received!", "profile": profile})

def generate_additional_questions(data):
    prompt = f"Based on the following user data, generate three additional questions to better understand the user:\n\n{data}\n\nQuestions:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    questions = response.choices[0].message.content.strip().split("\n")
    return questions[:3]  # Return the first three questions

def generate_profile(data):
    # Combine initial and additional answers
    combined_data = {**data["initial_answers"], **data["additional_answers"]}
    prompt = f"Generate a detailed user profile based on the following data. The profile should be professional, easy to understand, and formatted in Markdown. Include sections such as Personal Information, Interests, Preferences, and Additional Details. Here is the user data:\n\n{combined_data}\n\nProfile (in Markdown):"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    profile = response.choices[0].message.content.strip()
    return profile

if __name__ == '__main__':
    app.run(debug=True)