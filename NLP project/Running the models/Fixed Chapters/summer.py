import pandas as pd
import re
from transformers import pipeline
import torch
import json

"""
This scirpt was run on the student HPC cluster, using submit_pyhton.sh
the output is a single json file for every video analyzed

"""
# Check if CUDA is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

df = pd.read_csv('../../data/19k_transcripts.csv')

# Load the summarizer model on GPU
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)  # device=0 for the first GPU

def get_summary(text, vid_id):
    print(vid_id)
    # Split the text into 8 approximately equal parts
    chunk_size = len(text) // 8
    chunks = [text[i*chunk_size:(i+1)*chunk_size] for i in range(8)]

    summaries = []

    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) == 0:  # Skip empty chunks
            continue

        # Adjust max_length based on the length of the chunk
        chunk_length = len(chunk.split())
        max_length = min(50, chunk_length)  # Limit the max length to ensure summaries are concise

        try:
            # Summarize each chunk with a more constrained max_length
            chunk_summary = summarizer(chunk, max_length=max_length, min_length=10, do_sample=False)
            summary_text = chunk_summary[0]["summary_text"]

            # Ensure the summary is around 10 words
            summary_words = summary_text.split()
            if len(summary_words) > 15:
                summary_text = ' '.join(summary_words[:15]) + '...'
            else:
                summary_text = ' '.join(summary_words) + '...'

            summaries.append(summary_text)
        except Exception as e:
            print(f"Error summarizing chunk {i+1} for video {vid_id}: {e}")
            summaries.append("Error processing this chunk...")

    # Create a dictionary to store summaries
    chapter_dict = {}
    for i, summary in enumerate(summaries, 1):
        chapter_dict[i] = summary

    with open(f'resFixed/{vid_id}.json', 'w') as json_file:
        json.dump(chapter_dict, json_file, indent=4)

"""
Here we manipualted the start of the range, because the job could only run for a max 
of 4 hours, so we manipulated the start of the range to keep up 
"""
for i in range(10772, len(df)):
    get_summary(df["plain_text"][i], df["id"][i])

