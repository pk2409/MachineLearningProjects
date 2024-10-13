import streamlit as st
import os
import yt_dlp
from pydub import AudioSegment
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import shutil

#downloads the videos
def download_videos(singer_name, num_videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{singer_name}/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as youtube_dl:
        query = f'{singer_name} songs'
        youtube_dl.download([f'ytsearch{num_videos}:{query}'])


def converting_videos_to_audio(singer_name):
    audio_files = []
    for root, dirs, files in os.walk(singer_name):
        for file in files:
            if file.endswith(".mp3"):
                audio_files.append(os.path.join(root, file))
    return audio_files

#edits audio according to given duration
def cutting_the_audio(audio_files, duration):
    for audio_file in audio_files:
        audio = AudioSegment.from_mp3(audio_file)
        audio_cut = audio[:duration * 1000]
        audio_cut.export(audio_file, format="mp3")


def merging_the_audios(audio_files, output_file):
    combined_audios = AudioSegment.from_mp3(audio_files[0])
    for audio_file in audio_files[1:]:
        combined_audios += AudioSegment.from_mp3(audio_file)
    combined_audios.export(output_file, format="mp3")

#sends the email
def sending_an_email(to_email, zip_file):
    from_email = ""  
    password = "" 
    subject = "Mashup Audio File"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part = MIMEBase('application', "octet-stream")
    with open(zip_file, "rb") as f:
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="mashup.zip"')
    msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())


def create_zip(output_file):
    zip_file = f'{output_file}.zip'
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        zipf.write(output_file)
    return zip_file


st.title("Mashup Generator")


singer_name = st.text_input("Singer Name")
num_videos = st.number_input("Number of Videos")
audio_duration = st.number_input("Audio Duration in Seconds (greater than 20)", min_value=21)
output_file = st.text_input("Output File Name", value="mashup-output.mp3")
email_id = st.text_input("Email ID")


if st.button("Create the Mashup"):
    if not singer_name or not email_id or not output_file:
        st.error("Please fill all the fields before proceeding.")
    else:
        try:
            
            if os.path.exists(singer_name):
                shutil.rmtree(singer_name)  
            os.makedirs(singer_name)

            
            with st.spinner("Downloading videos..."):
                download_videos(singer_name, num_videos)
            st.success(f"Downloaded {num_videos} videos of {singer_name}.")

            audio_files = converting_videos_to_audio(singer_name)
            with st.spinner("Cutting audio files..."):
                cutting_the_audio(audio_files, audio_duration)
            st.success(f"Cut the first {audio_duration} seconds of each audio file.")

            with st.spinner("Merging audio files..."):
                merging_the_audios(audio_files, output_file)
            st.success(f"Audio files merged into {output_file}.")

            with st.spinner("Creating a zip file..."):
                zip_file = create_zip(output_file)
            st.success(f"Mashup zipped as {zip_file}.")

            with st.spinner("Sending the mashup via email..."):
                sending_an_email(email_id, zip_file)
            st.success(f"Mashup sent to {email_id} successfully.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
