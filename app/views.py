import json
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Information


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("upload")
        else:
            messages.error(request, "Wrong username and password!")
            return redirect("login")
    else:
        return render(request, "login.html")


@login_required
def upload_json(request):
    if request.method == "GET":
        return render(request, "upload.html")
    elif request.method == "POST":
        json_file = request.FILES["jsondocument"]
        if not json_file.name.endswith(".json"):
            messages.error(request, f"{json_file.name} is not JSON")
            return HttpResponseRedirect(reverse("upload"))
        try:
            f = json.load(json_file)
            for entry in f:
                id = entry["id"]
                user_id = entry["userId"]
                title = entry["title"]
                body = entry["body"]
                form = Information(id, user_id, title, body)
                form.save()
        except json.JSONDecodeError:
            messages.error(request, "Unable to parse JSON, bad formatting")
            return HttpResponseRedirect(reverse("upload"))
        except Exception as e:
            messages.error(request, f"Unable to upload json file {e}")
        return redirect(reverse("info"))


class InfoView(LoginRequiredMixin, generic.ListView):
    template_name = "info.html"
    context_object_name = "info_list"

    def get_queryset(self):
        return Information.objects.values("title", "body")
