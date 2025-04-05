import pyttsx3
from transformers import pipeline
import wikipediaapi
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for the text-to-speech engine
engine.setProperty('rate', 200)  # Set speaking rate
engine.setProperty('volume', 1.0)  # Set volume level
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the female voice

# Initialize the question-answering pipeline with T5 model
qa_pipeline = pipeline("question-answering", model="t5-large", tokenizer="t5-large")

# Initialize Wikipedia API with a custom User-Agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='MyPythonApp/1.0 (https://example.com; myemail@example.com)'
)

def search_wikipedia(query):
    """Search Wikipedia for a topic and return the summary."""
    try:
        page = wiki_wiki.page(query)
        if page.exists():
            return page.summary
        else:
            return "Sorry, I couldn't find relevant information on Wikipedia."
    except Exception as e:
        print(f"Error searching Wikipedia: {e}")
        return "There was an issue retrieving the information from Wikipedia."

def ask_question(question, context):
    """Ask a question and get an answer from the AI model."""
    if not context:
        return "I couldn't find an answer."
    result = qa_pipeline(question=question, context=context)
    return result.get('answer', "I couldn't find an answer.")

# Greet the user
greetings = [
    "Hello! My name is Jarvis. I am your personal assistant.",
    "Hi there! I'm Jarvis, your assistant. What can I do for you today?",
    "Greetings! I am Jarvis, your personal AI assistant."
]
engine.say(random.choice(greetings))
engine.say("You can ask me questions, and I will search for answers on Wikipedia.")

# Main loop to ask questions and get answers
while True:
    # Ask the user for a question
    question = input("Ask a question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        engine.say("Goodbye! Have a great day!")
        engine.runAndWait()  # Run speech queue here once
        break

    # Search Wikipedia for context
    context = search_wikipedia(question)

    # Get the answer from the AI model
    answer = ask_question(question, context)

    # Print and speak the answer
    print(f"Answer: {answer}")
    engine.say(f"The answer is: {answer}")

# Wait for all speech to finish before ending the program
engine.runAndWait()

# End of script, release resources
engine.say("Goodbye! Have a great day!")
engine.runAndWait()
