## Make Project
django-admin startproject smartnotes
cd smartnotes

## Run Server
python manage.py runserver

## Make an App
django-admin startapp home
add 'home' to INSTALLED_APPS in smartnotes/smartnotes/settings.py

in home\views.py
    make def home(request)

in smartnotes\smartnotes\urls.py
    add from home import views
    add path to url patterns

Views are sort of like flask routes

## Serving HTML
cd into app, cd home
create folder (templates)
create folder in templates folder with same name as app (home)
then you can render those with (return render(request, 'home/welcome.html', {}))

use those brackets to pass data that can be used with jinja2
    return render(request, 'home/welcome.html', {'today': datetime.today()})

this makes a template in Django Template Language (DTL) which is interpreted to HTML

## Reducing App Dependancy
Apps should be easily deletable, so we remove the import dependancy in smartnotes/urls.py by creating a similar url file inside of home and then including the home views as strings in the smartnotes/urls.py file like this:

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
```

## Django Admin 
reach at the /admin point

Need to initially configure the database

migrations track the changes to the database

django has authentication out of the box

run this to initially configure the admin auth

```bash
python manage.py migrate
```

To create an account / superuser run

```bash
python manage.py createsuperuser
```

configure name/email/password

## Auth
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin')
def authorized(request):
    return render(request, 'home/authorized.html', {})
```

go back to home/urls.py and add
```python 
urlpatterns = [
    path('home', views.home),
    path('authorized', views.authorized),
]
```

## Obeject Relational Mapping (ORM)
Make class tables like Flask
these turn into database tables with the use of migrations

to make a table, create a class like this
```python
class Notes(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

After making the table class run
```bash
python manage.py makemigrations
python manage.py migrate
```

go to the notes/admin.py file to enable control of the Notes table from the admin dashboard

```python
from django.contrib import admin
from . import models

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(models.Notes, NotesAdmin)
```

Access table entires as objects

```python
from notes.models import Notes
mynote = Notes.objects.get(pk='1')
mynote.title
'Django is cool'
```

Make an entry
```python
newNote = Notes.objects.create(title='A second note', content='cmd')
```

See entries
```python
Notes.objects.all()
```

Can do all sorts of filters on object entires

by adding this, 

```py
urlpatterns = [
    path('notes', views.list),
    path('notes/<int:pk>', views.detail)
]
```

You create a url for any pk you pass to detail

## Class based views