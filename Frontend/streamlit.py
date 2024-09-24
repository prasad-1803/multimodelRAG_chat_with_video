import streamlit as st
import requests

st.title("Multimodal RAG Chat with Videos")

# YouTube URL input section
st.header("YouTube Video Section")
youtube_url = st.text_input("Enter YouTube video URL:", key="youtube_url")

if youtube_url:
    # Display the YouTube video
    st.video(youtube_url)  # Streamlit will handle YouTube URLs directly

    # Create a button to send the YouTube URL to the backend
    if st.button("Send Video URL"):
        response = requests.post("http://127.0.0.1:5000/save-url", json={"video_url": youtube_url})

        if response.status_code == 200:
            st.write("Video URL sent successfully:", youtube_url)
        else:
            st.write("Error sending video URL:", response.status_code)

# Chat input section
st.header("Chat Section")
user_message = st.text_input("Enter your message:", key="chat_input")

if st.button("Send"):
    # Call your backend API for chat
    response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_message})

    if response.status_code == 200:
        # Display the response from the backend
        chat_response = response.json().get("response")
        st.write("Response from backend:", chat_response)
    else:
        st.write("Error:", response.status_code)
