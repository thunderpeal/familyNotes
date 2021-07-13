from django.shortcuts import render
from .models import SNote, SComment, UserAccount
from django.views import generic
from django.http import HttpResponse
# Create your views here.

class IndexView(generic.ListView):
    context_object_name = 'notes_list'
    template_name = "notes/index.html"
    def get_queryset(self):
        return SNote.objects.all()


def index(request):
    return render(request, 'notes/index.html')