import gc
import torch


def clear_torch_cache():
    gc.collect()
    torch.cuda.empty_cache()
