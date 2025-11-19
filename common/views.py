from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from common.forms import UserForm, EmailAuthenticationForm


# Create your views here.


class EmailLoginView(View):
    template_name = "login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = EmailAuthenticationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        # 명시적으로 넣어주자.
        form = EmailAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect("home")
        return render(request, self.template_name, {"form": form})


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=raw_password)
            return redirect("login")
    else:
        form = UserForm()
    return render(request, "signup.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")
