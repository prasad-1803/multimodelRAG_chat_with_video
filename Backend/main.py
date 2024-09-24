from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from embedding import generate_video_embedding  # Import embedding function
from retrieval import search_videos            # Import retrieval function
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file part"}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(file_path)
        
        # 1. Generate Embedding
        embedding = generate_video_embedding(file_path) 

        # 2. Store Embedding (Example - In-memory for simplicity)
        #    In a real app, use a database like LanceDB:
        #    https://github.com/lancedb/lancedb 
        if 'embeddings' not in app.config:
            app.config['embeddings'] = {}
        app.config['embeddings'][filename] = embedding

        return jsonify({
            "message": "Video uploaded and embedded successfully!",
            "file_path": file_path
        })
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # 1. Generate Query Embedding
    query_embedding = generate_video_embedding(user_message, text=True)

    # 2. Retrieve Similar Videos
    retrieved_videos = search_videos(query_embedding, app.config['embeddings'])

    response_message = f"You asked: {user_message}\n\n"
    response_message += "Relevant videos:\n" + "\n".join(retrieved_videos)

    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)