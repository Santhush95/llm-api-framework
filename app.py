##writefile app.py

from typing import Any
from fastapi import FastAPI
from fastapi import HTTPException
import tensorflow as tf

from ai import LLMModel, LLMInput

def llm_model_bert_classifier():
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

    model_name = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

    return LLMModel(model_name, tokenizer)

def llm_model_qwen_generator():
    from transformers import AutoTokenizer, AutoModelForCausalLM

    model_name = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

    return LLMModel(model_name, tokenizer, "text-generation")

def llm_controller(llm: dict[LLMModel]):
    @app.get("/")
    def status_gpu_check() -> dict[str, str]:
        gpu_msg = "Available" if tf.test.is_gpu_available() else "Unavailable"
        return {
            "status": "I am ALIVE!",
            "gpu": gpu_msg
        }

    @app.post("/classify/")
    async def classify(data: LLMInput) -> dict[str, Any]:
        try:
            inputs = data.inputs
            params = data.parameters or {}
            model_out = llm[0].output(inputs, **params)[0]
            print(model_out)
            return model_out
        except Exception as e:
            print(type(data))
            print(data)
            print(e)
            raise HTTPException(status_code=500, detail=len(str(e)))
        
    @app.post("/generate/")
    async def generate(data: LLMInput) -> dict[str, Any]:
        try:
            print(data)
            inputs = data.inputs
            params = data.parameters or {}
            model_out = llm[1].output(inputs, **params)[0]
            return model_out
        except Exception as e:
            print(type(data))
            print(data)
            print(e)
            raise HTTPException(status_code=500, detail=len(str(e)))

#Main Function
app = FastAPI()
llm_bert_classifier = llm_model_bert_classifier()
print(llm_bert_classifier.output("Today is a bad day because its monday."))


llm_qwen_generator = llm_model_qwen_generator()
prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
print(llm_qwen_generator.output(messages))

llm_controller([llm_bert_classifier, llm_qwen_generator])
