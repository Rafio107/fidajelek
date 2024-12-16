import streamlit as st
from PIL import Image, ImageFilter
import os

# Direktori untuk menyimpan file yang diunggah dan hasilnya
UPLOAD_FOLDER = 'uploaded_images'
RESULT_FOLDER = 'processed_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Fungsi untuk memproses gambar
def process_image(image, filter_type, level, rotation):
    # Pastikan nilai level (size) adalah bilangan ganjil
    level = level if level % 2 == 1 else level + 1

    # Terapkan filter
    if filter_type == 'Median Blur':
        processed_img = image.filter(ImageFilter.MedianFilter(size=level))
    elif filter_type == 'Bilateral Filter':
        # Pillow tidak mendukung Bilateral secara langsung, jadi kita gunakan GaussianBlur sebagai alternatif
        processed_img = image.filter(ImageFilter.GaussianBlur(radius=level))

    # Terapkan rotasi
    if rotation != 0:
        processed_img = processed_img.rotate(rotation, expand=True)

    return processed_img

# Sidebar untuk navigasi halaman
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ["Page 1: Instructions", "Page 2: Group Members", "Page 3: Image Processing"])

# Page 1: Instructions
if page == "Page 1: Group Linear 2":
    st.title("Instructions")
    st.write("""
    Welcome to the Image Processing Tool!
    
    - **Page 1**: Instructions on how to use the app.
    - **Page 2**: Information about the group members.
    - **Page 3**: Upload an image, apply filters, and process it.

    ### How to Use
    1. Navigate to **Page 3**.
    2. Upload your image using the file uploader.
    3. Select the filter type, set the blur/noise level, and choose rotation settings.
    4. Click "Process Image" to apply the changes.
    5. Download the processed image if desired.
    """)

# Page 2: Group Members
elif page == "Page 2: Group Members":
    st.title("Group Members")
    st.write("""
    ### Meet the Team
    1. Aldrian	004202300034
    2. Faiqotul Mufida	004202300001
    3. Muhammad Nova Ulin Nuha	004202300015
   
    We are passionate about building user-friendly tools and providing innovative solutions!
    """)

# Page 3: Image Processing
elif page == "Page 3: Image Processing":
    st.title("Image Processing Tool with Pillow")
    st.write("Upload an image, apply filters, and process it directly!")

    # Unggah file gambar
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Simpan file yang diunggah
        img_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Baca gambar menggunakan Pillow
        image = Image.open(img_path)

        # Tampilkan gambar yang diunggah
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Pilihan filter
        filter_type = st.selectbox("Choose a filter", ["Median Blur", "Bilateral Filter (Gaussian Blur Alternative)"])

        # Level blur atau noise
        level = st.slider("Blur/Noise Level (1-50)", min_value=1, max_value=50, value=5)

        # Rotasi gambar
        rotation = st.slider("Rotation (degrees)", min_value=0, max_value=360, step=90, value=0)

        # Tombol untuk memproses gambar
        if st.button("Process Image"):
            processed_img = process_image(image, filter_type, level, rotation)

            # Simpan hasil
            result_filename = f"processed_{uploaded_file.name}"
            result_path = os.path.join(RESULT_FOLDER, result_filename)
            processed_img.save(result_path)

            # Tampilkan hasil
            st.image(processed_img, caption="Processed Image", use_container_width=True)

            # Tombol untuk mengunduh gambar
            with open(result_path, "rb") as file:
                btn = st.download_button(
                    label="Download Processed Image",
                    data=file,
                    file_name=result_filename,
                    mime="image/png"
                )
