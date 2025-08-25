import gradio as gr
import yt_dlp
import os
import json

# Paths
OUTPUT_DIR = "output"
COOKIES_DIR = "cookies"
COOKIES_PATH = os.path.join(COOKIES_DIR, "cookies.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(COOKIES_DIR, exist_ok=True)

# Convert JSON cookies to Netscape format
def convert_cookies(json_file, output_file):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for cookie in cookies:
                domain = cookie.get("domain", "")
                flag = "TRUE" if domain.startswith(".") else "FALSE"
                path = cookie.get("path", "/")
                secure = "TRUE" if cookie.get("secure", False) else "FALSE"
                expiration = str(int(cookie.get("expirationDate", 1893456000)))
                name = cookie.get("name", "")
                value = cookie.get("value", "")
                f.write("\t".join([domain, flag, path, secure, expiration, name, value]) + "\n")
        return True, "✅ Cookies converted successfully."
    except Exception as e:
        return False, f"❌ Error converting cookies: {str(e)}"

# Upload cookies
def upload_cookies(file):
    if file is None:
        return "❌ No file uploaded.", check_cookies_status()
    success, msg = convert_cookies(file.name, COOKIES_PATH)
    return msg, check_cookies_status()

# Check if cookies exist
def check_cookies_status():
    if not os.path.exists(COOKIES_PATH) or os.stat(COOKIES_PATH).st_size == 0:
        return "❌ Cookies empty"
    return "✅ Cookies loaded"

# Download MP3 with yt-dlp
def download_mp3(url):
    if not os.path.exists(COOKIES_PATH) or os.stat(COOKIES_PATH).st_size == 0:
        return "❌ Cookies empty, please upload again.", None

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
            'cookiefile': COOKIES_PATH,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(filename)[0] + ".mp3"

        return f"✅ Downloaded: {os.path.basename(mp3_path)}", mp3_path

    except Exception as e:
        err = str(e)
        if "cookies are no longer valid" in err.lower() or "sign in to confirm" in err.lower():
            return "❌ Cookies expired, please upload again.", None
        return f"❌ Error: {err}", None

# Build Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎵 YouTube to MP3 Downloader")

    # 1. YouTube input + button
    url = gr.Textbox(label="YouTube URL", placeholder="Paste YouTube link here")
    download_button = gr.Button("Download MP3")

    # 2. Audio preview
    audio_preview = gr.Audio(label="Preview", type="filepath")

    # 3. Status
    status = gr.Textbox(label="Status", interactive=False)

    # 4. Upload cookies
    cookie_upload = gr.File(label="Upload Cookies (JSON)", file_types=[".json"])

    # 5. Cookies status
    cookie_status = gr.Textbox(label="Cookies Status", value=check_cookies_status(), interactive=False)

    # Actions
    download_button.click(fn=download_mp3, inputs=url, outputs=[status, audio_preview])
    cookie_upload.upload(fn=upload_cookies, inputs=cookie_upload, outputs=[cookie_status, cookie_status])

if __name__ == "__main__":
    demo.launch()
