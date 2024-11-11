import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
import pandas as pd
from itertools import islice

"""
This was run on the stundent HPC cluster,
here the output is a single txt file with the output of the model 
for every video analyzed
"""

# Set device to CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)


# Loading the model and tokenizer ========================================================
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
print("Tokenizer Loaded")

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
print("Model Loaded!")

# Loading data ============================================================================
df = pd.read_csv("../../data/19k_transcripts.csv")
df = df.drop(["Unnamed: 0","_id", "with_timestamps"], axis = 1)
data_dict = dict(zip(df['id'], df['plain_text']))
with open('prompt.txt', 'r') as file:
    # Read the entire contents of the file
    do_prompt = file.read()

print("Data Loaded")


# Using the model =========================================================================
"""
The actual for loop we used was structured in the follwoing way:
for number, vid_id in enumerate(islice(data_dict.keys(), <Starting Number>, None)):

this was done because each run had a time limt of 4 and half hours so we 
just counted the outputs to see where we were at. 
"""

for number, vid_id in enumerate(data_dict.keys()):
    text = data_dict[vid_id]
    input_text = do_prompt +  text

    messages = [
        {"role": "system", "content": "You are a heplful AI assistant that is expert in youtube transcripts, you will perfrom the instructions exactly as they are presented."},
        {"role": "user", "content": input_text},
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    responese_det = tokenizer.decode(response, skip_special_tokens=True))
    print(number)
    
    file_path = f"resLlama/{number}_{vid_id}.txt"
    with open(file_path, 'w') as file:
        file.write(responese_det)
