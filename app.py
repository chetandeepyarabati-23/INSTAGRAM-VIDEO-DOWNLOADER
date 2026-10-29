import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Reels Downloader", page_icon="📹")

st.title("📹 Instagram Reel Downloader")
st.write("Paste a public Instagram Reel link below to download the video.")

reel_url = st.text_input("Reel Link:", placeholder="https://www.instagram.com/reel/...")

if st.button("Fetch & Download Video", type="primary"):
    if not reel_url.strip():
        st.warning("Please enter a valid Instagram URL.")
    else:
        try:
            with st.spinner("Extracting video..."):
                temp_dir = tempfile.mkdtemp()
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(reel_url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                with open(filename, "rb") as f:
                    video_bytes = f.read()

                st.success("Video successfully extracted!")
                st.video(video_bytes)
                
                st.download_button(
                    label="⬇️ Download MP4 File",
                    data=video_bytes,
                    file_name=f"reel_{info.get('id', 'video')}.mp4",
                    mime="video/mp4"
                )
        except Exception as e:
            st.error(f"Error fetching video: {str(e)}")
            st.info("Ensure the account is public and the link is direct to a Reel.")