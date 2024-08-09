from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    TrainingArguments,
    pipeline,
    logging,
)


model_name = "jyotsna2411/real-estate-chatbot" #path/to/your/model/or/name/on/hub


modelfinetuned = AutoModelForCausalLM.from_pretrained("/home/jyotsna/Virtual_Real_Estate_Agent/source/finetunedmodel/model", device_map="auto",  trust_remote_code=True).eval()
tokenizerfinetuned = AutoTokenizer.from_pretrained("/home/jyotsna/Virtual_Real_Estate_Agent/source/finetunedmodel/tokenizer")