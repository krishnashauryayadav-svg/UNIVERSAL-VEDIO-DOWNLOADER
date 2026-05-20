from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('video_url')
    # Download folder path (Desktop par 'MyDownloads' folder)
    download_path = os.path.join(os.path.expanduser("~"), "Desktop", "MyDownloads")
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{download_path}/%(title,video)s.%(ext)s',
        'restrictfilenames': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return render_template('index.html', msg="Download Successful! Check your Desktop.")
    except Exception as e:
        return render_template('index.html', msg=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
