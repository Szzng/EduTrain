from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import CreateView, FormView, UpdateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register/register.html'
    success_url = reverse_lazy('course:index')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = UserUpdateForm
    template_name = 'register/update.html'
    success_url = reverse_lazy('register:login')

    def get_object(self, queryset=None):
        return self.request.user


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'register/login.html'
    success_url = reverse_lazy('course:index')

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = auth.authenticate(self.request, email=email, password=password)
        if user:
            auth.login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            return str(self.request.GET.get('next'))
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('course:index'))


