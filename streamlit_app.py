import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

# Direktori untuk menyimpan file yang diunggah dan hasilnya
UPLOAD_FOLDER = 'uploaded_images'
RESULT_FOLDER = 'processed_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Fungsi untuk memproses gambar
def process_image(image, filter_type, level, rotation):
    # Terapkan filter
    if filter_type == 'Median Blur':
        level = level if level % 2 == 1 else level + 1  # Pastikan level adalah angka ganjil
        processed_img = cv2.medianBlur(image, level)
    elif filter_type == 'Bilateral Filter':
        processed_img = cv2.bilateralFilter(image, level * 2 + 1, level * 10, level * 10)

    # Terapkan rotasi
    if rotation != 0:
        # Hitung pusat gambar
        center = (processed_img.shape[1] // 2, processed_img.shape[0] // 2)
        # Buat matriks rotasi
        M = cv2.getRotationMatrix2D(center, rotation, 1.0)
        processed_img = cv2.warpAffine(processed_img, M, (processed_img.shape[1], processed_img.shape[0]))

    return processed_img

# Header aplikasi
st.title("Gaussian Blur and Image Processing Tool")
st.write("Upload an image, apply filters, and process it directly!")

# Unggah file gambar
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Simpan file yang diunggah
    img_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Baca gambar menggunakan OpenCV
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Konversi ke RGB untuk ditampilkan di Streamlit

    # Tampilkan gambar yang diunggah
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Pilihan filter
    filter_type = st.selectbox("Choose a filter", ["Median Blur", "Bilateral Filter"])

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
        processed_img_bgr = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)  # Konversi kembali ke BGR untuk penyimpanan
        cv2.imwrite(result_path, processed_img_bgr)

        # Tampilkan hasil
        st.image(processed_img, caption="Processed Image", use_column_width=True)

        # Tombol untuk mengunduh gambar
        with open(result_path, "rb") as file:
            btn = st.download_button(
                label="Download Processed Image",
                data=file,
                file_name=result_filename,
                mime="image/png"
            )
