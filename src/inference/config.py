import yaml
from pathlib import Path

config_path = Path(__file__).parent / "config.yml"

with open(config_path, "r") as ymlfile:
    yml_config = yaml.safe_load(ymlfile)


class Config:
    def __init__(
        self,
        model_name,
        ft_model_name,
        temperature,
        top_p,
        top_k,
        num_beams,
        max_new_tokens,
    ):
        self.model_name = Path(__file__).parent.parent / model_name
        self.ft_model_name = Path(__file__).parent.parent / ft_model_name
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.num_beams = num_beams
        self.max_new_tokens = max_new_tokens


config = Config(**yml_config)
