from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import pickle
from pymongo import MongoClient
import argparse
import time

"""
This script was run on our own private server (we rented it from hetzner),
we saved all the transcirpts in a MongoDB database and then downloaded them 
using MongoDB compass, the output will be included in the data folder(code/data/19k_transcripts.csv).
This scipt was run by run2.sh, wich ran the script 20 times with a 1 minute pause in between
"""


def get_t(vid_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid_id)
    except:
        transcript = None

    if transcript is not None:
        output=''
        for x in transcript:
            sentence = x['text']
            output += f' {sentence}'
    else: 
        output = None
    return transcript, output
    
def get_data():    
    with open("800k_ids.pickle", 'rb') as f:
        videos = pickle.load(f)
    return videos
    
def main():
    parser = argparse.ArgumentParser(description="number of videos")
    parser.add_argument("-n", "--number", type=int, help="Number of Videos")
    args = parser.parse_args()
    number = args.number
    start = number - 1000
    
    client = MongoClient()
    db = client.transcripts_speriamo
    posts = db.posts_grosso
    
    videos = get_data()
    
    for video_id in videos[start:number]:
        stuff = get_t(video_id)
        dict = {"id": video_id,
                "with_timestamps": stuff[0],
                "plain_text": stuff[1]}
        #print(dict)
        post_id = posts.insert_one(dict).inserted_id
        time.sleep(5)

    client.close()


if __name__ == "__main__":
    main()
    
        

    
    
  
    
    
  
