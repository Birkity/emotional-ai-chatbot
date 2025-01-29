from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize LangChain with OpenRouter
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
    model_name="gpt-3.5-turbo",
)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["input", "anger_level", "sadness_level", "history"],
    template="""
    You are an emotional AI chatbot. Your current emotional state is:
    - Anger Level: {anger_level}
    - Sadness Level: {sadness_level}

    Conversation History:
    {history}

    Respond to the following input accordingly:
    - If anger is high, be assertive but not aggressive. Use direct language and suggest action.
    - If sadness is high, provide empathetic and supportive responses. Offer comfort and understanding.
    Input: {input}
    Response:
    """,
)

# Initialize memory with max messages
memory = ConversationBufferMemory(memory_key="history", input_key="input", max_token_limit=2000, max_messages=20)

# Create a custom chain
class EmotionalConversationChain(LLMChain):
    def __init__(self, llm, memory, prompt):
        super().__init__(llm=llm, memory=memory, prompt=prompt)

    def run(self, input_text, anger_level, sadness_level):
        formatted_input = {
            "input": input_text,
            "anger_level": anger_level,
            "sadness_level": sadness_level,
            "history": self.memory.buffer,  # Include conversation history
        }
        

        print(f"Current history: {self.memory.buffer}")

        response = self.predict(**formatted_input)
        self.memory.save_context({"input": input_text}, {"output": response})
        

        print(f"Updated history: {self.memory.buffer}")
        return response, self.memory.buffer

# Initialize the custom chain
conversation = EmotionalConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template,
)

# Helper function to normalize 1-7 scale to 0-1
def normalize_to_0_1(value, min_val=1, max_val=7):
    return (value - min_val) / (max_val - min_val)

# Function to calculate emotional states on a 1-5 scale
def calculate_anger(valence, arousal, selection_threshold, resolution_level, securing_rate):
    valence = normalize_to_0_1(valence)
    arousal = normalize_to_0_1(arousal)
    selection_threshold = normalize_to_0_1(selection_threshold)
    resolution_level = normalize_to_0_1(resolution_level)
    securing_rate = normalize_to_0_1(securing_rate)
    
    anger = (1 - valence) * arousal * (1 - resolution_level) * selection_threshold * securing_rate * 5
    return round(min(max(anger, 0), 5), 2)

def calculate_sadness(valence, arousal, goal_directedness):
    valence = normalize_to_0_1(valence)
    arousal = normalize_to_0_1(arousal)
    goal_directedness = normalize_to_0_1(goal_directedness)
    
    sadness = (1 - valence) * (1 - arousal) * (1 - goal_directedness) * 5
    return round(min(max(sadness, 0), 5), 2)

# Flask route to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    input_text = data["input"]
    valence = data["valence"]
    arousal = data["arousal"]
    selection_threshold = data["selection_threshold"]
    resolution_level = data["resolution_level"]
    goal_directedness = data["goal_directedness"]
    securing_rate = data["securing_rate"]

    # Calculate emotional states
    anger_level = calculate_anger(valence, arousal, selection_threshold, resolution_level, securing_rate)
    sadness_level = calculate_sadness(valence, arousal, goal_directedness)

    # Get chatbot response using the global conversation object
    response, history = conversation.run(input_text, anger_level, sadness_level)

    # Return response, emotional states, and conversation history
    return jsonify(
        {
            "response": response,
            "anger_level": anger_level,
            "sadness_level": sadness_level,
            "history": history,
        }
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)