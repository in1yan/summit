import google.generativeai as ai
from pytube import YouTube
import yt_dlp
import requests
from fake_useragent import UserAgent
from dotenv import load_dotenv
import os


load_dotenv()
ua = UserAgent()
def web(url):
    headers = {
        'User-Agent':ua.random
    }
    res = requests.get(url, headers=headers)
    data = {
            "src":"web",
            "content":res.text
            }
    return data
def summarize(data,task):
    ai.configure(api_key=os.getenv("GEN_KEY"))

    model = ai.GenerativeModel('gemini-1.5-flash')
    base_dir = os.path.dirname(__file__)
    if task == 'summary':
        file_name = "video.md" if data['src']=='vid' else "article.md" 
        file_path = os.path.join(base_dir,"prompts",file_name)
    elif task == 'wisdom':
        file_path = os.path.join(base_dir, "prompts", "wisdom.md")
    elif task == 'idea':
        file_path = os.path.join(base_dir, "prompts", "idea.md")
    file = open(file_path)
    prompt = file.read()
    res = model.generate_content(prompt+data['content'])
    return res.text

def auto_subs(video_url, language='en'):
    ydl_opts = {
        'cookiefile':'yt.txt',
        'subtitleslangs': [language],  # Language of the auto-generated subtitles (e.g., 'en' for English)
        'subtitlesformat': 'srt',  # Format of the subtitles (can be 'vtt' or 'srt')
        'skip_download': True,  # Only download subtitles, not the video
        'writeautomaticsub':True,
        # 'outtmpl': '%(title)s.%(ext)s',  # Output file template
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        print(info['automatic_captions']['en'])
        subs = info['automatic_captions']['en'][5]['url']
        subs = requests.get(subs)
        return subs.text
def transcript(url):
    # formatter = SRTFormatter()
    video = YouTube(url)
    # id = video.video_id
    # thumbnail = video.thumbnail_url
    # title = video.title
    # raw_transcript = YouTubeTranscriptApi.get_transcript(id, proxies={"http":"http://65.52.174.95:3128"})
    transcript = auto_subs(url)
    data = {
        "src":"vid",
        # "title":title,
        # "thumbnail":thumbnail,
        "content":transcript
    }
    return data
if __name__ == '__main__':
    # res = transcript('https://www.youtube.com/watch?v=Xly7lpTQELI')
    web_res = web("https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/")
    print(summarize(web_res))
