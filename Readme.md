## Multimodal RAG Chat with Videos
 # Overview -
- This project implements a Multimodal Retrieval-Augmented Generation (RAG) chat system that allows users to interact with video content through a chat interface. It   leverages the Bridge Tower model for enhanced understanding and processing of video information alongside LVLMS for generating responses.

# Features
- Video Upload: Users can upload video files (mp4, mov, avi) or provide a YouTube URL for chat interactions.
- Video Playback: Videos are displayed for easy viewing directly within the application.
- Chat Interface: A chat input section allows users to send messages and receive responses based on the video's content.
- Backend Integration: Communicates with a backend service to handle video uploads and chat requests.

# Technologies Used
- Streamlit: For the frontend web application.
- Bridge Tower Model: For processing and understanding video content.
- LVLMS: For generating chat responses.
- Requests: For API calls to upload videos and send chat messages.

# Getting Started
**Clone the repository:**

```bash
Copy code
git clone <repository-url>
cd multimodal-rag-chat
Install the required packages:
```

```bash
Copy code
pip install -r requirements.txt
Run the Streamlit application:
```

```bash
Copy code
streamlit run app.py
Open your web browser and navigate to http://localhost:8501 to access the application.
```
# License
- This project is licensed under the MIT License.