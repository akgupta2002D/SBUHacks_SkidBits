import json
from django.views.decorators.http import require_POST
from typing import List
from punctuators.models import PunctCapSegModelONNX
from moviepy.video.io import VideoFileClip
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import VideoForm
from .models import Video, VideoAnalysis
from moviepy.editor import VideoFileClip
import speech_recognition as sr
# Create your views here.
from openai import OpenAI
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import openai


def homepage(request):
    return render(request, "mainpage/landing.html")


def webcam_page(request):
    # This view simply renders the template with the webcam recording functionality.
    return render(request, 'mainpage/webcam_page.html')


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            # Redirect to the view_video URL with the video's ID
            return redirect(reverse('show_video', kwargs={'video_id': video.id}))
    else:
        form = VideoForm()
    return render(request, 'mainpage/main_page.html', {'form': form})

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


# m = PunctCapSegModelONNX.from_pretrained("pcs_en")


# def punctuator(text):
#     input_texts = [text]
#     results = m.infer(input_texts)
#     punctuated_texts = []
#     for _, output_texts in zip(input_texts, results):
#         for text in output_texts:
#             punctuated_texts.append(text)
#     return ' '.join(punctuated_texts)

def openAI_puntuator(text):

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an amazing text editor. Add punctuation and capitalization to the following text "
            },
            {
                "role": "user",
                "content": text  # Use the submitted transcription as input
            }
        ]
    )

    punctuated_text = completion.choices[0].message.content
    return punctuated_text


def show_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'mainpage/show_video.html', {'video': video})


def view_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_path = video.video.path
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    extract_audio(video_path, audio_path)
    text = audio_to_text(audio_path)
    # Punctuate and capitalize the transcribed text
    punctuated_text = openAI_puntuator(text)

    return JsonResponse({'transcription': punctuated_text})


# def analyze_transcription(request, video_id):
#     if request.method == "POST":
#         video = get_object_or_404(Video, id=video_id)

#         # Use the submitted transcription text
#         text = request.POST.get('transcription_text', '')

#         client = OpenAI(api_key=settings.OPENAI_API_KEY)

#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are an analytical assistant designed to provide brief, actionable feedback on public speeches. Analyze the transcript for clarity, filler word usage, and effectiveness. Provide feedback in less than 10 bullet points, highlighting specific sentences for clarity issues, counting filler words, and calculating the filler word ratio. Directly reference the transcript for examples."
#                 },
#                 {
#                     "role": "user",
#                     "content": text  # Use the submitted transcription as input
#                 }
#             ]
#         )

#         analysis_result = completion.choices[0].message.content
#         # We are also saving it to database.
#         VideoAnalysis.objects.create(
#             video=video, analysis_text=analysis_result)

#         return render(request, 'mainpage/analysis_result.html', {
#             'video': video,
#             'analysis_result': analysis_result
#         })

#     # If not POST, redirect to the video page or another appropriate action
#     return HttpResponse("Invalid request", status=400)


# To show the data of analysis for the video.
def view_analysis_results(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    # Get all analyses for this video, newest first
    analyses = video.analyses.all().order_by('-created_at')

    return render(request, 'mainpage/view_analysis_results.html', {
        'video': video,
        'analyses': analyses
    })


@require_POST
def analyze_transcription(request, video_id):
    # Ensure the request content type is application/json
    if request.headers.get('Content-Type') == 'application/json':
        data = json.loads(request.body)
        text = data.get('transcription_text', '')
    else:
        return HttpResponseBadRequest("Invalid request format, expected JSON")

    try:
        video = get_object_or_404(Video, id=video_id)
        openai.api_key = settings.OPENAI_API_KEY

        # Using the specified "gpt-3.5-turbo" model and the provided prompt structure
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an analytical assistant designed to provide brief, actionable feedback on public speeches. Analyze the transcript for clarity, filler word usage, and effectiveness. Provide feedback in less than 10 bullet points, highlighting specific sentences for clarity issues, counting filler words, and calculating the filler word ratio. Directly reference the transcript for examples."
                },
                {
                    "role": "user",
                    "content": text  # The transcription text submitted for analysis
                }
            ]
        )

        # Adjust based on the actual structure of the OpenAI response
        analysis_result = completion.choices[0].message.content
        VideoAnalysis.objects.create(
            video=video, analysis_text=analysis_result)

        return JsonResponse({'analysis_result': analysis_result})
    except Exception as e:
        # Returning a 400 error with a description of what went wrong
        return HttpResponseBadRequest(f"Error processing analysis: {str(e)}")
