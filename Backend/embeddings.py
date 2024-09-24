import json
import os
import numpy as np
from numpy.linalg import norm
import cv2
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from tqdm import tqdm
from utils import encode_image 
from utils import bt_embedding_from_prediction_guard as bt_embeddings
from captions import parse_webvtt
import time


# Directory containing extracted images
image_directory = 'data/video1/extracted_frame'

# Path to the VTT captions file
vtt_file_path = './data/video1/captions.vtt'

# Parse the captions
captions = parse_webvtt(vtt_file_path)

# Ensure that you have at least as many captions as images, otherwise handle this condition
num_captions = len(captions)


# Helper function to find the closest caption based on image name or timestamp (optional logic)
def find_caption_for_image(image_name, captions):
    # Assuming image names have timestamps like 'frame_0000000000.png'
    # Extract numeric part and convert it to seconds (you can modify this if your image naming is different)
    timestamp_in_seconds = int(image_name.split('_')[1].split('.')[0]) / 1000.0  # Example logic
    
    # Find the closest caption by timestamp
    for caption in captions:
        start_time = caption_to_seconds(caption['start'])
        end_time = caption_to_seconds(caption['end'])
        if start_time <= timestamp_in_seconds <= end_time:
            return caption['text']
    
    # If no caption is found, return a placeholder
    return "No caption available"

# Convert timestamp (HH:MM:SS.mmm) to seconds
def caption_to_seconds(timestamp):
    h, m, s = map(float, timestamp.replace('.', ':').split(':'))
    return h * 3600 + m * 60 + s

# Generate embeddings for all images in the directory
embeddings = []
image_metadata = []  # Store metadata if needed
base=[]
# Iterate over all files in the specified directory and keep track of index i
for i, filename in enumerate(tqdm(os.listdir(image_directory))):
    # Check if the file is an image
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        img_path = os.path.join(image_directory, filename)
        
        # Select caption from the array starting at index 1
        if i + 1 < num_captions:
            caption = captions[i + 1]['text']
        else:
            caption = "No caption available"  # Fallback caption if there are fewer captions than images
        
        # Encode the image into base64 format
        base64_img = encode_image(img_path)
        base.append(base64_img)
        
        
        
        # Get the embedding using the caption and image
        embedding = bt_embeddings(caption, base64_img)
        
        # Append the embedding and metadata
        embeddings.append(embedding)
        image_metadata.append({
            'image_path': img_path,
            'caption': caption,
            'embedding': embedding
        })
        
        # Wait for 2 seconds before processing the next image
        

# Optionally, convert embeddings and metadata to DataFrame
embedding_df = pd.DataFrame(image_metadata)

# Save embeddings to a file or proceed with further processing
embedding_df.to_csv('image_embeddings_with_captions.csv', index=False)

print("Embeddings generated and saved for all images in the directory.")

