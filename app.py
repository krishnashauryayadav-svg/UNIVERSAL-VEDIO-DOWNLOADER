from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
import os
import glob

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('video_url')
    
    # Render cloud server friendly temporary path
    download_path = "/tmp/MyDownloads"
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'quiet': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }        
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        if os.path.exists(filename):
            
            # 🔥 YAHA HAI ASLI JADU (Memory-Saver Setup):
            # Yeh decorator Flask ko bolta hai ki response send karne ke baad yeh function chalao
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(filename)
                    print(f"🔥 Successfully deleted from server to save space: {filename}")
                except Exception as error:
                    print(f"Error deleting file: {error}")
                return response

            # Video user ke device par bhejo (iske bhejte hi upar wala remove_file chal jayega)
            return send_file(filename, as_attachment=True)
        else:
            return render_template('index.html', msg="Error: Video processing failed or URL is invalid.")
            
    except Exception as e:
        return render_template('index.html', msg=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
