from django.shortcuts import render
from .models import SNote, SComment, UserAccount
from django.views import generic
from django.http import HttpResponse
from .forms import NoteForm

# Create your views here.

class IndexView(generic.ListView):
    context_object_name = 'notes_list'
    template_name = "notes/index.html"
    def get_queryset(self):
        return SNote.objects.all()

def add(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            nn = form.save()
    else:
        form = NoteForm(request.POST)
    context = {'form': form}
    return render(request,'notes/add.html', context)


def index(request):
    return render(request, 'notes/index.html')


