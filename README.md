# 🎵 YouTube to MP3 Downloader (Gradio)

A simple **YouTube to MP3 downloader** built with **Gradio** and **yt-dlp**, with support for uploading YouTube cookies for private/age-restricted content.

---

## 🚀 Features
- Paste a **YouTube URL** and download the audio as MP3.  
- **Preview audio** before downloading.  
- **Upload cookies** (JSON export from browser) to bypass age restrictions, region locks, or bot checks.  
- Automatically converts JSON cookies into the required **Netscape cookie format** for yt-dlp.  
- Shows **cookies status** (loaded ✅, empty ❌, expired ❌).  

---

## 📦 Installation

Clone the repo:

git clone https://github.com/yourusername/ytmp3-gradio.git
cd ytmp3-gradio

### Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Make sure ffmpeg is installed (required by yt-dlp):

bash
Copy
Edit
sudo apt-get install ffmpeg   # Linux (Debian/Ubuntu)
brew install ffmpeg           # macOS
▶️ Run the App
bash
Copy
Edit
python app.py
Gradio will start a local server (default: http://127.0.0.1:7860).

🔑 Using Cookies (for restricted videos)
Some YouTube videos require authentication (age-restricted, private, or region-locked).
In that case, you must export your YouTube cookies from your browser.

Follow the official yt-dlp guide here:
👉 How to export YouTube cookies

Save the cookies file as .json (e.g., cookies.json).

Upload the JSON file in the Gradio app under Upload Cookies (JSON).

The app will automatically convert it to cookies/cookies.txt (Netscape format required by yt-dlp).

If your cookies expire, re-export and upload again.

📂 Project Structure
bash
Copy
Edit
ytmp3-gradio/
│── app.py              # Main Gradio app
│── requirements.txt    # Python dependencies
│── Procfile            # For deployment (Heroku, etc.)
│── README.md           # Documentation
│── cookies/            # Folder for cookies
│   └── cookies.txt
│── output/             # Downloaded MP3 files
⚠️ Disclaimer
This project is for educational purposes only.
Downloading copyrighted content without permission may violate YouTube’s Terms of Service.
Use at your own risk.

🛠️ Tech Stack
Gradio – UI framework

yt-dlp – YouTube downloader

ffmpeg – Audio conversion
