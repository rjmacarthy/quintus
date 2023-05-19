import torch
import transformers
import asyncio

from inference.huggingface.model import HuggingFaceModel
from prompts.prompts import Prompts
from inference.base.chat import Chat
from utils.iteratorize import Iteratorize, Stream
from utils.torch_utils import clear_torch_cache

class HuggingfaceChat(Chat):
    def __init__(self):
        super().__init__()
        self.prompts = Prompts()
        self.model, self.tokenizer = HuggingFaceModel().get_instance()
        self.generate_params = {}

        while True:
            user_input = input("👤: ")
            prompt = self.prompts.context_prompt(user_input, "The company")
            response = self.generate_reply(prompt)
            asyncio.run(self.consume_stream(response))
        
    async def consume_stream(self, stream):
        async for line in stream:
            print(f"{line}", end="", flush=True)
        print()

    def get_reply_from_output_ids(self, output_ids, input_ids):
        new_tokens = len(output_ids) - len(input_ids[0])
        reply = self.tokenizer.decode(output_ids[-new_tokens:], skip_special_tokens=True)

        # Prevent LlamaTokenizer from skipping a space
        if type(self.tokenizer) is transformers.LlamaTokenizer and len(output_ids) > 0:
            if self.tokenizer.convert_ids_to_tokens(int(output_ids[-new_tokens])).startswith('▁'):
                reply = ' ' + reply

        return reply
    
    async def generate_reply(self, prompt):
        try:
            input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
            original_input_ids = input_ids
            output = input_ids[0]
            eos_token_ids = self.tokenizer.eos_token_id is not None and [self.tokenizer.eos_token_id] or []
            
            def generate_with_callback(self, callback=None, **kwargs):
                kwargs['stopping_criteria'].append(Stream(callback_func=callback))
                clear_torch_cache()
                with torch.no_grad():
                    self.model.generate(**kwargs)

            def generate_with_streaming(**kwargs):
                return Iteratorize(generate_with_callback, kwargs)

            with generate_with_streaming() as generator:
                for output in generator:
                    yield self.get_reply_from_output_ids(output, input_ids)
                    if output[-1] in eos_token_ids:
                            break
        except:
            raise
        finally:
            original_tokens = len(original_input_ids[0])
            new_tokens = len(output) - (original_tokens)
            yield self.tokenizer.decode(output[-new_tokens:], skip_special_tokens=True)
    
    def generate(self, prompt):
        reply = None
        for _, reply in enumerate(self.generate_reply(prompt)):
            yield reply
            
            