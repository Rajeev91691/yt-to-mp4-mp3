from flask import Flask, render_template, request, send_file
import os
import re
import yt_dlp as youtube_dl

app = Flask(__name__)

# Function to sanitize filenames for Windows
def sanitize_filename(filename):
    # Remove invalid characters including full-width vertical bar
    return re.sub(r'[\\/*?:"<>|｜]', "", filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    format_choice = request.form['format']

    try:
        # Create downloads folder
        out_dir = r"C:\Users\Rajeev\Desktop"
        os.makedirs(out_dir, exist_ok=True)

        # Base yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'forceipv4': True,   # avoids network issues
        }

        if format_choice == "mp3":
            # Download audio only
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            # Download high-quality video + audio and merge into MP4
            ydl_opts.update({
                'format': 'best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            ext = "mp3" if format_choice == "mp3" else "mp4"
            # Sanitize filename for Windows
            filename = os.path.join(out_dir, f"{sanitize_filename(title)}.{ext}")

        return send_file(os.path.abspath(filename), as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
