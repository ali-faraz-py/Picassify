import streamlit as st
from PIL import Image
import io
import torch

from utils import load_image_from_upload, tensor_to_image
from style_transfer import run_style_transfer

st.set_page_config(
    page_title="PICASSIFY",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Barlow+Condensed:wght@300;400;600;800;900&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d0d0d;
        background-image:
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        font-family: 'Space Mono', monospace;
        color: #f0f0f0;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 0;
        max-width: 100%;
    }

    .hero {
        background: #0d0d0d;
        border-bottom: 4px solid #ff2d00;
        padding: 3rem 4rem 2rem 4rem;
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: 'ART';
        position: absolute;
        right: -2rem;
        top: -2rem;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 18rem;
        color: rgba(255, 45, 0, 0.04);
        line-height: 1;
        pointer-events: none;
        user-select: none;
    }

    .issue-tag {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: #ff2d00;
        letter-spacing: 0.3rem;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        border-left: 3px solid #ff2d00;
        padding-left: 0.8rem;
    }

    .main-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 10rem;
        color: #f0f0f0;
        line-height: 0.85;
        letter-spacing: 0.05rem;
        margin-bottom: 0.5rem;
    }

    .main-title span {
        color: #ff2d00;
        display: block;
    }

    .tagline {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 300;
        font-size: 1.3rem;
        color: #888;
        letter-spacing: 0.2rem;
        text-transform: uppercase;
        margin-top: 0.5rem;
        border-top: 1px solid #333;
        padding-top: 1rem;
        max-width: 600px;
    }

    .content-wrap {
        padding: 3rem 4rem;
    }

    .section-label {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #ff2d00;
        letter-spacing: 0.4rem;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: #333;
    }

    .upload-block {
        border: 2px solid #222;
        padding: 0;
        position: relative;
        background: #111;
        transition: border-color 0.2s;
    }

    .upload-block:hover {
        border-color: #ff2d00;
    }

    .upload-header {
        background: #1a1a1a;
        border-bottom: 1px solid #222;
        padding: 0.8rem 1.2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .upload-num {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3rem;
        color: #ff2d00;
        line-height: 1;
    }

    .upload-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 800;
        font-size: 1.4rem;
        letter-spacing: 0.15rem;
        color: #f0f0f0;
        text-transform: uppercase;
    }

    .upload-desc {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
    }

    .upload-inner {
        padding: 1.5rem;
    }

    .settings-bar {
        background: #111;
        border: 2px solid #222;
        border-left: 4px solid #ff2d00;
        padding: 2rem;
        margin: 2.5rem 0;
    }

    .settings-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2rem;
        color: #f0f0f0;
        letter-spacing: 0.1rem;
        margin-bottom: 0.3rem;
    }

    .settings-sub {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #555;
        letter-spacing: 0.2rem;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }


    .result-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3rem;
        color: #f0f0f0;
        text-align: center;
        letter-spacing: 0.2rem;
        margin-bottom: 1.5rem;
    }

    .ticker {
        background: #ff2d00;
        padding: 0.4rem 4rem;
        overflow: hidden;
        white-space: nowrap;
        margin: 2rem 0;
    }

    .ticker-text {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.3rem;
        color: #0d0d0d;
        text-transform: uppercase;
        animation: ticker 20s linear infinite;
        display: inline-block;
    }

    @keyframes ticker {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }

    .footer-bar {
        background: #111;
        border-top: 4px solid #ff2d00;
        padding: 1.5rem 4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 4rem;
    }

    .footer-left {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.5rem;
        color: #f0f0f0;
        letter-spacing: 0.2rem;
    }

    .footer-right {
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        color: #555;
        text-align: right;
        letter-spacing: 0.1rem;
    }

    [data-testid="stButton"] button {
        background: #ff2d00 !important;
        color: #0d0d0d !important;
        border: none !important;
        border-radius: 0 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 1.5rem !important;
        letter-spacing: 0.3rem !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
    }

    [data-testid="stButton"] button:hover {
        background: #f0f0f0 !important;
        transform: translateY(-3px) !important;
        box-shadow: 6px 6px 0px #ff2d00 !important;
    }

    [data-testid="stButton"] button:active {
        transform: translateY(0) !important;
        box-shadow: none !important;
    }

    [data-testid="stDownloadButton"] button {
        background: transparent !important;
        color: #ff2d00 !important;
        border: 2px solid #ff2d00 !important;
        border-radius: 0 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.2rem !important;
        transition: all 0.2s !important;
    }

    [data-testid="stDownloadButton"] button:hover {
        background: #ff2d00 !important;
        color: #0d0d0d !important;
        box-shadow: 4px 4px 0px #ffffff !important;
    }

    [data-testid="stSlider"] label p {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.7rem !important;
        color: #888 !important;
        letter-spacing: 0.15rem !important;
        text-transform: uppercase !important;
    }

    [data-testid="stFileUploader"] {
        background: transparent !important;
    }

    [data-testid="stFileUploader"] label {
        color: #555 !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.7rem !important;
    }

    [data-testid="stImage"] img {
        border: 1px solid #222 !important;
    }

    .stProgress > div > div {
        background: #ff2d00 !important;
        border-radius: 0 !important;
    }

    .stProgress > div {
        background: #1a1a1a !important;
        border-radius: 0 !important;
    }

    div[data-testid="stSelectSlider"] label p {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.7rem !important;
        color: #888 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='hero'>
        <div class='issue-tag'>Neural Style Transfer Engine · Vol. 01</div>
        <div class='main-title'>
            PICASS
            <span>IFY</span>
        </div>
        <div class='tagline'>Upload. Transmute. Collect your Masterpiece.</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='ticker'>
        <span class='ticker-text'>
            NEURAL STYLE TRANSFER &nbsp;·&nbsp; VGG19 ARCHITECTURE &nbsp;·&nbsp;
            GRAM MATRIX &nbsp;·&nbsp; CONTENT LOSS &nbsp;·&nbsp; STYLE LOSS &nbsp;·&nbsp;
            PYTORCH ENGINE &nbsp;·&nbsp; UPLOAD YOUR PHOTO &nbsp;·&nbsp;
            CHOOSE YOUR STYLE &nbsp;·&nbsp; GENERATE ART &nbsp;·&nbsp;
            NEURAL STYLE TRANSFER &nbsp;·&nbsp; VGG19 ARCHITECTURE &nbsp;·&nbsp;
            GRAM MATRIX &nbsp;·&nbsp; CONTENT LOSS &nbsp;·&nbsp; STYLE LOSS &nbsp;·&nbsp;
            PYTORCH ENGINE &nbsp;·&nbsp; UPLOAD YOUR PHOTO &nbsp;·&nbsp;
            CHOOSE YOUR STYLE &nbsp;·&nbsp; GENERATE ART &nbsp;·&nbsp;
        </span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='content-wrap'>", unsafe_allow_html=True)

st.markdown("<div class='section-label'>01 — Input</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
        <div class='upload-block'>
            <div class='upload-header'>
                <div>
                    <div class='upload-label'>The Subject</div>
                    <div class='upload-desc'>Your photograph</div>
                </div>
                <div class='upload-num'>01</div>
            </div>
            <div class='upload-inner'>
    """, unsafe_allow_html=True)
    content_file = st.file_uploader(
        "Upload content image",
        type=["jpg", "jpeg", "png"],
        key="content",
        label_visibility="collapsed"
    )
    if content_file:
        st.image(content_file, use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='upload-block'>
            <div class='upload-header'>
                <div>
                    <div class='upload-label'>The Style</div>
                    <div class='upload-desc'>Your painting / artwork</div>
                </div>
                <div class='upload-num'>02</div>
            </div>
            <div class='upload-inner'>
    """, unsafe_allow_html=True)
    style_file = st.file_uploader(
        "Upload style image",
        type=["jpg", "jpeg", "png"],
        key="style",
        label_visibility="collapsed"
    )
    if style_file:
        st.image(style_file, use_container_width=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='settings-bar'>
        <div class='settings-title'>Parameters</div>
        <div class='settings-sub'>Configure the style transfer engine</div>
""", unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)

with s1:
    steps = st.slider(
        "ITERATIONS",
        min_value=100,
        max_value=600,
        value=150,
        step=50
    )

with s2:
    style_weight = st.select_slider(
        "STYLE STRENGTH",
        options=[100000, 500000, 1000000, 5000000, 10000000],
        value=1000000,
        format_func=lambda x: {
            100000:   "Subtle",
            500000:   "Moderate",
            1000000:  "Strong",
            5000000:  "Intense",
            10000000: "Max"
        }[x]
    )

with s3:
    image_size = st.select_slider(
        "CANVAS SIZE",
        options=[128, 192, 256],
        value=192,
        format_func=lambda x: f"{x} × {x}"
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-label'>02 — Generate</div>", unsafe_allow_html=True)

generate_btn = st.button("EXECUTE STYLE TRANSFER", use_container_width=True)

if generate_btn:
    if not content_file or not style_file:
        st.error("ERROR — Both images required to proceed.")
    else:
        st.markdown("<div class='result-title'>GENERATING ARTWORK</div>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_text  = st.empty()

        def progress_callback(step, total, total_loss, c_loss, s_loss):
            progress_bar.progress(step / total)
            status_text.markdown(
                f"<p style='font-family: Space Mono, monospace; font-size: 0.7rem;"
                f"color: #555; letter-spacing: 0.15rem; text-transform: uppercase;'>"
                f"STEP {step}/{total} &nbsp;·&nbsp; LOSS: {total_loss:.2f}</p>",
                unsafe_allow_html=True
            )

        with st.spinner(""):
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

        st.markdown("<div class='section-label'>03 — Output</div>", unsafe_allow_html=True)
        st.image(result_image, caption="GENERATED ARTWORK", use_container_width=True)

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        buf.seek(0)

        st.download_button(
            label="DOWNLOAD ARTWORK",
            data=buf,
            file_name="picassify_artwork.png",
            mime="image/png",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='footer-bar'>
        <div class='footer-left'>PICASSIFY</div>
        <div class='footer-right'>
            BUILT BY ALI FARAZ<br>
            PYTORCH · VGG19 · STREAMLIT<br>
            NEURAL STYLE TRANSFER · GATYS ET AL. 2015
        </div>
    </div>
""", unsafe_allow_html=True)