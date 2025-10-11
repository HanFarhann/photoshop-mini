import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageChops
import numpy as np
import io

# === Konfigurasi dasar ===
st.set_page_config(page_title="Photoshop Mini++ by Hanskuy", page_icon="🎨", layout="wide")

# === CSS untuk tema gelap dan elegan ===
st.markdown("""
    <style>
        body { background-color: #111 !important; }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1f1f1f, #101010);
            color: white;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
        .stApp { background-color: #181818; color: #eee; }
        h1, h2, h3 {
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            color: #00b4d8 !important;
        }
        .block-container { padding-top: 1rem; }
        .stButton>button {
            background-color: #00b4d8;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
        }
        .stDownloadButton>button {
            background-color: #06d6a0;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
        }
    </style>
""", unsafe_allow_html=True)

# === Sidebar ===
st.sidebar.title("🎨 Photoshop Mini++ by Hanskuy")
st.sidebar.markdown("**Aplikasi Pengolahan Citra Berbasis Web**")
st.sidebar.write("---")

menu = st.sidebar.selectbox(
    "Pilih jenis operasi:",
    [
        "Citra Negatif",
        "Grayscale",
        "Image Brightening",
        "Operasi Aritmetika Dua Citra",
        "Operasi Boolean Dua Citra",
        "Operasi Geometri",
    ],
)

st.sidebar.write("---")
uploaded_file = st.sidebar.file_uploader("📤 Unggah Gambar", type=["jpg", "jpeg", "png"])
st.sidebar.caption("Format: JPG / PNG")

# === Fungsi Helper ===
def show_image(image, caption=""):
    """Menampilkan gambar dengan aman di Streamlit"""
    try:
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image.astype(np.uint8))
        st.image(image, caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Gagal menampilkan gambar: {e}")

def download_image(image, filename="hasil.png"):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("📥 Unduh Hasil", data=byte_im, file_name=filename, mime="image/png")

# === Konten utama ===
st.title("🖼️ Photoshop Mini++ by Hanskuy")

if uploaded_file:
    try:
        img = Image.open(uploaded_file).convert("RGB")
        show_image(img, "Gambar Asli")
        st.markdown("---")

        # === 1. Citra Negatif ===
        if menu == "Citra Negatif":
            st.subheader("🌓 Citra Negatif")
            neg = ImageOps.invert(img)
            show_image(neg, "Citra Negatif")
            download_image(neg, "citra_negatif.png")

        # === 2. Grayscale ===
        elif menu == "Grayscale":
            st.subheader("⚫ Grayscale")
            gray = ImageOps.grayscale(img)
            show_image(gray, "Citra Grayscale")
            download_image(gray, "grayscale.png")

        # === 3. Image Brightening ===
        elif menu == "Image Brightening":
            st.subheader("☀️ Brightness Control")
            brightness = st.slider("Atur kecerahan", 0.0, 3.0, 1.0, 0.1)
            enhancer = ImageEnhance.Brightness(img)
            bright = enhancer.enhance(brightness)
            show_image(bright, f"Hasil Brightening ({brightness}x)")
            download_image(bright, f"bright_{brightness}.png")

        # === 4. Operasi Aritmetika Dua Citra ===
        elif menu == "Operasi Aritmetika Dua Citra":
            st.subheader("➕➖ Operasi Aritmetika")
            second_file = st.file_uploader("Unggah Gambar Kedua", type=["jpg", "jpeg", "png"], key="second1")

            if second_file:
                other = Image.open(second_file).convert("RGB").resize(img.size)
                show_image(other, "Gambar Kedua")

                op = st.selectbox("Pilih operasi:", ["Tambah", "Kurang", "Rata-rata"])
                A = np.array(img, dtype=np.int16)
                B = np.array(other, dtype=np.int16)

                if op == "Tambah":
                    result = np.clip(A + B, 0, 255)
                elif op == "Kurang":
                    result = np.clip(A - B, 0, 255)
                else:
                    result = ((A + B) / 2).astype(np.uint8)

                result_img = Image.fromarray(result.astype(np.uint8))
                show_image(result_img, f"Hasil Operasi {op}")
                download_image(result_img, f"aritmetika_{op.lower()}.png")

        # === 5. Operasi Boolean Dua Citra ===
        elif menu == "Operasi Boolean Dua Citra":
            st.subheader("⚙️ Operasi Boolean")
            second_file = st.file_uploader("Unggah Gambar Kedua", type=["jpg", "jpeg", "png"], key="second2")

            if second_file:
                other = Image.open(second_file).convert("RGB").resize(img.size)
                show_image(other, "Gambar Kedua")

                op = st.selectbox("Pilih operasi Boolean:", ["AND", "OR", "XOR"])
                A = np.array(img)
                B = np.array(other)

                if op == "AND":
                    result = np.bitwise_and(A, B)
                elif op == "OR":
                    result = np.bitwise_or(A, B)
                else:
                    result = np.bitwise_xor(A, B)

                result_img = Image.fromarray(result.astype(np.uint8))
                show_image(result_img, f"Hasil Operasi Boolean {op}")
                download_image(result_img, f"boolean_{op.lower()}.png")

        # === 6. Operasi Geometri ===
        elif menu == "Operasi Geometri":
            st.subheader("📐 Transformasi Geometri")
            geo = st.selectbox("Pilih transformasi:", ["Translasi", "Rotasi", "Flipping", "Zooming"])

            if geo == "Translasi":
                dx = st.slider("Geser ke kanan (+) atau kiri (-)", -200, 200, 0)
                dy = st.slider("Geser ke bawah (+) atau atas (-)", -200, 200, 0)
                translated = ImageChops.offset(img, dx, dy)
                show_image(translated, f"Hasil Translasi ({dx}, {dy})")
                download_image(translated, f"translasi_{dx}_{dy}.png")

            elif geo == "Rotasi":
                angle = st.slider("Pilih sudut rotasi", 0, 360, 90)
                rotated = img.rotate(angle)
                show_image(rotated, f"Hasil Rotasi {angle}°")
                download_image(rotated, f"rotasi_{angle}.png")

            elif geo == "Flipping":
                flip = st.radio("Pilih arah flipping", ["Horizontal", "Vertikal"])
                flipped = ImageOps.mirror(img) if flip == "Horizontal" else ImageOps.flip(img)
                show_image(flipped, f"Hasil Flipping {flip}")
                download_image(flipped, f"flipping_{flip.lower()}.png")

            elif geo == "Zooming":
                zoom_factor = st.slider("Faktor Zoom", 1.0, 3.0, 1.5, 0.1)
                w, h = img.size
                new_size = (int(w * zoom_factor), int(h * zoom_factor))
                zoomed = img.resize(new_size)
                show_image(zoomed, f"Hasil Zooming ({zoom_factor}x)")
                download_image(zoomed, f"zoom_{zoom_factor}.png")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

else:
    st.warning("📸 Silakan unggah gambar terlebih dahulu dari sidebar.")
