from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key for authentication
genai.configure(api_key="AIzaSyA6Bkhpmh6MY2-whmHejhRUsnA286YsExI")

# Set up the model with generation configuration and safety settings
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Function to start a conversation
def start_conversation():
    return model.start_chat(history=[
        {
            "role": "user",
            "parts": ["car"]
        },
        {
            "role": "model",
            "parts": ["**Noun**\n\n1. A motor vehicle with four wheels, an engine that powers it, and seats for one to eight people.\n2. A railway carriage for passengers.\n3. A cable car or funicular railway.\n4. (informal) A stolen vehicle.\n\n**Verb**\n\n1. To transport or drive (someone or something) in a car.\n2. (slang) To steal (a car).\n\n**Examples**\n\n1. We drove to the beach in my new car.\n2. The car was parked illegally.\n3. The car was stolen from the driveway.\n4. The thief was arrested for car theft.\n\n**Synonyms**\n\n* Automobile\n* Vehicle\n* Motor car\n* Coach\n* Saloon\n* Sedan\n* Coupe\n* Hatchback\n* Estate car\n* Station wagon\n* SUV\n* Crossover"]
        }
    ])


# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chatbot route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.form['user_input']
    convo = start_conversation()
    convo.send_message(user_input)
    bot_response = convo.last.text
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
