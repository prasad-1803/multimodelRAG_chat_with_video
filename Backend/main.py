from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
# from embedding import generate_video_embedding  # Import embedding function
# from retrieval import search_videos            # Import retrieval function
from flask_cors import CORS
import os  
from pathlib import Path
from utils import download_video, get_transcript_vtt
from extract import extract_and_save_frames_and_metadata
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 
# In-memory storage for URLs
if 'video_urls' not in app.config:
    app.config['video_urls'] = []

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/save-url', methods=['POST'])
def save_url():
    data = request.get_json()
    video_url = data.get("video_url", "")
    
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400

    # Save URL to in-memory storage
    app.config['video_urls'].append(video_url)
        
    vid1_url = video_url


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



    return jsonify({"message": "Video URL saved successfully!", "video_url": video_url})


# @app.route('/upload', methods=['POST'])
# def upload_video():
#     if 'video' not in request.files:
#         return jsonify({"error": "No video file part"}), 400

#     file = request.files['video']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     filename = secure_filename(file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     try:
#         file.save(file_path)
        
#         # 1. Generate Embedding
#         embedding = generate_video_embedding(file_path) 

#         # 2. Store Embedding (Example - In-memory for simplicity)
#         #    In a real app, use a database like LanceDB:
#         #    https://github.com/lancedb/lancedb 
#         if 'embeddings' not in app.config:
#             app.config['embeddings'] = {}
#         app.config['embeddings'][filename] = embedding

#         return jsonify({
#             "message": "Video uploaded and embedded successfully!",
#             "file_path": file_path
#         })
#     except Exception as e:
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     user_message = data.get("message", "")

#     # 1. Generate Query Embedding
#     query_embedding = generate_video_embedding(user_message, text=True)

#     # 2. Retrieve Similar Videos
#     retrieved_videos = search_videos(query_embedding, app.config['embeddings'])

#     response_message = f"You asked: {user_message}\n\n"
#     response_message += "Relevant videos:\n" + "\n".join(retrieved_videos)

#     return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)