import os
import zipfile
import streamlit as st




from google_images_download import google_images_download 

response = google_images_download.googleimagesdownload()  


def download_images(keyword,limit):
    arguments={"Keyword":keyword,"Limit":limit}  
    paths=response.download(arguments)
    return paths 

def create_zip(folder_path, zip_name="downloaded_images.zip"): 
    with zipfile.ZipFile(zip_name, 'w') as zipf:  
        for root, _, files in os.walk(folder_path): 
            for file in files:  
                zipf.write(os.path.join(root, file), file)
    return zip_name


st.title("download google images")

keyword = st.text_input("Enter the keyword for the images:")
limit = st.number_input("Enter the number of images to download:", min_value=1, step=1)


if st.button("Download"):  
    if keyword and limit:
        with st.spinner('Downloading images...'):
            paths = download_images(keyword, limit) 
            image_folder = list(paths.values())[0][0]  
            zip_file = create_zip(image_folder)  

        with open(zip_file, "rb") as fp:
            st.download_button(
                label="Download ZIP",
                data=fp,
                file_name=zip_file,
                mime="application/zip"
            )
    else:
        st.error("Please enter a keyword and a valid number of images.")
