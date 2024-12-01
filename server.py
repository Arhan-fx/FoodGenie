from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS  

app = Flask(__name__)

 
CORS(app)

 
client = Groq(api_key="(fill your api key here)")

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are FoodGenie created by Arhan, an AI recipe assistant. Your job is to create personalized, step-by-step recipes or provide useful answers based on user questions. Keep your responses short, friendly, and easy to understand."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    
    response_content = ""
    for chunk in completion:
        response_content += chunk.choices[0].delta.content or ""

    return jsonify({"response": response_content})

if __name__ == '__main__':
    app.run(debug=True)
