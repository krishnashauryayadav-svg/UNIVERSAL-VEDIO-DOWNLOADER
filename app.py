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
        'ignoreerrors': True,
        'no_warnings': True,
        'quite': True,
        'http_hedders':{
               'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Wine64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
               'Accept-': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language':'en-US,en;q=0.5,
        }
        'extractor_args':{
                'youtube':{
                      'player_client':['android','web']
                }
    }
    }

          
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return render_template('index.html', msg="Download Successful! Check your Desktop.")
    except Exception as e:
        return render_template('index.html', msg=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
