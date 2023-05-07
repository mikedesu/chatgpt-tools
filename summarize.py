import yt_dlp
import webvtt
import sys



# URL of the YouTube video to download subtitles for
video_url = sys.argv[1]

# Create a yt-dlp options dict specifying to download the automatic captions
# as a .vtt file
options = {
    'writesubtitles': True,
    'subtitleslangs': ['auto'],
    'subtitlesformat': 'vtt',
	'outtmpl': '%(title)s.%(ext)s',
    'bandwidth': '1000000'
}

# Create a yt-dlp instance with our options
ydl = yt_dlp.YoutubeDL(options)

# Download the subtitles
ydl.download([video_url])


# Open the .vtt file and read its contents
#with open('example.vtt', 'r') as f:
#    vtt_data = f.read()

# Parse the .vtt data using the webvtt library
#parsed_captions = webvtt.read_buffer(vtt_data)

# Extract the text contents of each caption
#captions_text = [caption.text.strip() for caption in parsed_captions]

# Join the text contents into a single string
#plaintext = '\n'.join(captions_text)

# Print the plaintext subtitles
#print(plaintext)

