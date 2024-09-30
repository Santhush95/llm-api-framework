from transformers import pipeline
import torch
from pydantic import BaseModel
from typing import Any

class LLMModel:
    def __init__(self, name, tokenizer, type="text-classification"):
        self.name = name
        self.type = type
        self.tokenizer = tokenizer

    def pipe(self):
        pipe = pipeline(
            self.type,
            model=self.name,
            tokenizer=self.tokenizer,
            max_new_tokens=50
            # torch_dtype=torch.bfloat16
            # device_map="auto",
        )
        return pipe
    
    def output(self, input, **parameters):
        pipe = self.pipe()
        outputs = pipe(input, **parameters)
        return outputs

class LLMInput(BaseModel):
        inputs: str | list
        parameters: dict[str, Any] | None    