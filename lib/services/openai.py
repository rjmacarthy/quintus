import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "gpt-3.5-turbo"


def get_model():
    return model_engine


def get_completion(messages):
    completion = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages,
    )

    message = completion["choices"][0]["message"]["content"]

    return message
