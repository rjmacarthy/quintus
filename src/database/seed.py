from schema.config import LocalModelConfig
from database.repository import Repository


def seed_config():
    repository = Repository(LocalModelConfig)

    repository.create(
        model_name_or_path="models/llama-7b",
        ft_model_name_or_path="models/llama-7b-ft",
        temperature=0.2,
        top_p=0.9,
        top_k=50,
        num_beams=4,
        max_new_tokens=512,
    )


def seed():
    seed_config()


if __name__ == "__main__":
    seed()
