import streamlit as st
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np

##### Image Enhancement #####
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

##### Image Inverted #####
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

##### Image Rotation #####
# Fungsi untuk rotasi gambar 90 derajat searah jarum jam
def rotate_image_90_clockwise(input_image):
    try:
        if input_image is not None:
            # Buka gambar menggunakan Pillow
            image = Image.open(input_image)

            # Konversi gambar menjadi array NumPy
            img_array = np.array(image)

            # Mendapatkan lebar dan tinggi gambar
            height, width, channels = img_array.shape

            # Buat array kosong untuk menyimpan hasil rotasi
            rotated_array = np.zeros((width, height, channels), dtype=np.uint8)

            # Lakukan rotasi sebesar 90 derajat searah jarum jam
            for x in range(width):
                for y in range(height):
                    rotated_array[x, y] = img_array[height - 1 - y, x]

            # Konversi array kembali menjadi gambar menggunakan Pillow
            rotated_image = Image.fromarray(rotated_array)

            return rotated_image
        else:
            return None

    except Exception as e:
        st.error(f'Error in rotate_image_90_clockwise: {str(e)}')
        return None

# Fungsi untuk rotasi gambar 180 derajat searah jarum jam
def rotate_image_180_clockwise(input_image):
    try:
        # Buka gambar menggunakan Pillow
        image = Image.open(input_image)

        # Konversi gambar menjadi array NumPy
        img_array = np.array(image)

        # Mendapatkan lebar dan tinggi gambar
        height, width, channels = img_array.shape

        # Buat array kosong untuk menyimpan hasil rotasi
        rotated_array = np.zeros_like(img_array, dtype=np.uint8)

        # Lakukan rotasi 180 derajat searah jarum jam
        for x in range(width):
            for y in range(height):
                rotated_array[height - 1 - y, width - 1 - x] = img_array[y, x]

        # Konversi array kembali menjadi gambar menggunakan Pillow
        rotated_image = Image.fromarray(rotated_array)

        return rotated_image

    except Exception as e:
        st.error(f'Error in rotate_image_180_clockwise: {str(e)}')
        return None
    
# Fungsi untuk rotasi gambar sesuai sudut yang ditentukan
def rotate_image_custom(input_image, angle_degrees):
    # Buka gambar menggunakan Pillow
    image = Image.open(input_image)

    # Konversi sudut rotasi dari derajat ke radian
    angle_radians = np.radians(angle_degrees)

    # Mendapatkan lebar dan tinggi gambar
    width, height = image.size

    # Menghitung dimensi baru setelah rotasi
    w_prime = int(abs(width * np.cos(angle_radians)) + abs(height * np.sin(angle_radians)))
    h_prime = int(abs(width * np.sin(angle_radians)) + abs(height * np.cos(angle_radians)))

    # Buat gambar baru untuk menyimpan hasil rotasi
    rotated_image = Image.new("RGB", (w_prime, h_prime))

    # Menghitung koordinat pusat untuk rotasi
    center_x = width / 2
    center_y = height / 2

    # Lakukan rotasi sesuai sudut yang ditentukan
    for x_prime in range(w_prime):
        for y_prime in range(h_prime):
            # Menghitung koordinat sebelum rotasi
            x = int((x_prime - w_prime / 2) * np.cos(-angle_radians) - (y_prime - h_prime / 2) * np.sin(-angle_radians) + center_x)
            y = int((x_prime - w_prime / 2) * np.sin(-angle_radians) + (y_prime - h_prime / 2) * np.cos(-angle_radians) + center_y)

            # Pastikan koordinat dalam batas gambar asli
            if 0 <= x < width and 0 <= y < height:
                pixel = image.getpixel((x, y))
                rotated_image.putpixel((x_prime, y_prime), pixel)

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
st.title('Image Enhancement, Invert, and Rotation')

# Upload gambar
uploaded_image = st.file_uploader('Unggah gambar:', type=['jpg', 'png', 'jpeg'])

# Tambahkan slider untuk mengatur faktor intensitas
intensity_factor = st.slider('Faktor Intensitas:', min_value=1, max_value=100, value=2)

# Checkbox untuk mengaktifkan rotasi 90 derajat
rotate_90_degrees = st.checkbox("Rotasi 90 Derajat")

# Checkbox untuk mengaktifkan rotasi 180 derajat
rotate_180_degrees = st.checkbox("Rotasi 180 Derajat")

# Checkbox untuk mengaktifkan rotasi sesuai sudut yang ditentukan
rotate_45_degrees = st.checkbox("Rotasi Sesuai Sudut (45 derajat)")

# Kolom untuk tampilan gambar asli, gambar yang telah ditingkatkan, gambar grayscale, inverted image, dan hasil rotasi
col1, col2 = st.columns(2)
plot1, plot2 = st.columns(2)

col3, col4 = st.columns(2)
plot3, plot4 = st.columns(2)

col5, col6, col7 = st.columns(3)

# Tombol untuk memproses gambar
if uploaded_image is not None:
    try:
        ##### Image Enhancement #####
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
        
        ##### Image Inverted #####
        
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
        
        ##### Image Rotation #####
        if rotate_90_degrees:
            # Rotasi 90 derajat searah jarum jam
            rotated_90_image = rotate_image_90_clockwise(uploaded_image)
            
            # Tampilkan gambar yang telah ditingkatkan intensitasnya dan dirotasi
            col5.image(rotated_90_image, caption='Gambar dengan Rotasi 90 Derajat', use_column_width=True)
            
        if rotate_180_degrees:
            # Rotasi 180 derajat searah jarum jam
            rotated_180_image = rotate_image_180_clockwise(uploaded_image)
            
            # Tampilkan gambar yang telah ditingkatkan intensitasnya dan dirotasi
            col6.image(rotated_180_image, caption='Gambar dengan Rotasi 180 Derajat', use_column_width=True)
            
        if rotate_45_degrees:
            # Rotasi sesuai sudut yang ditentukan (45 derajat)
            rotated_45_image = rotate_image_custom(uploaded_image, 45)
            
            # Tampilkan gambar yang telah dirotasi sesuai sudut yang ditentukan
            col7.image(rotated_45_image, caption='Gambar dengan Rotasi Sesuai Sudut (45 derajat)', use_column_width=True)

    except Exception as e:
        st.error(f'Error: {str(e)}')

