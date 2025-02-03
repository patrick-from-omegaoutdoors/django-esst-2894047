from .models import Notes
from .forms import NotesForm

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView,
)

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = "/admin"

    def get_queryset(self):
        return self.request.user.notes.all()


class PopularNotesListView(ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    queryset = Notes.objects.filter(likes__gte=1)


class NotesDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    context_object_name = "note"


class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Notes
    form_class = NotesForm
    success_url = '/smart/notes'

    def form_valid(self, form) -> HttpResponseRedirect:
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    form_class = NotesForm
    success_url = '/smart/notes'


class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'


def add_like_view(request, pk) -> HttpResponseRedirect | Http404:
    if request.method == 'POST':
        note = get_object_or_404(Notes, pk=pk)
        note.likes += 1
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    
    raise Http404

def chagne_visability_view(request, pk) -> HttpResponseRedirect | Http404:
    if request.method == 'POST':
        note = get_object_or_404(Notes, pk=pk)
        note.is_public = not note.is_public
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    
    raise Http404