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
        self.model = model
        self.service = service
        self.api_key = api_key
        openai.api_key = api_key
        self.prompt = prompt
        if self.service == "openai":
            self.messages = [{"role": "system", "content": prompt}]

    def interact(self, message):
        """Interact with the LLM"""
        print(message)
        if self.service == "openai":
            self.messages.append({"role": "user", "content": message})
            result = openai.chat.completions.create(
                model=self.model, messages=self.messages
            )
            print(result)
            return result.choices[0].message.content
        
        return None

    def reset(self):
        """Reset messages history."""
        if self.service == "openai":
            self.messages = [{"role": "system", "content": self.prompt}]
        
        return None
