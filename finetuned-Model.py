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
device =  torch.cuda.is_available()
print(device)

modelfinetuned = AutoModelForCausalLM.from_pretrained(model_name)
tokenizerfinetuned = AutoTokenizer.from_pretrained(model_name)

def generate_text_with_constraints(prompt, max_tokens=100):

  model_name_or_path = model_name# Replace with your model path
  tokenizer = tokenizerfinetuned
  model = modelfinetuned


  pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=max_tokens, truncation=True)

  # Generate initial text
  initial_output = pipe(f"<s>[INST] {prompt} [/INST]")
  generated_text = initial_output[0]['generated_text']

  # Implement a loop to refine the output (optional)
  # You can add logic here to check for sentence completion, adjust max_length, etc.

  return generated_text

# Example usage:
prompt = "How is real estate market of Kitchener doing?"
result = generate_text_with_constraints(prompt, max_tokens=100)
print(result)