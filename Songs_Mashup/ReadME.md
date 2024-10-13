## SONGS MASHUP ##
This streamlit based program creates a web interface for creating  mashups of songs based on the user entered values - singer name , song duration , number of songs

--> LIBRARIES:
  1. use yt_dlp for downloading and extracting youtube videos
  2. use pydub for cutting and merging audio segments
  3. zipfile to compress the output audio into zip
  4. emal.mime and smtplib to send an email to user

--> FUNCTION SPECIFIC:
  1. yt_dlp.YoutubeDL searches and downaloads the top num_videos results
  2. smtplib.SMTP connects to gmail's SMTP server to send the mail to the provided email address
  3. the "create mashup" button triggers the entire process
  4. if folder with name of singer already exists , it creates a new one


THE INTERFACE
![image](https://github.com/user-attachments/assets/452dd70b-3c2a-4c09-8c08-9ff66ac1ac3d)

FOLDER AND FILES CREATED
![image](https://github.com/user-attachments/assets/f12fec72-5d41-45e5-867b-fcb6fbabd017)

OUTPUT AFTER RUNNING
![image](https://github.com/user-attachments/assets/8f8d56c4-a542-45e3-b024-94d8ad4dc419)

