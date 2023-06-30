from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import RegistrationForm, LoginForm
from django.views.generic.edit import CreateView
from .forms import SignUpForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'accounts/signup.html'


class RegistrationView:
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Замените 'home' на ваш URL-шаблон
        return render(request, 'registration.html', {'form': form})


class LoginView:
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile.html')  # Замените 'home' на ваш URL-шаблон
            form.add_error(None, 'Неверные имя пользователя или пароль.')
        return render(request, 'login.html', {'form': form})

#
# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect('index.html')  # Замените 'home' на ваш URL-шаблон
