"""Lidya LLM connectors. Only work for OPENAI for the moment."""

#  Connector for your favorites LLMs
# Support
# [x] Ollama
# [v] OpenAI
# [x] Mistral
# [x] Claude

#  Imports
import openai  # ChatGPT


# Connector
class Connector:
    """Lidya LLM connector"""

    def __init__(self, model, service, api_key, prompt):
        """
         Initialize the instance. This is the method that must be called by 
         the user when interacting with OpenAI
         
         @param model - Model to use for access
         @param service - Service to use for access
         @param api_key - API key to use for access ( optional )
         @param prompt - Text to display in the prompt ( optional )
        """
        self.model = model
        self.service = service
        self.api_key = api_key
        openai.api_key = api_key
        self.prompt = prompt
        # This method is called when the service is openai
        if self.service == "openai":
            self.messages = [{"role": "system", "content": prompt}]

    def interact(self, message):
        """
         Interact with the LLM. This is a method to be called by the 
         user when they want to interact with the LLM
         
         @param message - The message that will be displayed to the user
         
         @return The user's response to the user or None if there is 
         no response to the inputted message
        """
        # Create a new message in the chat.
        if self.service == "openai":
            self.messages.append({"role": "user", "content": message})
            result = openai.chat.completions.create(
                model=self.model, messages=self.messages
            )
            print(result)
            return result.choices[0].message.content
        return None

    def reset(self):
        """
         Reset the history to the default state. This is called 
         when the user presses the reset button in the service
        """
        # This method is called when the service is openai
        if self.service == "openai":
            self.messages = [{"role": "system", "content": self.prompt}]
