import os
import yt_dlp
import gradio as gr

OUTPUT_DIR = "output"
COOKIES_FILE = "cookies/cookies.txt"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("cookies", exist_ok=True)

def download_audio(youtubelink, quality):
    bitrate = quality.replace("kbps", "")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{OUTPUT_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
        'quiet': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            },
            {
                'key': 'FFmpegMetadata'
            }
        ],
        'prefer_ffmpeg': True,
        'extractaudio': True,
        'cachedir': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtubelink, download=True)
            filename = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(filename)[0] + ".mp3"
        return mp3_path
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("## 🎵 YouTube to MP3 Downloader")

    with gr.Row():
        url_input = gr.Textbox(label="YouTube URL", placeholder="Paste YouTube link here...")
    
    quality_input = gr.Radio(["128kbps", "192kbps", "256kbps", "320kbps"], 
                             value="256kbps", label="Select Quality")
    
    download_btn = gr.Button("Download & Convert")

    audio_output = gr.Audio(label="Downloaded MP3", type="filepath")

    download_btn.click(fn=download_audio, 
                       inputs=[url_input, quality_input], 
                       outputs=audio_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
