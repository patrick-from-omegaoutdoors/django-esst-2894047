from django.shortcuts import render
from django.http import Http404

from .models import Notes

# def list(request):
#     all_notes = Notes.objects.all()
#     return render(request, 'notes/notes_list.html', {'notes': all_notes})

# def detail(request, pk):
#     try:
#         note = Notes.objects.get(pk=pk)
#         return render(request, 'notes/notes_detail.html', {'note': note})
    
#     except Notes.DoesNotExist:
#         raise Http404("Note does not exist")
    
from django.views.generic import ListView, DetailView, CreateView

class NotesListView(ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"

class PopularNotesListView(ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    queryset = Notes.objects.filter(likes__gte=1)

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = "note"

class NotesCreateView(CreateView):
    model = Notes
    fields = ['title', 'content']
    success_url = '/smart/notes'