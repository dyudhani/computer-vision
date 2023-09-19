import streamlit as st
import numpy as np
from PIL import Image


# Fungsi untuk meningkatkan kecemerlangan citra
def enhance_brightness(image, C_R, C_G, C_B):
    # Konversi gambar ke array NumPy
    image_array = np.array(image)

    # Inisialisasi citra yang ditingkatkan dengan salinan citra asli
    enhanced_image_array = np.copy(image_array)

    # Iterasi melalui setiap piksel dalam citra dan terapkan rumus peningkatan kecemerlangan
    for y in range(image_array.shape[0]):
        for x in range(image_array.shape[1]):
            R, G, B = image_array[y, x]
            R_enhanced = min(255, max(0, R + C_R))
            G_enhanced = min(255, max(0, G + C_G))
            B_enhanced = min(255, max(0, B + C_B))
            enhanced_image_array[y, x] = [R_enhanced, G_enhanced, B_enhanced]

    # Konversi array kembali ke gambar menggunakan PIL
    enhanced_image = Image.fromarray(enhanced_image_array.astype(np.uint8))
    return enhanced_image


# Judul aplikasi
st.title('Aplikasi Peningkatan Kecemerlangan Citra')

# Upload gambar
uploaded_image = st.file_uploader('Unggah gambar:', type=['jpg', 'png', 'jpeg'])

# Tombol untuk meningkatkan kecemerlangan citra
if uploaded_image is not None:
    try:
        # Tampilkan gambar yang diunggah
        st.image(uploaded_image, caption='Gambar Asli', use_column_width=True)

        # Tentukan nilai konstanta C untuk setiap saluran warna (R, G, dan B)
        C_R = st.slider('Konstanta untuk Saluran Merah (R):', min_value=-255, max_value=255, value=50)
        C_G = st.slider('Konstanta untuk Saluran Hijau (G):', min_value=-255, max_value=255, value=50)
        C_B = st.slider('Konstanta untuk Saluran Biru (B):', min_value=-255, max_value=255, value=50)
        
        # Tombol untuk meningkatkan kecemerlangan citra
        if st.button('Meningkatkan Kecemerlangan Citra'):
            # Meningkatkan citra
            enhanced_image = enhance_brightness(uploaded_image, C_R, C_G, C_B)

            # Tampilkan citra yang telah ditingkatkan kecemerlangannya
            st.image(enhanced_image, caption='Gambar yang Telah Ditingkatkan', use_column_width=True)

        else:
            st.error('Error: Citra harus berwarna (R, G, B)')

    except Exception as e:
        st.error(f'Error: {e}')
