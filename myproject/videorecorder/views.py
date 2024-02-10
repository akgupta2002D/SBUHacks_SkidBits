from django.shortcuts import render

def record_video(request):
    return render(request, 'videorecorder/record_video.html')