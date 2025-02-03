from datetime import datetime

from .forms import UserRegistrationForm

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'today': datetime.today()}


class AuthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'home/authorized.html'
    login_url = '/admin'


class LoginInterfaceView(LoginView):
    template_name = "home/login.html"


class LogoutInterfaceView(LogoutView):
    template_name = "home/logout.html"


class RegisterInterfaceView(CreateView):
    template_name = "home/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        user = form.save()  # Save the user with hashed password
        self.object = user  # Set self.object to avoid AttributeError

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            self.request, 
            username = username, 
            password = password
        )

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        
        else:
            form.add_error(None, "Authentication failed. Try logging in.")
            return self.form_invalid(form)