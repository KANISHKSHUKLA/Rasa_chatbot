# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa-pro/concepts/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="")

class ActionCollectInfo(Action):
    def name(self) -> Text:
        return "action_collect_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the latest customer message
        customer_message = tracker.latest_message.get('text')
        user_id = tracker.sender_id

        # Check if the intent requires a Gemini response
        intent = tracker.get_intent_of_latest_message()

        # Use Gemini API to generate a response
        try:
            # Example prompt for Gemini
            prompt = f"Customer query: {customer_message}. Provide a helpful and empathetic response."
            
            # Generate response using Gemini
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Send the Gemini-generated response back to the user
            if response and hasattr(response, "text"):
                gemini_response = response.text
                dispatcher.utter_message(text=gemini_response)
            else:
                # Fallback in case of no valid response from Gemini
                dispatcher.utter_message(text="Sorry, I couldn't generate a response right now.")
        except Exception as e:
            # Error handling for Gemini API call
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []