import cv2
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk mengubah resolusi gambar
def resize_image(image, target_size):
    return cv2.resize(image, target_size)

# Fungsi untuk mengonversi gambar ke format RGB
def convert_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Fungsi untuk menampilkan gambar
def display_image(image, caption=None):
    if caption:
        st.image(image, caption=caption, use_column_width=False)
    else:
        st.image(image, use_column_width=True)

# Fungsi untuk menampilkan informasi pixel dalam tabel
def display_pixel_info(pixel_data, title):
    st.write(title)
    df = pd.DataFrame(pixel_data, columns=["Koordinat", "Red", "Green", "Blue"])
    st.table(df)

# Fungsi untuk menampilkan warna pixel saat mengklik pada gambar
def show_pixel_color(image, x, y):
    (b, g, r) = image[y, x]
    st.write(f"Warna pixel pada koordinat ({x}, {y}) - Red: {r}, Green: {g}, Blue: {b}")

st.markdown("""
    <style>
    table td:nth-child(1) {
        display: none
    }
    table th:nth-child(1) {
        display: none
    }
    </style>
    """, unsafe_allow_html=True)

st.header("Deteksi dan Informasi Warna pada Gambar")

# Upload gambar menggunakan Streamlit
uploaded_image = st.file_uploader("Pilih gambar", type=["jpg", "png", "jpeg"])

# Checkbox untuk mengontrol perubahan resolusi
change_resolution = st.checkbox("Ubah Resolusi Gambar ke 50x50")

# Inisialisasi variabel image
image = None

# Tampilkan gambar asli jika sudah ada
if uploaded_image is not None:
    # Ambil nilai byte gambar dari UploadedFile
    image_bytes = uploaded_image.read()

    # Baca gambar yang diunggah menggunakan OpenCV
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), 1)

    # Mengubah gambar ke resolusi 50x50 jika checkbox dicentang
    if image is not None and change_resolution:
        image = resize_image(image, (50, 50))
        display_image(convert_to_rgb(image), caption='Gambar yang Diunggah (50x50)')
    elif image is not None:
        display_image(convert_to_rgb(image), caption='Gambar yang Diunggah')

# Informasi pixel dari gambar yang sudah diubah resolusinya (looping dari 0,1 sampai 0,49)
if image is not None:  # Pastikan gambar telah diunggah
    pixel_data_x = []
    pixel_data_y = []
    
    for x in range(50):
        (b, g, r) = image[0, x]
        pixel_data_x.append([f"Pixel pada (0, {x})", r, g, b])

    for x in range(50):
        (b, g, r) = image[x, 0]
        pixel_data_y.append([f"Pixel pada ({x}, 0)", r, g, b])

    display_pixel_info(pixel_data_x, "Informasi Pixel Vertical")
    display_pixel_info(pixel_data_y, "Informasi Pixel Horizontal")