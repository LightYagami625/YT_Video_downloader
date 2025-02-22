from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["videoUrl"]
        try:
            filename = download_video(video_url)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run(debug=True)