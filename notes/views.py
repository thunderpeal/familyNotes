from django.shortcuts import render
from django.urls import reverse_lazy
from .models import SNote, SComment, CustomUser
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse

# Create your views here.

class IndexView(ListView):
    context_object_name = 'notes_list'
    template_name = "notes/index.html"
    def get_queryset(self):
        return SNote.objects.all()


class NoteAdd(CreateView):
    model = SNote
    template_name = 'notes/add.html'
    fields = '__all__'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        u = CustomUser.objects.get(login=self.request.user)
        form.instance.author = u
        return super(NoteAdd, self).form_valid(form)



def index(request):
    return render(request, 'notes/index.html')


