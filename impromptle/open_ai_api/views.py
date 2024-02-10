# open_ai/views.py
from django.shortcuts import render
# Ensure this is updated to use the new OpenAI client
from .utils import ask_openai


def openai_form(request):
    context = {}
    if request.method == "POST":
        prompt = request.POST.get('prompt', '')
        response = ask_openai(prompt)
        context = {'response': response, 'prompt': prompt}
    return render(request, 'open_ai_api/form.html', context)
