from argparse import ArgumentParser

from database.schema.config import LocalModelConfig
from database.repository import Repository


def save_model_config(model_name: str, model_name_ft: str):
    repository = Repository(LocalModelConfig)

    repository.create(
        model_name_or_path=model_name,
        ft_model_name_or_path=model_name_ft,
        temperature=0.2,
        top_p=0.9,
        top_k=50,
        num_beams=4,
        max_new_tokens=512,
    )
