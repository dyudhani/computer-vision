import streamlit as st
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import math

# Fungsi untuk mengubah gambar ke skala abu-abu (grayscale)
def convert_to_grayscale(image):
    grayscale_image = image.convert('L')
    return grayscale_image

# Fungsi untuk meningkatkan intensitas gambar
def enhance_intensity(image, intensity_factor):
    width, height = image.size
    enhanced_image = Image.new('RGB', (width, height))

    for x in range(width):
        for y in range(height):
            original_color = image.getpixel((x, y))
            shifted_color = tuple(min(c + intensity_factor, 255) for c in original_color)
            enhanced_image.putpixel((x, y), shifted_color)

    return enhanced_image

# Fungsi untuk membuat inverted image
def invert_image(image):
    width, height = image.size
    inverted_image = Image.new('RGB', (width, height))

    for x in range(width):
        for y in range(height):
            original_color = image.getpixel((x, y))
            inverted_color = tuple(255 - c for c in original_color)
            inverted_image.putpixel((x, y), inverted_color)

    return inverted_image

# Fungsi untuk rotasi gambar
def rotate_image(image, angle):
    width, height = image.size
    rotated_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(rotated_image)
    cx, cy = width / 2, height / 2
    radians = math.radians(angle)

    for x in range(width):
        for y in range(height):
            # Hitung koordinat piksel baru setelah rotasi
            x_new = (x - cx) * math.cos(radians) - (y - cy) * math.sin(radians) + cx
            y_new = (x - cx) * math.sin(radians) + (y - cy) * math.cos(radians) + cy

            # Ambil warna piksel asli
            original_color = image.getpixel((x, y))

            # Set warna piksel pada gambar hasil rotasi
            draw.point((x_new, y_new), fill=original_color)

    return rotated_image

# Fungsi untuk menghitung dan menggambar histogram intensitas keseluruhan
def plot_histogram(image, title):
    grayscale_image = image.convert('L')
    image_array = np.array(grayscale_image)
    intensity_hist, bins_intensity = np.histogram(image_array, bins=256, range=(0, 256))

    fig, ax = plt.subplots()
    ax.plot(bins_intensity[:-1], intensity_hist, color='gray', alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel('Intensitas (0 - 255)')
    ax.set_ylabel('Frekuensi')
    ax.set_xlim([0, 255])
    ax.grid()

    return fig

# Judul aplikasi
st.title('Image Enhancement, invert and rotation')

# Upload gambar
uploaded_image = st.file_uploader('Unggah gambar:', type=['jpg', 'png', 'jpeg'])

# Tambahkan slider untuk mengatur faktor intensitas
intensity_factor = st.slider('Faktor Intensitas:', min_value=1, max_value=100, value=2)

# Kolom untuk tampilan gambar asli, gambar yang telah ditingkatkan, gambar grayscale, dan inverted image
col1, col2 = st.columns(2)
plot1, plot2 = st.columns(2)

col3, col4 = st.columns(2)
plot3, plot4 = st.columns(2)

# Tombol untuk memproses gambar
if uploaded_image is not None:
    try:
        # Tampilkan gambar asli
        col1.image(uploaded_image, caption='Gambar Asli', use_column_width=True)

        # Konversi gambar yang diunggah menjadi objek PIL
        image = Image.open(uploaded_image)

        # Tampilkan histogram intensitas keseluruhan gambar asli
        plot1.pyplot(plot_histogram(image, 'Histogram Intensitas Keseluruhan - Gambar Asli'))

        # Meningkatkan intensitas gambar dengan faktor yang diatur oleh slider
        enhanced_image = enhance_intensity(image, int(intensity_factor))

        # Tampilkan gambar yang telah ditingkatkan intensitasnya
        col2.image(enhanced_image, caption='Gambar yang Telah Ditingkatkan Intensitasnya', use_column_width=True)

        # Tampilkan histogram intensitas keseluruhan gambar yang telah ditingkatkan
        plot2.pyplot(plot_histogram(enhanced_image, 'Histogram Intensitas Keseluruhan - Gambar Ditingkatkan'))

        # Mengubah gambar ke skala abu-abu (grayscale)
        grayscale = convert_to_grayscale(image)
        
        # Tampilkan gambar asli
        col3.image(uploaded_image, caption='Gambar Asli', use_column_width=True)

        # Konversi gambar yang diunggah menjadi objek PIL
        image = Image.open(uploaded_image)

        # Tampilkan histogram intensitas keseluruhan gambar asli
        plot3.pyplot(plot_histogram(image, 'Histogram Intensitas Keseluruhan - Gambar Asli'))

        # Membuat inverted image
        inverted = invert_image(image)

        # Tampilkan inverted image
        col4.image(inverted, caption='Inverted Image', use_column_width=True)

        # Tampilkan histogram intensitas keseluruhan inverted image
        plot4.pyplot(plot_histogram(inverted, 'Histogram Intensitas Keseluruhan - Inverted Image'))
        
        # Fungsi untuk menampilkan hasil rotasi
        def show_rotated_images(image, angles):
            col4, col5, col6 = st.columns(3)
            for angle in angles:
                rotated = rotate_image(image, angle)
                col4.image(rotated, caption=f'Rotasi {angle} derajat', use_column_width=True)

        # Tampilkan hasil rotasi dengan beberapa sudut
        rotation_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        show_rotated_images(image, rotation_angles)

    except Exception as e:
        st.error(f'Error: {str(e)}')
