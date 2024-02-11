from moviepy.video.io import VideoFileClip
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import VideoForm
from .models import Video
from moviepy.editor import VideoFileClip
import speech_recognition as sr
# Create your views here.
from openai import OpenAI
from django.conf import settings
from django.http import HttpResponse


def homepage(request):
    return render(request, "mainpage/base.html")


def webcam_page(request):
    # This view simply renders the template with the webcam recording functionality.
    return render(request, 'mainpage/webcam_page.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # Redirect to the view_video URL with the video's ID
            return redirect(reverse('view_video', kwargs={'video_id': video.id}))
    else:
        form = VideoForm()
    return render(request, 'mainpage/upload_video.html', {'form': form})

# Change the function below to work with the video that we upload above.

# Assume VideoForm is imported correctly
# Assume you have functions convert_video_to_audio(video) and transcribe_audio(audio)


def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()


def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"


def view_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_path = video.video.path
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    extract_audio(video_path, audio_path)
    text = audio_to_text(audio_path)
    return render(request, 'mainpage/view_video.html', {'video': video, 'text': text})


def analyze_transcription(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)

        # Use the submitted transcription text
        text = request.POST.get('transcription_text', '')

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."
                },
                {
                    "role": "user",
                    "content": text  # Use the submitted transcription as input
                }
            ]
        )

        analysis_result = completion.choices[0].message.content

        return render(request, 'mainpage/analysis_result.html', {
            'video': video,
            'analysis_result': analysis_result
        })

    # If not POST, redirect to the video page or another appropriate action
    return HttpResponse("Invalid request", status=400)
