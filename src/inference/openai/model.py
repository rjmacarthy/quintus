import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "gpt-3.5-turbo"


class OpenAIModel:
    def completion(self, messages):
        completion = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages,
        )

        message = completion["choices"][0]["message"]["content"]

        return message
