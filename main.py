from dotenv import load_dotenv
import os
from openai import OpenAI
from groq import Groq


class LLMApp:
    def __init__(self,
                 model="llama3.1",
                 temperature=0.7,
                 max_tokens=1024,
                 default_system_prompt="You are a helpful assistant."
                 ):
        """Initialize the LLM application"""
        self.model = model
        if default_system_prompt is None:
            default_system_prompt = "You are a helpful assistant."
        self.default_system_prompt = default_system_prompt
        self.conversation_history = []
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        self.groq_client = Groq(api_key=self.groq_api_key)
        self.chatbot_name = "Bestie"
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.groq_models = {
            "llama3.1": "llama-3.1-8b-instant",
            "llama3.3": "llama-3.3-70b-versatile"
        }
        self.open_ai_models = {
            "gpt5": "gpt-5",
            "gpt5nano": "gpt-5-nano",
            "gpt5mini": "gpt-5-mini",
        }
        if model in self.groq_models:
            self.client = self.groq_client
            self.model = self.groq_models[model]
        elif model in self.open_ai_models:
            self.client = self.openai_client
            self.model = self.open_ai_models[model]

    def chat(self, user_message, system_prompt, temperature=None, max_tokens=None):
        """
        Send a message and get a response

        Args:
            user_message: The user's message
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            The assistant's response text
        """

        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": f"{system_prompt}"
                }
            )

        # Add conversation history
        if self.conversation_history:
            messages.extend(self.conversation_history)

        # Add current user's message
        messages.append(
            {
                "role": "user",
                "content": f"{user_message}"
            }
        )

        # Make LLM call
        if self.model in self.groq_models.values():
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=1, #in GPT 5 it is fixed
                max_completion_tokens=max_tokens, #it is different now, the old  max_tokens is deprecated
            )

        # Extract response text
        assistant_message = response.choices[0].message.content

        return assistant_message


    # def get_response(
    #     self,
    #     user_message: str,
    #     system_prompt: str = None,
    # ) -> str:
    #     """
    #     Get response from the LLM based on user message and optional system prompt

    #     Args:
    #         user_message: The user's message
    #         system_prompt: Optional system prompt to set context
    #         temperature: Sampling temperature (0-1)
    #         max_tokens: Maximum tokens in response

    #     Returns:
    #         The assistant's response text
    #     """

    #     messages = []

    #     # Add system prompt if provided
    #     if system_prompt:
    #         messages.append(
    #             {
    #                 "role": "system",
    #                 "content": f"{system_prompt}"
    #             }
    #         )

    #     # Add conversation history
    #     if self.conversation_history:
    #         messages.extend(self.conversation_history)

    #     # Add current user's message
    #     messages.append(
    #         {
    #             "role": "user",
    #             "content": f"{user_message}"
    #         }
    #     )
    #     # Make LLM call
    #     if self.model in self.groq_models.values():
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=messages,
    #             temperature=self.temperature,
    #             max_tokens=self.max_tokens,
    #         )
    #     else:
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=messages,
    #             temperature=1,  # in GPT 5 it is fixed
    #             # it is different now, the old  max_tokens is deprecated
    #             max_completion_tokens=self.max_tokens,
    #         )

    #     # Extract response text
    #     assistant_message = response.choices[0].message.content

    #     return assistant_message


# if __name__ == "__main__":
#     app = LLMApp()
#     user_input = "Hello, how are you?"
#     response = app.get_response(user_input)
#     print("Assistant:", response)
