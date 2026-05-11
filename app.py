import streamlit as st
from PIL import Image
import io
import torch

from utils import load_image_from_upload, tensor_to_image
from style_transfer import run_style_transfer

st.set_page_config(
    page_title="Picassify — Neural Style Transfer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=IM+Fell+English:ital@0;1&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #1a1209;
        background-image:
            radial-gradient(ellipse at 20% 20%, rgba(139, 90, 20, 0.15) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 80%, rgba(101, 55, 0, 0.12) 0%, transparent 60%),
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
        font-family: 'Cormorant Garamond', serif;
        color: #e8d5a3;
        min-height: 100vh;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 2rem 2rem;
        max-width: 1300px;
    }

    .header-ornament {
        text-align: center;
        color: #c9a84c;
        font-size: 1.4rem;
        letter-spacing: 0.8rem;
        margin-bottom: 0.5rem;
        opacity: 0.7;
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 700;
        text-align: center;
        color: #f0d080;
        letter-spacing: 0.15rem;
        line-height: 1;
        text-shadow:
            0 0 60px rgba(201, 168, 76, 0.4),
            0 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 0.3rem;
    }

    .main-title span {
        font-style: italic;
        color: #c9a84c;
    }

    .subtitle {
        font-family: 'IM Fell English', serif;
        font-style: italic;
        text-align: center;
        font-size: 1.3rem;
        color: #b8986a;
        letter-spacing: 0.1rem;
        margin-bottom: 0.5rem;
    }

    .divider {
        text-align: center;
        color: #c9a84c;
        font-size: 1.2rem;
        letter-spacing: 0.5rem;
        margin: 1.5rem 0;
        opacity: 0.6;
    }

    .divider::before,
    .divider::after {
        content: '————————————————';
        opacity: 0.3;
    }

    .upload-section {
        background: linear-gradient(135deg,
            rgba(40, 28, 10, 0.8) 0%,
            rgba(30, 20, 5, 0.9) 100%);
        border: 1px solid rgba(201, 168, 76, 0.25);
        border-radius: 4px;
        padding: 2rem;
        position: relative;
        box-shadow:
            0 4px 30px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(201, 168, 76, 0.1);
    }

    .upload-section::before {
        content: '';
        position: absolute;
        top: 6px;
        left: 6px;
        right: 6px;
        bottom: 6px;
        border: 1px solid rgba(201, 168, 76, 0.1);
        border-radius: 2px;
        pointer-events: none;
    }

    .corner-ornament {
        position: absolute;
        width: 20px;
        height: 20px;
        border-color: #c9a84c;
        border-style: solid;
        opacity: 0.5;
    }

    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 400;
        color: #f0d080;
        text-align: center;
        margin-bottom: 1.2rem;
        letter-spacing: 0.1rem;
    }

    .section-title span {
        font-style: italic;
        color: #c9a84c;
    }

    .instruction-text {
        font-family: 'IM Fell English', serif;
        font-style: italic;
        text-align: center;
        color: #8a7050;
        font-size: 1rem;
        margin-bottom: 1rem;
    }

    .settings-panel {
        background: linear-gradient(135deg,
            rgba(30, 20, 5, 0.9) 0%,
            rgba(25, 15, 3, 0.95) 100%);
        border: 1px solid rgba(201, 168, 76, 0.2);
        border-radius: 4px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .result-panel {
        background: linear-gradient(135deg,
            rgba(35, 23, 7, 0.9) 0%,
            rgba(25, 15, 3, 0.95) 100%);
        border: 1px solid rgba(201, 168, 76, 0.3);
        border-radius: 4px;
        padding: 2.5rem;
        text-align: center;
        box-shadow:
            0 8px 40px rgba(0,0,0,0.6),
            0 0 80px rgba(201, 168, 76, 0.05);
    }

    .quote-box {
        border-left: 2px solid #c9a84c;
        padding: 1rem 1.5rem;
        margin: 2rem auto;
        max-width: 600px;
        opacity: 0.7;
    }

    .quote-text {
        font-family: 'IM Fell English', serif;
        font-style: italic;
        font-size: 1.1rem;
        color: #b8986a;
        text-align: center;
    }

    .quote-author {
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.9rem;
        color: #8a7050;
        text-align: center;
        margin-top: 0.5rem;
        letter-spacing: 0.15rem;
    }

    footer-text {
        text-align: center;
        color: #5a4a30;
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(201, 168, 76, 0.1);
    }

    [data-testid="stButton"] button {
        background: linear-gradient(135deg, #8b6914 0%, #c9a84c 50%, #8b6914 100%) !important;
        color: #1a1209 !important;
        border: none !important;
        border-radius: 2px !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.2rem !important;
        padding: 0.9rem 2rem !important;
        text-transform: uppercase !important;
        transition: all 0.4s ease !important;
        box-shadow:
            0 4px 20px rgba(139, 105, 20, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    [data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow:
            0 8px 30px rgba(201, 168, 76, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    [data-testid="stButton"] button:active {
        transform: translateY(0) !important;
    }

    [data-testid="stSlider"] {
        padding: 0.5rem 0;
    }

    [data-testid="stSlider"] label {
        font-family: 'Cormorant Garamond', serif !important;
        color: #b8986a !important;
        font-size: 1rem !important;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #8b6914, #c9a84c) !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(201, 168, 76, 0.05) !important;
        border: 1px dashed rgba(201, 168, 76, 0.3) !important;
        border-radius: 4px !important;
    }

    [data-testid="stFileUploader"] label {
        color: #b8986a !important;
        font-family: 'Cormorant Garamond', serif !important;
    }

    [data-testid="stImage"] img {
        border: 1px solid rgba(201, 168, 76, 0.2) !important;
        border-radius: 2px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #f0d080 !important;
    }

    p, label {
        font-family: 'Cormorant Garamond', serif !important;
        color: #b8986a !important;
    }

    .stSelectbox label {
        color: #b8986a !important;
        font-family: 'Cormorant Garamond', serif !important;
    }

    [data-testid="stDownloadButton"] button {
        background: transparent !important;
        color: #c9a84c !important;
        border: 1px solid rgba(201, 168, 76, 0.4) !important;
        border-radius: 2px !important;
        font-family: 'Cormorant Garamond', serif !important;
        letter-spacing: 0.1rem !important;
    }

    [data-testid="stDownloadButton"] button:hover {
        background: rgba(201, 168, 76, 0.1) !important;
        border-color: #c9a84c !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<div class='header-ornament'>✦ ✦ ✦</div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>Picass<span>ify</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Neural Artistry — Where Intelligence Meets the Canvas</p>", unsafe_allow_html=True)
st.markdown("<div class='divider'>⬧</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='quote-box'>
        <p class='quote-text'>"Every artist dips his brush in his own soul,<br>and paints his own nature into his pictures."</p>
        <p class='quote-author'>— Henry Ward Beecher</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'>⬧</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'><span>I.</span> The Subject</h2>", unsafe_allow_html=True)
    st.markdown("<p class='instruction-text'>Upload the photograph to be transformed</p>", unsafe_allow_html=True)
    content_file = st.file_uploader(
        "Content Image",
        type=["jpg", "jpeg", "png"],
        key="content",
        label_visibility="collapsed"
    )
    if content_file:
        st.image(content_file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'><span>II.</span> The Muse</h2>", unsafe_allow_html=True)
    st.markdown("<p class='instruction-text'>Upload the painting whose soul shall be borrowed</p>", unsafe_allow_html=True)
    style_file = st.file_uploader(
        "Style Image",
        type=["jpg", "jpeg", "png"],
        key="style",
        label_visibility="collapsed"
    )
    if style_file:
        st.image(style_file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'>⬧</div>", unsafe_allow_html=True)

st.markdown("<div class='settings-panel'>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'><span>III.</span> The Alchemy</h2>", unsafe_allow_html=True)
st.markdown("<p class='instruction-text'>Adjust the parameters of artistic transmutation</p>", unsafe_allow_html=True)

set_col1, set_col2, set_col3 = st.columns(3)

with set_col1:
    steps = st.slider(
        "Iterations of Refinement",
        min_value=100,
        max_value=600,
        value=300,
        step=50,
        help="More iterations = more stylized result (but slower)"
    )

with set_col2:
    style_weight = st.select_slider(
        "Strength of Style",
        options=[100000, 500000, 1000000, 5000000, 10000000],
        value=1000000,
        format_func=lambda x: {
            100000: "Subtle",
            500000: "Moderate",
            1000000: "Strong",
            5000000: "Intense",
            10000000: "Overwhelming"
        }[x],
        help="Controls how strongly the painting's style is applied"
    )

with set_col3:
    image_size = st.select_slider(
        "Canvas Resolution",
        options=[256, 384, 512],
        value=256,
        format_func=lambda x: {
            256: "256 × 256",
            384: "384 × 384",
            512: "512 × 512"
        }[x],
        help="Higher resolution = better quality but much slower on CPU"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'>⬧</div>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    generate_btn = st.button("✦  Begin the Transformation  ✦", use_container_width=True)

if generate_btn:
    if not content_file or not style_file:
        st.warning("Please upload both a content image and a style image to proceed.")
    else:
        st.markdown("<div class='divider'>⬧</div>", unsafe_allow_html=True)
        st.markdown("<div class='result-panel'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'><span>IV.</span> The Masterpiece Emerges</h2>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_text  = st.empty()

        def progress_callback(step, total, total_loss, c_loss, s_loss):
            progress = step / total
            progress_bar.progress(progress)
            status_text.markdown(
                f"<p style='text-align:center; font-family: IM Fell English, serif; "
                f"font-style:italic; color:#8a7050;'>"
                f"Refining... Step {step} of {total} &nbsp;|&nbsp; "
                f"Loss: {total_loss:.2f}</p>",
                unsafe_allow_html=True
            )

        with st.spinner("The canvas is being painted..."):
            content_tensor = load_image_from_upload(content_file, size=image_size)
            style_tensor   = load_image_from_upload(style_file,   size=image_size)

            generated = run_style_transfer(
                content_tensor,
                style_tensor,
                steps=steps,
                content_weight=1,
                style_weight=style_weight,
                progress_callback=progress_callback
            )

        progress_bar.empty()
        status_text.empty()

        result_image = tensor_to_image(generated)

        st.markdown("<br>", unsafe_allow_html=True)
        st.image(result_image, caption="Your Generated Artwork", use_container_width=True)

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        buf.seek(0)

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Save Your Masterpiece",
            data=buf,
            file_name="picassify_artwork.png",
            mime="image/png",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'>⬧</div>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align:center; padding: 2rem 0;'>
        <p style='font-family: IM Fell English, serif; font-style:italic;
                  color:#5a4a30; font-size:0.95rem; letter-spacing:0.05rem;'>
            Picassify — Built by Ali Faraz &nbsp;✦&nbsp; Powered by PyTorch & VGG19
        </p>
        <p style='font-family: Cormorant Garamond, serif; color:#3a2a10;
                  font-size:0.85rem; margin-top:0.5rem;'>
            Neural Style Transfer · Gatys et al. 2015
        </p>
    </div>
""", unsafe_allow_html=True)