from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

user_data = {
    "initial_answers": {},
    "additional_answers": {}
}
additional_questions = []

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
    profile = {
        "name": data["initial_answers"].get("question-0"),
        "age": data["initial_answers"].get("question-1"),
        "hobbies": data["initial_answers"].get("question-2"),
        "favorite_book": data["initial_answers"].get("question-3"),
        "personality": data["initial_answers"].get("question-4"),
        "social_preference": data["initial_answers"].get("question-5"),
        "favorite_movie": data["initial_answers"].get("question-6"),
        "favorite_music_genre": data["initial_answers"].get("question-7"),
        "travel_preference": data["initial_answers"].get("question-8"),
        "dream_job": data["initial_answers"].get("question-9"),
        "strengths_weaknesses": data["initial_answers"].get("question-10"),
        "pets": data["initial_answers"].get("question-11"),
        "favorite_food": data["initial_answers"].get("question-12"),
        "friendship_values": data["initial_answers"].get("question-13"),
        "stress_handling": data["initial_answers"].get("question-14"),
        "motivation": data["initial_answers"].get("question-15"),
        "desired_skill": data["initial_answers"].get("question-16"),
        "admired_person": data["initial_answers"].get("question-17"),
        "long_term_goals": data["initial_answers"].get("question-18"),
        "free_time_activities": data["initial_answers"].get("question-19"),
        "additional_question_0": data["additional_answers"].get("additional-question-0"),
        "additional_question_1": data["additional_answers"].get("additional-question-1"),
        "additional_question_2": data["additional_answers"].get("additional-question-2")
    }
    return profile

if __name__ == '__main__':
    app.run(debug=True)