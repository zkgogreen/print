from django.shortcuts import render, get_object_or_404, redirect
from .models import Main, FieldMenu
from .forms import MainForm, FieldMenuForm
# Create your views here.


def index(request):
    if request.method == 'POST':
        Main.objects.all().update(utama=False)
        Main.objects.filter(id=request.POST['id']).update(utama=True)
    context = {
        'datas':Main.objects.all()
    }
    return render(request, 'index.html', context)

def edit(request, id):
    instance = get_object_or_404(Main, pk=id)
    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('index:index')
    context = {
        'form':MainForm(instance=instance),
        'data':instance,
        'datas':FieldMenu.objects.filter(main=instance)
    }
    return render(request, 'edit.html', context)

def add(request):
    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            FieldMenu.objects.create(main_id=new_form.id,nama='jumlah',urutan=14)
            FieldMenu.objects.create(main_id=new_form.id,nama='rasa',urutan=6)
            FieldMenu.objects.create(main_id=new_form.id,nama='varian',urutan=5)
            FieldMenu.objects.create(main_id=new_form.id,nama='harga',urutan=15)
            return redirect('index:index')
    return render(request, 'edit.html', {'form':MainForm})

def deleteSub(request, id):
    return redirect('index:edit')

def editSub(request, id):
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'edit':
            FieldMenu.objects.filter(id=request.POST['id']).update(urutan=request.POST['urutan'], nama=request.POST['nama'])
        else:
            FieldMenu.objects.filter(id=request.POST['id']).delete()
    return redirect('index:edit', id=id)

def addSub(request, id):
    if request.method == 'POST':
        FieldMenu.objects.create(main_id=id, urutan=request.POST['urutan'], nama=request.POST['nama'])
        return redirect('index:edit', id=id)