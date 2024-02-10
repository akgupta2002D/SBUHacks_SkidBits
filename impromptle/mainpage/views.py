from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import VideoForm
from .models import Video

# Create your views here.


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


def view_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    # You can now pass the video object to your template or process it further
    return render(request, 'mainpage/view_video.html', {'video': video})
