import whisper
import os
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

# FFmpeg path configuration
os.environ["PATH"] += os.pathsep + r"C:\Users\bhard\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"

def translate_video(video_path: str, output_path: str = "output_dubbed.mp4") -> str:
    """
    Automatically translates a Hindi video to English dubbed video.
    
    Args:
        video_path: Path to the input Hindi video file
        output_path: Path where the dubbed video will be saved
    
    Returns:
        Path to the output dubbed video file
    """
    
    print("Step 1: Extracting audio from video...")
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)

    print("Step 2: Transcribing Hindi audio to text...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="hi")
    hindi_text = result["text"]
    print(f"  Transcribed text: {hindi_text[:80]}...")

    print("Step 3: Translating Hindi text to English...")
    translator = GoogleTranslator(source="hi", target="en")
    chunks = [hindi_text[i:i+4500] for i in range(0, len(hindi_text), 4500)]
    english_text = " ".join([translator.translate(chunk) for chunk in chunks])
    print(f"  Translated text: {english_text[:80]}...")

    print("Step 4: Converting English text to speech...")
    dubbed_audio_path = "temp_dubbed_audio.mp3"
    tts = gTTS(text=english_text, lang="en", slow=False)
    tts.save(dubbed_audio_path)

    print("Step 5: Merging dubbed audio with video...")
    dubbed_audio = AudioFileClip(dubbed_audio_path)
    final_video = video.set_audio(dubbed_audio)
    final_video.write_videofile(output_path, verbose=False, logger=None)

    # Cleanup temporary files
    os.remove(audio_path)
    os.remove(dubbed_audio_path)
    video.close()

    print(f"\nSuccess! Dubbed video saved at: {output_path}")
    
    # Automatically open the output video
    os.startfile(output_path)
    
    return output_path


if __name__ == "__main__":
    VIDEO_FILE = "videoplayback.mp4"
    translate_video(VIDEO_FILE)
