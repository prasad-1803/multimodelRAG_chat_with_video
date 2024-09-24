import os  
from pathlib import Path
from utils import download_video, get_transcript_vtt
from extract import extract_and_save_frames_and_metadata


vid1_url = "https://youtu.be/aWiW-PjB2hs?si=hw1CimniNs0y4Nl5"


vid1_dir = "./data/video1"
vid1_filepath = download_video(vid1_url, vid1_dir)

# Download Youtube video's subtitle to ./shared_data/videos/video1
vid1_transcript_filepath = get_transcript_vtt(vid1_url, vid1_dir)

# Define output directories
extracted_frames_path = os.path.join(vid1_dir, 'extracted_frame')
metadatas_path = vid1_dir

# Create these output folders if not existing
Path(extracted_frames_path).mkdir(parents=True, exist_ok=True)
Path(metadatas_path).mkdir(parents=True, exist_ok=True)

# Extract frames and metadata
metadata = extract_and_save_frames_and_metadata(
                vid1_filepath, 
                vid1_transcript_filepath,
                extracted_frames_path,
                metadatas_path,
            )

