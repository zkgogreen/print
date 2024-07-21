from django.shortcuts import render
from .models import Main
from .forms import MainForm
# Create your views here.


def index(request):
    instance = Main.objects.all().first()
    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
    context = {
        'form':MainForm(instance=instance),
        'data':instance
    }
    return render(request, 'index.html', context)