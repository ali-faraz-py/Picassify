# 🎨 PICASSIFY: High-Performance Neural Style Transfer Engine

A professional-grade Computer Vision dashboard built with **Python** and **Streamlit**. This tool utilizes **Neural Style Transfer (NST)** via the **VGG19** architecture to blend the content of one image with the artistic style of another, transforming digital photos into structured masterpieces.

---

## 🚀 Live Demo
**[Click here to try the Live App](https://picassify-art.streamlit.app/)**

---

## 📺 Demo Preview
![Picassify Demo](assets\Picassify.gif)

---

## ✨ Features
- **Neural Style Transfer:** Implements the landmark Gatys et al. algorithm to decouple and recombine content and style representations.
- **VGG19 Feature Extraction:** Leverages a pre-trained 19-layer Convolutional Neural Network (CNN) to capture deep hierarchical features of artistic brushstrokes.
- **Customizable Hyperparameters:** Real-time control over style-to-content weight ratios and optimization steps for granular artistic control.
- **Automated Preprocessing:** Intelligent image resizing and ImageNet-standard normalization pipeline (Mean/Std-dev correction).
- **Interactive UI:** A dark-themed, industrial dashboard designed for high-speed local or cloud-based artistic inference.

---

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **Framework:** Streamlit (Web UI)
- **Deep Learning Engine:** PyTorch / Torchvision
- **Architecture:** VGG19 (Deep Feature Extractor)
- **Optimization:** Adam Optimizer
- **Image Processing:** Pillow & NumPy

---

## 🚀 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ali-faraz-py/Picassify.git](https://github.com/ali-faraz-py/Picassify.git)
   cd Picassify

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Run the application:**
    ```bash
    streamlit run app.py

---

## 📂 Project Structure
```text
picassify/
├── app.py              # Streamlit Web UI and visualization logic
├── style_transfer.py   # Core NST engine and VGG19 feature extraction
├── utils.py            # Image processing, normalization, and tensor conversion
├── requirements.txt    # Project dependencies (PyTorch, Streamlit, etc.)
├── .gitattributes      # GitHub language statistics and configuration
├── .gitignore          # Prevents tracking of __pycache__ and local assets
└── README.md           # Project documentation
```

---

## 🧠 Model Insights 
The engine utilizes a **VGG19 (Visual Geometry Group)** network, a powerhouse for feature representation in Computer Vision.

* **The Architecture:** The model treats style as a mathematical distribution of features. By calculating the **Gram Matrix** of specific layers, Picassify captures the texture and color patterns of the style image.

* **Loss Optimization:** The system simultaneously minimizes two loss functions: **Content Loss** (ensuring the objects remain recognizable) and **Style Loss** (ensuring the texture matches the artwork).

* **Feature Layers:** We extract content features from the deeper conv4_2 layer and style features from multiple layers (conv1_1 through conv5_1) to capture both fine detail and global artistic structure.

---

### 👤 Author
**Syed Ali Faraz** - [GitHub Profile](https://github.com/ali-faraz-py)

*If you found this NLP pipeline useful, please give the repository a ⭐!*