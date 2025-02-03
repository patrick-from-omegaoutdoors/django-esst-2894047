from django import forms
from django.core.exceptions import ValidationError

from .models import Notes


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'content': forms.Textarea(attrs={'class': "form-control mb5"})
        }
        labels = {
            'content': 'Write your thoughts here:'
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if 'Django' not in title:
            raise ValidationError(
                'We only accept notes with Django in the title'
            )
        
        return title